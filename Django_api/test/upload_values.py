import requests

#----------------------------------API_G001_POST_TEST----------------------------------
# 傳送的參數
payload = {"Longitude":121.5,"Latitude":23.5}
# POST G001 API
r = requests.post("http://127.0.0.1:8000/G001/", json=payload)
print("上傳完成")