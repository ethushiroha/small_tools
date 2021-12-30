import json

import requests

from Config.Config import MyWeatherApiData
from Models.Weather import Weather, WeatherDay, WeatherHour


class WeatherRequester:
    @staticmethod
    def get_weather(parm=None) -> Weather:
        data = {
            "app": MyWeatherApiData.app,
            "sign": MyWeatherApiData.sign,
            "appkey": MyWeatherApiData.appKey,
            "format": "json",
            "weaid": MyWeatherApiData.city_id,
            "ag": MyWeatherApiData.mode
        }
        res = requests.post(url=MyWeatherApiData.url, data=data)
        if res.status_code != 200:
            # raise Exception?
            return None
        ans = json.loads(res.text)
        ans = WeatherParser.parse(ans)
        w = Weather(ans)
        if parm is None:
            return w
        elif parm == "今天":
            ans = []
            for i in range(6):
                ans.append(w.hours[i].__str__())
            return json.dumps(ans, ensure_ascii=False, sort_keys=True, indent=4)
        elif parm == "明天":
            return w.days[0]
        elif parm == "后天":
            return w.days[1]

    @staticmethod
    def get_message(user_id, parm: list = None) -> str:
        print("parm ==>", parm)
        if (parm is not None) and (len(parm) > 0):
            parm = parm[0]
        else:
            parm = None
        w = WeatherRequester.get_weather(parm)
        msg = ""
        if type(w) == Weather:
            msg = "[CQ:at,qq={}] 天气预报: \n{}".format(user_id, w.__str__().decode('utf-8'))
        elif type(w) == WeatherDay:
            msg = "[CQ:at,qq={}] 天气预报: \n{}".format(user_id, w.__str__())
        elif type(w) == str:
            msg = w
        return msg


class WeatherParser:

    @staticmethod
    def parse(ans: json) -> json:
        print("ans ==> ", ans)
        result = {
            'success': ans['success'],
            'city': ans['result']['area_1'] + ans['result']['area_2'],
            'week': ans['result']['realTime']['week'],
            'weather': ans['result']['realTime']['wtNm'],
            'Temp': ans['result']['realTime']['wtTemp'],
            'Days': [],
            'Hours': []
        }
        for a in ans['result']['futureDay']:
            tmp = {
                "day_info": a['dateYmd'] + "   " + a['week'],
                "day_weather": a['wtNm1'],
                "night_weather": a['wtNm2'],
                "day_Temp": a['wtTemp1'],
                "night_Temp": a['wtTemp2']
            }
            result['Days'].append(tmp)
        for a in ans['result']['futureHour']:
            tmp = {
                "hour_info": a['dateYmdh'],
                "weather": a['wtNm'],
                "Temp": a['wtTemp']
            }
            result['Hours'].append(tmp)
        return result
