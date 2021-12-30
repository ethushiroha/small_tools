import json


class LibSit:
    def __init__(self, res_dict: dict = None):
        if res_dict is None:
            return None

        self.msg = str(res_dict.get("msg"))
        self.error = False

        if self.msg != "预约成功":
            self.error = True
        else:
            try:
                data = res_dict.get("data").get("list")
                self.begin = str(data.get("beginTime").get("date"))
                self.ends = str(data.get("endTime").get("date"))
                self.update = str(data.get("updateTime").get("date"))
                self.position = str(data.get("spaceInfo").get("areaInfo").get("nameMerge")
                                    + data.get("spaceInfo").get("name"))
            except Exception as e:
                pass

    def __str__(self):
        object_dict = None
        if self.error is True:
            object_dict = {
                "错误": self.msg
            }
        else:
            object_dict = {
                "状态": self.msg,
                "预约时间": self.update,
                "位置": self.position,
                "时间": self.begin + " ==> " + self.ends
            }
        return json.dumps(object_dict, indent=4, sort_keys=False, ensure_ascii=False)
