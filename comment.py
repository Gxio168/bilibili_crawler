from response import get_response
import csv
from w_rid import get_query_with_wrid


def get_comment(oid, dir):
    f = open(dir + "data.csv", mode="a", encoding="utf-8", newline="")
    csv_writer = csv.DictWriter(f, fieldnames=["昵称", "性别", "地区", "评论"])
    csv_writer.writeheader()
    url = "https://api.bilibili.com/x/v2/reply/wbi/main"
    params = get_params(oid=oid, offset="")
    resp = get_response(url=url, data=params)
    json_data = resp.json()
    info_list = []
    for i in range(50):
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
        params = get_params(oid=oid, offset=offset)
        resp = get_response(url, params)
        json_data = resp.json()
    f.close()


def get_params(oid, offset):
    template = {
        "mode": "2",
        "oid": f"{oid}",
        "pagination_str": '{"offset":"' + offset + '"}',
        "plat": "1",
        "seek_rpid": "",
        "type": "1",
        "web_location": "1315875",
    }
    return get_query_with_wrid(template)
