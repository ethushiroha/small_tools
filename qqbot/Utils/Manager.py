import traceback
import requests
from Exceptions.ParseException import ParseException
from Models.Msg import Msg
from Utils.Sign import Signer
from Utils.WebExploitApi import *
from Config.Config import *
from Utils.WeatherRequester import WeatherRequester
from Utils.Translator import Translator


class Parser:
    def __init__(self, msg: Msg):
        if msg is None:
            raise Exception("msg is None")

        self.command = None
        self.parameter: list = None
        self.group_id = msg.group_id
        Sender.data['group_id'] = self.group_id
        self.sender = msg.sender.user_id

        index = msg.raw_message.find("  ")
        while index != -1:
            msg.raw_message = msg.raw_message.replace("  ", " ")
            index = msg.raw_message.find("  ")

        msg_split_list = msg.raw_message.split(" ")
        self.__getCommand(msg_split_list[0])
        self.__getParameter(msg_split_list[1:])
        self.execute()

    def __getCommand(self, raw_msg: str) -> None:
        try:
            if raw_msg[0] != "/":
                self.command = None
                return
            self.command = raw_msg
        except Exception as e:
            traceback.print_exc()
            self.command = None
            logger.error("__getCommand error " + e.__str__())
            raise ParseException("__getCommand: " + e.__str__())

    def __getParameter(self, raw_msg: list):
        try:
            self.parameter = raw_msg
        except Exception as e:
            traceback.print_exc()
            self.parameter = None
            raise ParseException("__getParameter: " + e.__str__())

    def execute(self) -> dict:
        try:
            command_log_info(self.command)
            if self.command == "/打卡":
                Sender.data['message'] = Signer.attempt_to_sign(self.sender, self.parameter)
                res = send_msg()
                return {"status_code": res.status_code, "text": res.text}
            elif self.command == "/查看备注":
                Sender.data['message'] = Signer.get_commit(user_id=self.sender)
                res = send_msg()
                return {"status_code": res.status_code, "text": res.text}
            elif self.command == "/修改备注":
                Sender.data['message'] = Signer.edit_commit(self.sender, self.parameter)
                res = send_msg()
                return {"status_code": res.status_code, "text": res.text}
            elif self.command == "/天气预报":
                Sender.data['message'] = WeatherRequester.get_message(user_id=self.sender, parm=self.parameter)
                res = send_msg()
                return {"status_code": res.status_code, "text": res.text}
            elif self.command == "/whois":
                Sender.data['message'] = Whois.get(self.parameter[0])
                res = send_msg()
                return {"status_code": res.status_code, "text": res.text}
            elif self.command == "/ip":
                Sender.data['message'] = Ip2Addr.get(self.parameter[0])
                res = send_msg()
                return {"status_code": res.status_code, "text": res.text}
            elif self.command == "/translate":
                if self.parameter[0] == "en":
                    self.parameter.pop(0)
                    Sender.data['message'] = Translator.translate(list2str(self.parameter), "en")
                else:
                    Sender.data['message'] = Translator.translate(list2str(self.parameter))
                res = send_msg()
                return {"status_code": res.status_code, "text": res.text}
            elif self.command == "/占座":
                MyCSULabSitData.flag = True
                Sender.data['message'] = "成功设置"
                res = send_msg()
                return {"status_code": "true"}
        except Exception as e:
            traceback.print_exc()
            logger.error("execute error " + e.__str__())
            # raise Exception?


def list2str(parm: list) -> str:
    res = ""
    for c in parm:
        res += c + " "
    return res


def send_msg() -> requests.Response:
    url = Sender.top_url + "send_group_msg"
    logger.debug({"request.data": Sender.data})
    res = requests.post(url=url, data=Sender.data)
    logger.info("request to {}, response for {} ==> {}"
                .format(url, res.status_code, res.text))
    return res


def command_log_info(command: str) -> None:
    logger.info("get command for: {}".format(command))
