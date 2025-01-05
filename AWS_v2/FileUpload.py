import os
import boto3
import base64
import json
import requests

def upload(filePath):
    filename = os.path.basename(filePath)
    print(f"Filename: {filename}")
    
    signature = os.getenv("signature_")

    lambda_client = boto3.client('lambda', region_name='ap-northeast-1')
    bucket_file_name = filename

    # 讀取檔案並編碼為 Base64
    with open(filePath, 'rb') as file:
        file_content = base64.b64encode(file.read()).decode('utf-8')

    data = {
        'file_name': bucket_file_name,
        'file_content': file_content,
        'signature': signature
    }
    if not signature:
        print("please login first!")
        return
    lambda_url = "https://6auheksf66higjqjm54fgqidoe0etfyi.lambda-url.ap-northeast-1.on.aws/"

    # 設置標頭
    headers = {"Content-Type": "application/json"}
    print(f"File uploading...")
    # 發送 POST 請求到 Lambda
    response = requests.post(lambda_url, headers=headers, data=json.dumps(data))

    #print("HTTP 狀態碼：", response.status_code)
    print(response.json()["message"])


