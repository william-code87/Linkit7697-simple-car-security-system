import requests,json

#----------------------------------API_G000_GET_TEST----------------------------------
# 輸入要GET的API
get_rdata = requests.get('http://127.0.0.1:8000/G000/')
# 將得到的Response格式化輸出
print(get_rdata.text)