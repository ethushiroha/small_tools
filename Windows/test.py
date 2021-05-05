import requests

url = "http://baidu.com"

res = requests.get(url)

print(res.status_code)
