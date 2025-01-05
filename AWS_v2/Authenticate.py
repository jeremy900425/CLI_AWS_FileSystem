import os
from dotenv import load_dotenv, set_key
import hmac
import hashlib
import time
import base64
import json
import requests

class Authenticate:
    SECRET_KEY = "my_super_secret_key"  # 用來生成 HMAC

    def __init__(self, env_path='./AWS_v2/.env'):
        self.env_path = env_path
        self._ensure_env_file()
        load_dotenv(self.env_path)

    def _ensure_env_file(self):
        if not os.path.exists(self.env_path):
            with open(self.env_path, 'w') as f:
                f.write('DB_HOST="mydb.c7mgm26yshd5.ap-northeast-1.rds.amazonaws.com"\n')
                f.write('DB_PORT="5432"\n')
                f.write('DB_NAME="postgres"\n')
                f.write('DB_USER="postgres"\n')
                f.write('DB_PASSWORD="ssvs6337A"\n')
                f.write('signature_=""\n')
    def normal_login(self, username, password):
        lambda_url = "https://azvjohpdvrpq47m36cv2kkump40kcouw.lambda-url.ap-northeast-1.on.aws/"
        headers = {"Content-Type": "application/json"}
        data = {
            "username": username,
            "password": password
        }
        print("========= Data Processing... pls wait ========= ")
        response = requests.post(lambda_url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            # print(response.json()["message"])
            # print(response.json()["signature"])
            set_key("./AWS_v2/.env", "signature_", response.json()["signature"])
            return True
        elif response.status_code == 401:
            return False
        else:
            print("Error: Lambda error")
            return False


    def check_expiration(self):
        """檢查 Token 的剩餘有效時間"""
        signature = os.getenv("signature_")
        if not signature:
            print("Error: Token no exist。")
            return
        
        # 分離 Base64 編碼的 Payload 和 簽名
        payload_encoded, signature = signature.rsplit('.', 1)
        # 解碼 Base64 獲取原始的 JSON 字符串
        payload_str = base64.urlsafe_b64decode(payload_encoded).decode()
        expiration_timestamp = int(json.loads(payload_str)["expire"])

        current_timestamp = int(time.time())
        remaining_time = int(expiration_timestamp) - current_timestamp
        if remaining_time <= 0:
            print("Token Expired！")
        else:
            hours, remainder = divmod(remaining_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"Token remaining time: {hours} hours, {minutes} minutes, {seconds} seconds")
    def _parse_token(self, token):
        try:
            # 分割 Token 為 Payload 和 Signature
            payload_base64, signature = token.split(".")
            
            # 驗證簽名
            expected_signature = hmac.new(self.SECRET_KEY.encode(), payload_base64.encode(), hashlib.sha256).hexdigest()
            if signature != expected_signature:
                print("Error：Token signature error！")
                return False
            
            # 解碼 Payload
            payload_json = base64.urlsafe_b64decode(payload_base64).decode()
            payload = json.loads(payload_json)
            # print(payload) {'username': 'test', 'expire': 1735022270}
            # 驗證過期時間
            current_timestamp = int(time.time())
            if current_timestamp > payload["expire"]:
                print("Error：Token expired！")
                return False
            
            print("Token verification success！")
            return True
        except Exception as e:
            print(f"Error： {e}")
            return False
# Example usage:
# auth = Authenticate()
# token = auth.create_access_token("admin")
# auth.check_expiration()
# payload = auth.parse_token("eyJ1c2VybmFtZSI6ICJ0ZXN0IiwgImV4cGlyZSI6IDE3MzUwMjIyNzB9.b0195c657575e346158faefb3aa79cabc7c905d6fddfdcad0447b71c237fd178")