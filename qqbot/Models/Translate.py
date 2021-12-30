import json


class Translate:
    def __init__(self, res_dict: dict = None):
        if res_dict is None:
            return None
        self.from_language = str(res_dict.get("from"))
        self.to_language = str(res_dict.get("to"))
        self.src = str(res_dict.get("trans_result")[0].get("src"))
        self.dst = str(res_dict.get("trans_result")[0].get("dst"))

    def __str__(self):
        object_dict = {
            "源语言": self.from_language,
            "目标语言": self.to_language,
            "原语句": self.src,
            "翻译结果": self.dst
        }
        return json.dumps(object_dict, indent=4, sort_keys=False, ensure_ascii=False)

