import time

EIGHT_HOUR = 8 * 60 * 60
DAY = 3 * EIGHT_HOUR


class Time:

    @staticmethod
    def getNowTime() -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", Time.get_localtime())

    @staticmethod
    def get_localtime():
        return time.localtime()

    @staticmethod
    def get_timestamp() -> int:
        return int(time.time())

    @staticmethod
    def is_next_day(last, now) -> int:
        day_count_last = last // DAY
        day_count_now = now // DAY
        if day_count_last > day_count_now:
            raise Exception("date Error")
        return day_count_now - day_count_last
