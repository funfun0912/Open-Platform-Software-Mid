import requests
import json
import csv
from pprint import pprint
#from google.colab import files

client_id = 's1111528-a3f10b32-ab51-4ae5'
client_secret = '0e8e4133-2717-40fc-bb13-bf2f59400d6f'

# 填入你的 client_id 和 client_secret
app_id = 's1111528-a3f10b32-ab51-4ae5'
app_key = '0e8e4133-2717-40fc-bb13-bf2f59400d6f'

auth_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
url = "https://tdx.transportdata.tw/api/basic/v2/Rail/TRA/LiveTrainDelay?$top=30&$format=JSON"

class Auth():
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        return {
            'content-type': 'application/x-www-form-urlencoded',
        }

    def get_auth_data(self):
        return {
            'grant_type': 'client_credentials',
            'client_id': self.app_id,
            'client_secret': self.app_key
        }

class data():
    def __init__(self, app_id, app_key, auth_response):
        self.app_id = app_id
        self.app_key = app_key
        self.auth_response = auth_response

    def get_data_header(self):
        try:
            auth_JSON = self.auth_response.json()  # 使用 .json() 方法解析 JSON
            access_token = auth_JSON['access_token']
        except KeyError:
            raise Exception("Access token not found in response.")

        return {
            'Authorization': 'Bearer ' + access_token,
            'Accept': 'application/json',
        }

if __name__ == '__main__':
    try:
        # 進行 OAuth 認證請求
        a = Auth(app_id, app_key)
        auth_response = requests.post(auth_url, data=a.get_auth_data())
        auth_response.raise_for_status()  # 檢查請求是否成功

        d = data(app_id, app_key, auth_response)  # 使用取得的 token 進行資料請求
        data_response = requests.get(url, headers=d.get_data_header())
        data_response.raise_for_status()  # 檢查請求是否成功

    except requests.exceptions.RequestException as e:
        print(f"Error during the request: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")

    # 印出認證資料
    print(auth_response)
    pprint(auth_response.text)

    # 解析資料並存儲
    try:
        data_json = data_response.json()  # 解析資料
        with open('api.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['TrainNo', 'StationName', 'DelayTime', 'SrcUpdateTime', 'UpdateTime'])

            # 寫入資料
            for train in data_json:
                writer.writerow([
                    train['TrainNo'],
                    train['StationName']['Zh_tw'],  # 使用中文站名
                    train['DelayTime'],
                    train['SrcUpdateTime'],
                    train['UpdateTime']
                ])


        print("✅ 資料已成功寫入 api.csv")
        #files.download('LiveTrainDelay.csv')

    except KeyError as e:
        print(f"Missing expected data field: {e}")
