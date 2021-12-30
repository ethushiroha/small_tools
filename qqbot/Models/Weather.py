import json


class Weather:
    def __init__(self, ans: json = None):
        if ans is None:
            return
        self.success = ans['success']
        self.city = ans['city']
        self.week = ans['week']
        self.weather = ans['weather']
        self.Temp = ans['Temp']
        self.days = []
        for day in ans['Days']:
            self.days.append(WeatherDay(day))
        self.hours = []
        for hour in ans['Hours']:
            self.hours.append(WeatherHour(hour))

    def get_tomorrow(self):
        return self.days[0]

    def get_today(self):
        return self.hours

    def __str__(self):
        tmp1 = []
        for day in self.days:
            tmp1.append(day.__str__())
        tmp2 = []
        for hour in self.hours:
            tmp2.append(hour.__str__())
        ans = {
            "成功": self.success,
            "城市": self.city,
            "星期": self.week,
            "天气": self.weather,
            "温度": self.Temp,
            "未来预报": tmp1,
            "小时预报": tmp2,
        }
        print(ans.__str__())
        return json.dumps(ans, ensure_ascii=False, sort_keys=False, indent=4).encode('utf-8')


class WeatherDay:
    def __init__(self, ans: json = None):
        if ans is None:
            return
        self.day_info = ans['day_info']
        self.day_weather = ans['day_weather']
        self.night_weather = ans['night_weather']
        self.day_Temp = ans['day_Temp']
        self.night_Temp = ans['night_Temp']

    def __str__(self) -> json:
        ans = {
            "日期": self.day_info,
            "白天天气": self.day_weather,
            "白天温度": self.day_Temp,
            "夜晚天气": self.night_weather,
            "夜晚温度": self.night_Temp
        }
        return str(ans)


class WeatherHour:
    def __init__(self, ans: json = None):
        if ans is None:
            return
        self.hour_info = ans['hour_info']
        self.weather = ans['weather']
        self.Temp = ans['Temp']

    def __str__(self) -> json:
        ans = {
            "时间": self.hour_info,
            "天气": self.weather,
            "温度": self.Temp
        }
        return str(ans)
