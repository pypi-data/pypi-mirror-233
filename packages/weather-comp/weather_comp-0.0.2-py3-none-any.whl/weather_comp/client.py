import requests
import time
import datetime;
import json

user = None
channel = None
thingSpeakChannelId = None
thingSpeakApiKey = None

last_send_time = 0

def send_init_request(data, log = True):
    url = 'https://weather-comp.region.mo/api/client/user'
    try:
        response = requests.post(url, json=data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            global user
            user = result.get('data').get('user')
            global channel
            channel = user.get('channel')
            global thingSpeakChannelId
            thingSpeakChannelId = channel.get('thingSpeakChannelId')
            global thingSpeakApiKey
            thingSpeakApiKey = channel.get('thingSpeakApiKey')
            if log:
                ct = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
                print('weather-comp::init>', ct, '用戶認證成功')
        else:
            if log:
                ct = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
                print('weather-comp::init>', ct,'請求失敗，錯誤代碼：', response.status_code)
    except requests.Timeout:
        if log:
            ct = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
            print('weather-comp::init>', ct,'請求超時')


def init(username, password, log = True):
    data = {
        'username': username,
        'password': password
    }
    send_init_request(data, log)

def send(data = {}, log = True):
    # 0. 檢查是否已經初始化
    if user is None or channel is None or thingSpeakChannelId is None or thingSpeakApiKey is None:
        if log:
            ct = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
            print('weather-comp::send>', ct,'請先執行 init()')
        return

    # 1. 檢查時間
    global last_send_time
    current_time = time.time()
    if current_time - last_send_time >= 30 or last_send_time == 0:
        last_send_time = current_time
    else:
        if log:
            ct = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
            print('weather-comp::send>', ct,'請求過於頻繁, 請求間隔須至少30秒')
        return
    
    # 2. 檢查輸入資料
    if type(data) is not dict:
        if log:
            ct = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
            print('weather-comp::send>', ct,'data 必須是dict 型別')
        return
    
    # 3. 準備新的 data
    if data.get('LONG') is None and data.get('LAT') is None and data.get('PM2.5') is None and data.get('PM10') is None and data.get('CO') is None and data.get('SO2') is None and data.get('NO2') is None and data.get('O3') is None:
        if log:
            ct = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
            print('weather-comp::send>', ct,'data 必須包含至少一個欄位')
        return

    new_data = {
        'api_key': thingSpeakApiKey,
        'field1': data.get('LONG'),
        'field2': data.get('LAT'),
        'field3': data.get('PM2.5'),
        'field4': data.get('PM10'),
        'field5': data.get('CO'),
        'field6': data.get('SO2'),
        'field7': data.get('NO2'),
        'field8': data.get('O3')
    }

    # print(new_data)

    url = 'https://api.thingspeak.com/update.json'

    try:
        response = requests.post(url, json=new_data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if result == 0:
                if log:
                    ct = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
                    print('weather-comp::send>', ct,'資料上傳失敗')
            else:
                if log:
                    ct = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
                    print('weather-comp::send>', ct,'資料上傳成功\n', json.dumps(result, sort_keys=True, indent=4))
        else:
            if log:
                ct = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
                print('weather-comp::send>', ct,'請求失敗，錯誤代碼：', response.status_code)
    except requests.Timeout:
        if log:
            ct = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
            print('weather-comp::send>', ct,'請求超時')

# init('superadmin', '')
# send({
#     'LONG': 121.5654,
#     'LAT': 25.0330,
#     'PM2.5': 10,
#     'PM10': 20,
#     'CO': 30,
#     'SO2': 40,
#     'NO2': 50,
#     'O3': 60
# })
