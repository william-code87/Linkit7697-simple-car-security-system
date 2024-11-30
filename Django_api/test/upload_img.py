import requests,json,cv2

#----------------------------------API_G005_POST_TEST----------------------------------
# BODY傳輸格式
headers = {'Content-Type': 'application/binary'}
with open(r"C:\Users\user\Desktop\pythonAPI\chumpower_api\test\map.png", 'rb') as artifact:
    res = requests.post("http://127.0.0.1:8000/G005/", headers=headers, data=artifact)
    print(res)
    artifact.close()