from Config.Config import Sender
from Models.Reminders.BasicReminder import BasicReminder
from Utils.Manager import send_msg
from Utils.CSULibSitor import CSULibSitor
from Config.Config import MyCSULabSitData


class SitReminder(BasicReminder):

    @staticmethod
    def Remind(user_id=0):
        if MyCSULabSitData.flag is False:
            return None
        else:
            target = CSULibSitor.get()
            if target is not None:
                Sender.data['message'] = target.__str__()
            else:
                Sender.data['message'] = "发生错误"
        res = send_msg()
        return {"status": "ok"}
