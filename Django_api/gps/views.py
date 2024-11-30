from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pymysql,json

server = "127.0.0.1"  # 主機
db_username = "test"  # 使用者帳號
db_password = "test"  # 使用者密碼
db_database = "test"
db_table = "dht"

# 開始新增需要的功能
#----------------------------------建立資料表----------------------------------
# 無須帶入參數
# 成功 ： 回傳OK
# 失敗 ： 回傳ERROR
@csrf_exempt
def G000(request):
    # 判斷是否使用POST，是才處理
    if request.method == "GET":
        # 資料庫建立語法
        sql = ("CREATE TABLE dht (ID INT AUTO_INCREMENT,"
               "Celisius VARCHAR,"
               "Fahrenheit VARCHAR,"
               "Humidity VARCHAR)")
        try:
            # 指定連結的資料庫
            db = pymysql.connect(host=server, user=db_username, password=db_password, database=db_database)
            # 使用 cursor() 方法創建一個游標對象 cursor
            cursor = db.cursor()
            # 使用 execute() 方法執行 SQL，如果資料表存在則删除
            cursor.execute("DROP TABLE IF EXISTS dht")
            # 執行建立指令
            cursor.execute(sql)
            # 允許資料庫更新資訊
            db.commit()
            print("創建完成")
            status = "OK"
        except:
            # 資料庫回傅錯誤訊息
            db.rollback()
            print("創建失敗")
            status = "ERROR"
        # 關閉資料庫連結
        db.close()
        # 回傳狀態
        return HttpResponse(status)
#----------------------------------資料上傳----------------------------------
# 成功 ： 回傳OK
# 失敗 ： 回傳ERROR
@csrf_exempt
def G001(request):
    # 判斷是否使用POST，是才處理
    if request.method == "POST":
        # 讀取body
        data = json.loads(request.body)
        print(data['Celisius'])
        # 資料庫上傳語法
        sql = ("INSERT INTO dht (Celisius, Fahrenheit, Humidity)"
                   " VALUES ('%s', '%s', '%s')") % \
                (data['Celisius'], data['Fahrenheit'], data['Humidity'])
        print(sql)
        try:
            # 指定連結的資料庫
            db = pymysql.connect(host=server, user=db_username, password=db_password, database=db_database)
            # 使用 cursor() 方法創建一個游標對象 cursor
            cursor = db.cursor()
            # 執行建立指令
            cursor.execute(sql)
            # 允許資料庫更新資訊
            db.commit()
            print("上傳完成")
            status = "OK"
        except:
            # 資料庫回傅錯誤訊息
            db.rollback()
            print("上傳失敗")
            status = "ERROR"
        # 關閉資料庫連結
        db.close()
        # 回傳狀態
        return HttpResponse(status)
#----------------------------------資料查詢----------------------------------
# 成功 ： 回傳所查詢到的對應值
# 失敗 ： 回傳ERROR
@csrf_exempt
def G002(request):
    # 判斷是否使用POST，是才處理
    if request.method == "POST":
        # 資料庫查詢語法
        sql = ("SELECT * FROM `dht` ORDER BY id DESC LIMIT 1 OFFSET 1")
        print(sql)
                # 宣告dict
        rejdata = []
        try:
            # 指定連結的資料庫
            db = pymysql.connect(host=server, user=db_username, password=db_password, database=db_database)
            # 使用 cursor() 方法創建一個游標對象 cursor
            cursor = db.cursor()
            # 執行建立指令
            cursor.execute(sql)
            # 允許資料庫更新資訊
            db.commit()
            # 獲取符合條件資料的值
            results = cursor.fetchall()
            #將list拆解
            for row in results:
                id = row[0]
                Celisius = row[1]
                Fahrenheit = row[2]
                Humidity = row[3]
                # 紀錄查詢到的資料
                jdata = {"Id":id,"Celisius":Celisius,"Fahrenheit":Fahrenheit,"Humidity":Humidity}
                rejdata.append(jdata)
                print(rejdata)
                print("----------------------------------------------------------")
            print("查詢完成")
        except:
            # 資料庫回傅錯誤訊息
            db.rollback()
            print("查詢失敗")
        # 關閉資料庫連結
        db.close()
        # 回傳狀態
        return HttpResponse(json.dumps(rejdata),content_type="application/json")
