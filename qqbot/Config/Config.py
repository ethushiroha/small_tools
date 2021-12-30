from Logger.DefaultLogger import DefaultLogger
from Models.DataSource import MyDataSource

logger = DefaultLogger()
source = MyDataSource()


class Sender:
    top_url = "http://127.0.0.1:5700/"

    headers = {
        "Cookie": "access_token=404b58f4-850c-4a38-9930-6c7e4d2c30f8"
    }

    data = {
        "group_id": 594600349,
        "auto_escape": False
    }


class MyWeatherApiData:
    app = "weather.realtime"
    sign = "987f833ec4c6d4c2d2b40aec05314d05"
    appKey = "59232"
    city_id = "2869"
    mode = "today,futureDay,futureHour"
    url = "http://api.k780.com/"


class MyTranslateApiData:
    app_id = "20200212000383203"
    key = "YcaOPOoEsIIWP3gt5zIy"
    api_url = "https://fanyi-api.baidu.com/api/trans/vip/translate"


class MyCSULabSitData:
    # username = "8208181311"
    username = "8208181317"
    password = "c6f057b86584942e415435ffb1fa93d4"
#    password = "a723157b7a7ff9df03eb2166c5e3cdd5"
    flag = False
#    chair_num = 10799
    chair_num = 10550
    area = 100
#    area = 103
