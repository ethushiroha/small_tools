import json

from Config.Config import source, logger
from Logger.DefaultLogger import make_debug_info
from Utils.Timer import Time


class SignData:
    def __init__(self, userid=0, continuous=0, sum_days=0, last_sign_timestamp=0, commits=""):
        self.userid: int = userid
        self.continuous_days: int = continuous
        self.sum_days: int = sum_days
        self.last_sign_timestamp: int = last_sign_timestamp
        self.commits: int = commits

    @staticmethod
    def query(user_id):
        print("query ==> ", user_id)
        sql = "select userid, continuous_days, sum_days, last_sign_timestamp, commits from SignData where userid = {}" \
            .format(int(user_id))
        print(sql)
        rows = source.execute(sql).fetchall()
        if len(rows) == 0:
            return None
        print(rows[0])
        row = rows[0]
        logger.sql(sql=sql, ans=str(row))
        sign = SignData(
            userid=int(row[0]),
            continuous=int(row[1]),
            sum_days=int(row[2]),
            last_sign_timestamp=int(row[3]),
            commits=row[4]
        )
        return sign

    @staticmethod
    def update(user_id, continuous=None, sum_days=None, commits=None):
        sql = "update SignData " \
              "set "
        if continuous is not None:
            sql += "continuous_days={},".format(continuous)
        if sum_days is not None:
            sql += "sum_days={},".format(sum_days)
        if commits is not None:
            sql += "commits='{}',".format(commits)

        sql += "last_sign_timestamp={} ".format(Time.get_timestamp())
        sql = sql + "where userid={};".format(user_id)
        print(sql)
        source.execute(sql)
        logger.sql(sql=sql, ans="")
        return SignData.query(user_id)

    @staticmethod
    def insert(user_id, commits=None) -> list:
        time_stamp = Time.get_timestamp()
        if commits is None:
            commits = " "
        sql = "insert into SignData " \
              "(userid, continuous_days, sum_days, last_sign_timestamp, commits) " \
              "values ({}, 1, 1, {}, \'{}\')" \
            .format(int(user_id), time_stamp, commits)
        print(sql)
        source.execute(sql)
        logger.sql(sql=sql, ans="")
        return SignData.query(user_id)

    def __str__(self):
        ans = {
            "userid": self.userid,
            "continue": self.continuous_days,
            "sum_days": self.sum_days,
            "timestamp": self.last_sign_timestamp,
            "commits": self.commits
        }
        return json.dumps(ans, indent=4, sort_keys=True)
