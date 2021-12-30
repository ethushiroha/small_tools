import datetime
import json

import requests


def login(username: str, password: str) -> str:
    url = "http://libzw.csu.edu.cn/api.php/login"
    data = {
        "username": username,
        "password": password,
        "from": "mobile"
    }
    headers = {
        "Host": "libzw.csu.edu.cn",
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "Origin": "http://www.skalibrary.com",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.9(0x1800092e) NetType/WIFI Language/zh_CN",
        "Referer": "http://www.skalibrary.com/",
        "Content-Length": "73",
        "Accept-Language": "zh-cn",
    }
    res = requests.post(url, headers=headers, data=data)
    if res.status_code == 200:
        res_dict: dict = json.loads(res.text)
        print(res_dict)
        return res_dict["data"]["_hash_"]["access_token"]
    else:
        print(res.status_code)
        print(res.text)


next_day = (datetime.datetime.now() + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
print(next_day)


def get_segment() -> int:
    # 103 ==> 3 楼 测试用
    # 101 ==> 2 楼
    area = 103
    segment_url = "http://libzw.csu.edu.cn/api.php/space_time_buckets?" \
                  "area={}&day={}".format(area, next_day)
    segment_headers = {
        "Host": "libzw.csu.edu.cn",
        "Origin": "http://www.skalibrary.com",
        "Connection": "close",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.9(0x1800092e) NetType/WIFI Language/zh_CN",
        "Accept-Language": "zh-cn",
        "Referer": "http://www.skalibrary.com/",
        "Accept-Encoding": "gzip, deflate",
    }
    segment_res = requests.get(segment_url, headers=segment_headers)
    if segment_res.status_code == 200:
        res_dict = json.loads(segment_res.text)
        return res_dict['data']['list'][0]['id']
    else:
        print(segment_res.status_code)
        print(segment_res.text)


def get_chair(chair_num: int, token: str, username: str, segment: int) -> str:
    data = {
        "access_token": token,
        "userid": username,
        "type": 1,
        "segment": segment,
        "id": chair_num
    }
    headers = {
        "Host": "libzw.csu.edu.cn",
        "Origin": "http://www.skalibrary.com",
        "Connection": "close",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.9(0x1800092e) NetType/WIFI Language/zh_CN",
        "Accept-Language": "zh-cn",
        "Referer": "http://www.skalibrary.com/",
        "Accept-Encoding": "gzip, deflate",
    }

    url = "http://libzw.csu.edu.cn/api.php/spaces/{}/book".format(chair_num)
    res = requests.post(url, headers=headers, data=data)
    if res.status_code == 200:
        print("成功")
        res_dict = json.loads(res.text)
        print(res_dict)
        return res_dict["msg"]
    else:
        print("失败")
        print(res.status_code)
        print(res.text)


# 默认抢二楼的位置，修改楼层请修改 get_segment 函数中的 area 变量

# 二楼A区为 100， 二楼B区为101
# 三楼A区为 102， 以此类推。。。。

# 二楼 A 区 BF2A001 的 id 为 10497， A区最后 BF2A088 为 10584
# B区 10585 - 10736
# 三楼 A 区 10737 - 10798 。。。。
# 数据包在 burp.txt 中，可以自己发包找数据
def main():
    # 你的学号

    username = ""
    password = ""

    token = login(username, password)
    segment = get_segment()
    # 10799 测试用
    # 10677
    # ans = get_chair(chair_num=10799, token=token, segment=segment, username=username)
    print(segment)


if __name__ == '__main__':
    main()
