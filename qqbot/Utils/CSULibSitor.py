import json
import datetime

import requests

from Models.CSULibSit import LibSit
from Config.Config import MyCSULabSitData
from Config.Config import logger


class CSULibSitor:
    next_day = None

    @staticmethod
    def __get_next_day():
        CSULibSitor.next_day = (datetime.datetime.now() + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")

    @staticmethod
    def __get_token() -> int:
        username = MyCSULabSitData.username
        password = MyCSULabSitData.password
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

        logger.info("request to {}, response for {} ==> {}"
                    .format(url, res.status_code, res.text))

        if res.status_code == 200:
            res_dict: dict = json.loads(res.text)
            return res_dict["data"]["_hash_"]["access_token"]
        else:
            return None

    @staticmethod
    def __get_segment():
        # 103 ==> 3 楼 测试用
        # 101 ==> 2 楼
        area = MyCSULabSitData.area
        segment_url = "http://libzw.csu.edu.cn/api.php/space_time_buckets?" \
                      "area={}&day={}".format(area, CSULibSitor.next_day)
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
        logger.info("request to {}, response for {} ==> {}"
                    .format(segment_url, segment_res.status_code, segment_res.text))

        if segment_res.status_code == 200:
            res_dict = json.loads(segment_res.text)
            return res_dict['data']['list'][0]['id']
        else:
            return None

    @staticmethod
    def get() -> LibSit:
        CSULibSitor.__get_next_day()

        if MyCSULabSitData.flag is False:
            return None
        try:
            token = CSULibSitor.__get_token()
            segment = CSULibSitor.__get_segment()
            if (token is None) or (segment is None):
                return None

            username = MyCSULabSitData.username
            chair_num = MyCSULabSitData.chair_num

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

            logger.info("request to {}, response for {} ==> {}"
                        .format(url, res.status_code, res.text))

            if res.status_code == 200:
                res_dict = json.loads(res.text)
                MyCSULabSitData.flag = False
                return LibSit(res_dict)
            else:
                return None
        except Exception as e:
            logger.error(e.__str__())
            return None




