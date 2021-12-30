import json


class MyParser:
    @staticmethod
    def ParseJson(json_path):
        try:
            with open(json_path, 'r') as f:
                j = json.load(f)
                return j
        except FileNotFoundError as e:
            # file not found
            return None
        except Exception as e:
            return None
