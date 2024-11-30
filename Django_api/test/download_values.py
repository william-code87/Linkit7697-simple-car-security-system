import requests,json
import pandas as pd

#----------------------------------API_G002_GET_TEST----------------------------------
# 輸入要GET的API
get_rdata = requests.get('http://127.0.0.1:8000/G002/')
# 將得到的Response格式化輸出
print(pd.DataFrame(get_rdata.json()))
print("--------------------------------------------------------------------------------")
#----------------------------------API_G002_POST_TEST----------------------------------
payload = {"Longitude":121.5}
post_rdata = requests.post("http://127.0.0.1:8000/G002/", json=payload)
print(pd.DataFrame(post_rdata.json()))