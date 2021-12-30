from baseproxy.proxy import ReqIntercept, RspIntercept, AsyncMitmProxy
import json

__author__ = 'qiye'
__date__ = '2018/6/21 23:35'


class DebugInterceptor(ReqIntercept, RspIntercept):
    def deal_request(self, request):
        return request

    def deal_response(self, response):
        data = response.get_body_data()
        print("data ==> ", data)
        if b"2021-10-25 22:24:27" in data:
            data_json = json.loads(data)
            data_json['data'][0]['sampleDate'] = "2021-11-03 15:34:15"
            data_json['data'][0]['reportDate'] = "2021-11-03 22:24:27"
            response.set_body_data(json.dumps(data_json).encode())
        return response


if __name__ == "__main__":
    baseproxy = AsyncMitmProxy(https=True)
    baseproxy.register(DebugInterceptor)
    baseproxy.serve_forever()
