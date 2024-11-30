import requests,json,cv2

#----------------------------------API_G004_GET_TEST----------------------------------
res = requests.get("http://127.0.0.1:8000/G004/")
# 開啟寫檔位置
fh = open("download_map.png", "wb")
fh.write(res.content)
fh.close()
print("下載完成")