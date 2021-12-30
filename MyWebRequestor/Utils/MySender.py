import json

import requests

from MyWebRequestor.Utils.MyParser import MyParser


class Sender:
    def __init__(self, url=None, headers=None, method=None, bodyType=None):
        """
        @param headers: 请求头
        @param method: 请求方法，request.get / request.post
        @param bodyType: json/context，仅post有效
        """
        self.headers = headers
        self.method = method
        self.url = url
        self.type = bodyType

    @staticmethod
    def getFromJson(json_path):
        j: dict = MyParser.ParseJson(json_path)
        if j is None:
            return None
        sender = Sender()

        # parse Url
        url = j.get("url")
        if url is None:
            return None
        sender.url = url

        # parse headers
        headers: dict = j.get("headers")
        if headers is None:
            return None
        sender.headers = dict(headers)

        # parse method
        method = j.get("method")
        if method is None:
            return None
        if method == "get":
            sender.method = requests.get
            sender.type = None

        elif method == "post":
            sender.method = requests.post

        return sender

    def send(self):
        res = self.method(url=self.url, headers=self.headers)
        print(res.text)
        return res

    def __str__(self):
        object_dict = {
            "method: ": self.method.__name__,
            "headers: ": self.headers,
            "type: ": self.type,
        }
        return json.dumps(object_dict, indent=4, sort_keys=False)
