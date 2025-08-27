import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
cookie = config.get("cookie")


def get_response(url, data):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "cookie": cookie,
    }
    resp = requests.get(url=url, headers=headers, params=data)
    return resp
