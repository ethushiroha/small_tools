from Models.Reminders.CardReminder import CardReminder
from Models.Reminders.BasicReminder import BasicReminder
from Models.Reminders.SitReminder import SitReminder


class Reminder:

    def __init__(self, func=None):
        if func is not None:
            self.__Parse(func)
        else:
            self.func = None

    def __Parse(self, func):
        if func == "card":
            self.func = CardReminder
        if func == "Sit":
            self.func = SitReminder

    def remind(self):
        if self.func is None:
            return
        if self.func.__base__.__name__ != BasicReminder.__name__:
            return
        return self.func.Remind()
