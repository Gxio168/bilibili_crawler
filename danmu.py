import requests
import re


def get_danmu():
    url = "https://api.bilibili.com/x/v2/dm/wbi/web/seg.so?type=1&oid=1512399639&pid=1153355619&segment_index=1&pull_mode=1&ps=120000&pe=360000&web_location=1315873&w_rid=a92241461f2cd3e2480111106ba3798d&wts=1756119154"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "origin": "https://www.bilibili.com",
        "referer": "https://www.bilibili.com/video/BV1wZ421e7Fr",
    }
    resp = requests.get(url = url, headers = headers)
    resp.encoding = "utf-8"
    print(resp.text)
