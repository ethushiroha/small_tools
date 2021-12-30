import json
import urllib
from hashlib import md5

import requests
from Config.Config import MyTranslateApiData
from Models.Translate import Translate


class Translator:
    @staticmethod
    def translate(sentence: str, to_language: str = "zh") -> str:
        try:
            data = {
                "q": sentence,
                "appid": MyTranslateApiData.app_id,
                "from": "auto",
                "to": to_language,
                "sign": "",
                "salt": "1234",
            }
            data = Translator.__calc_sign(data)
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            print("sentence ==> ", sentence)
            print("data ==> ", data)
            res = requests.post(MyTranslateApiData.api_url, headers=headers, data=data)
            print("text ==> ", res.text)
            if res.status_code == 200:
                res_json = json.loads(res.text)
                return Translate(res_json).__str__()
            else:
                return "error"
        except Exception as e:
            return e.__str__()

    @staticmethod
    def __calc_sign(data: dict) -> dict:
        appid = data.get("appid")
        q = data.get("q")
        salt = data.get("salt")
        key = MyTranslateApiData.key
        tmp = appid + q + salt + key
        sign = md5(tmp.encode()).hexdigest()
        data['sign'] = sign
#         data['q'] = urllib.parse.quote(data['q'])
        return data
