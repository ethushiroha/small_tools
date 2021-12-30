from Models.Reminders.BasicReminder import BasicReminder
from Utils.Manager import send_msg
from Config.Config import *


class CardReminder(BasicReminder):

    @staticmethod
    def Remind(user_id=0):
        Sender.data['message'] = "[CQ:at,qq=all] 要记得今天的打卡呀～"
        res = send_msg()
        return {"status": "ok"}
