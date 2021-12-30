import inspect
import json

from Exceptions.LoggerException import LoggerException
from Utils.Timer import Time


class DefaultLogger:
    def __init__(self):
        try:
            self.info_logger = open("info.log", 'w+')
            self.error_logger = open("error.log", 'w+')
            self.debug_logger = open("debug.log", 'w+')
            self.sql_logger = open("sql.log", 'w+')
        except Exception as e:
            raise LoggerException("init logger error" + e)

    def info(self, msg) -> None:
        m = Time.getNowTime() + " | [INFO] | " + msg + "\n\n"
        self.info_logger.write(m)
        self.info_logger.flush()
        print(m, flush=True)

    def error(self, msg) -> None:
        m = Time.getNowTime() + " | [ERROR] | " + msg + "\n\n"
        self.error_logger.write(m)
        self.error_logger.flush()
        print(m, flush=True)

    def debug(self, variable: dict, m="") -> None:
        msg = str(variable)
        tmp_msg = Time.getNowTime() + ": " + m + "\n" + msg + "\n\n"
        self.debug_logger.write(tmp_msg)
        self.debug_logger.flush()
        print(tmp_msg, flush=True)

    def sql(self, sql, ans) -> None:
        msg = Time.getNowTime() + "| SQL | " + sql + " ==> " + ans + "\n\n"
        self.sql_logger.write(msg)
        self.sql_logger.flush()
        print(msg, flush=True)

    def __del__(self):
        try:
            self.info_logger.close()
            self.error_logger.close()
            self.debug_logger.close()
            self.sql_logger.close()
        except Exception as e:
            raise LoggerException("close logger error" + e)


def retrieve_name(var):
    """
    Gets the name of var. Does it from the out most frame inner-wards.
    :param var: variable to get name from.
    :return: string
    """
    for fi in reversed(inspect.stack()):
        names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
        if len(names) > 0:
            return names[0]


def make_debug_info(*variables) -> dict:
    ans = {}
    for var in variables:
        ans[retrieve_name(var)] = var
    return ans
