import sqlite3


class MyDataSource:
    def __init__(self):
        # self.conn = sqlite3.connect("/Users/shirohaethu/Documents/GitHub/small_tools/qqbot/data.sqlite")
        self.conn = sqlite3.connect("/opt/qqbot/database/data.sqlite")
        self.cursor = self.conn.cursor()

    def execute(self, sql):
        ans = self.cursor.execute(sql)
        self.conn.commit()
        return ans

    def __del__(self):
        self.conn.commit()
        self.conn.cursor().close()
        self.conn.close()
