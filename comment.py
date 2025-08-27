from response import get_response
import time
import hashlib
from urllib.parse import urlencode
import csv



def get_comment():
    f = open("data.csv", mode="a", encoding="utf-8", newline="")
    csv_writer = csv.DictWriter(f, fieldnames=["昵称", "性别", "地区", "评论"])
    csv_writer.writeheader()
    url = "https://api.bilibili.com/x/v2/reply/wbi/main"
    params = get_params(oid="1153355619", offset="", wts=int(time.time()))
    resp = get_response(url, params)
    json_data = resp.json()
    info_list = []
    for i in range(1):
        replies = json_data["data"]["replies"]
        offset = json_data["data"]["cursor"]["pagination_reply"]["next_offset"]
        for reply in replies:
            dit = {
                "昵称": reply["member"]["uname"],
                "性别": reply["member"]["sex"],
                "地区": reply["reply_control"]["location"],
                "评论": reply["content"]["message"],
            }
            info_list.append(dit)
        csv_writer.writerows(info_list)
        info_list = []
        params = get_params(oid="1153355619", offset=offset, wts=int(time.time()))
        resp = get_response(url, params)
        json_data = resp.json()
    f.close()


def get_params(oid, offset, wts):
    template = {
        "mode": "2",
        "oid": f"{oid}",
        "pagination_str": '{"offset":"' + offset + '"}',
        "plat": "1",
        "seek_rpid": "",
        "type": "1",
        "web_location": "1315875",
        "wts": f"{wts}",
    }
    w_rid = get_w_rid(template)
    template["w_rid"] = w_rid
    return template


def get_w_rid(params):
    md5_hash = hashlib.md5()
    query_string = urlencode(params) + "ea1db124af3c7062474693fa704f4ff8"
    md5_hash.update(query_string.encode("utf-8"))
    return md5_hash.hexdigest()
