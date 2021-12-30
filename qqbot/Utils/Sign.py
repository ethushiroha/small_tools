from Config.Config import logger
from Logger.DefaultLogger import make_debug_info

from Models.SignData import SignData
from Utils.Timer import Time


class Signer:

    @staticmethod
    def attempt_to_sign(user_id, commit=None) -> str:
        if commit is not None:
            m = Signer.__list_to_str(commit)
            return Signer.default_sign(user_id, commit=m)
        else:
            return Signer.default_sign(user_id)

    @staticmethod
    def default_sign(user_id, commit=None) -> str:
        sign = SignData.query(user_id)
        if sign is None:
            sign = SignData.insert(user_id, commits=commit)
        else:
            time_stamp = Time.get_timestamp()

            debug_info = make_debug_info(sign.last_sign_timestamp, time_stamp)
            logger.debug(debug_info)
            print("last ==> {}, now ==> {}".format(sign.last_sign_timestamp, time_stamp))

            # 打卡间隔超过一天
            ans = Time.is_next_day(sign.last_sign_timestamp, time_stamp)
            if ans == 0:
                print(SignData.query(user_id))
                data = "[CQ:at,qq={}] 今天已经打过卡啦，学习辛苦啦～".format(user_id)
                return data
            elif ans > 1:
                sign = SignData.update(user_id=user_id, continuous=0, sum_days=(sign.sum_days + 1), commits=commit)

        sign = SignData.update(user_id=user_id, continuous=(sign.continuous_days + 1), sum_days=(sign.sum_days + 1),
                               commits=commit)
        if commit is None:
            commit = ""
        data = "[CQ:at,qq={}] 今天打卡成功，连续打卡{}天，累计打卡{}天。你的备注是：{}" \
            .format(user_id, sign.continuous_days, sign.sum_days, commit)
        return data

    @staticmethod
    def get_commit(user_id) -> str:
        ans = ""
        sign = SignData.query(user_id=user_id)
        if sign is None:
            return "[CQ:at,qq={}] 你还没有写备注哦"
        ans += "[CQ:at,qq={}] 你的备注是： {}".format(user_id, sign.commits)
        return ans

    @staticmethod
    def edit_commit(user_id, new_commit: list) -> str:
        new_commit = Signer.__list_to_str(new_commit)
        sign = SignData.query(user_id=user_id)
        if sign is None:
            return "[CQ:at,qq={}] 你还没有写过备注哦".format(user_id)
        sign = SignData.update(user_id=user_id, commits=new_commit)
        ans = "[CQ:at,qq={}] 修改成功，你现在的备注是: {}".format(user_id, sign.commits)
        return ans

    @staticmethod
    def __list_to_str(l: list) -> str:
        m = ""
        for c in l:
            m += c + " "
        return m
