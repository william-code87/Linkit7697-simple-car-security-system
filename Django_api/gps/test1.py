from sys import argv
from base64 import b64encode
from json import dumps

# 圖片轉檔用
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
        base64data = b64encode(binaryData)
        base64_string = base64data.decode('utf-8')
    return base64data

empPicture = convertToBinaryData("map.png")
base64.emp = b64encode(empPicture)

file_str=open('test.png','wb')
file_str.write(base64.b64decode(empPicture))
file_str.close()