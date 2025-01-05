import requests
import json
import webbrowser


def download(file_name):
    # API URL
    api_url = "https://hyuu9p3nu1.execute-api.ap-northeast-3.amazonaws.com/dev"

    # 請求的 Headers
    headers = {
        "Content-Type": "application/json"
    }

    # 請求的 Body
    body = {
        "bucket_name": "file-system2",
        "file_key": file_name
    }
    print("========= Data Processing... pls wait ========= ")

    try:
        # 發送 POST 請求
        response = requests.post(api_url, headers=headers, json=body)
        response_data = response.json()
        
        # 檢查回應狀態碼
        if response.status_code == 200:
            print("========= Data Successfully Downloaded, Opening the webbrowser...=========")
            body_str = response_data.get("body")
            body_data = json.loads(body_str)
            download_url = body_data.get("download_url")

            if download_url:
                print(f"Download URL: {download_url}")
                # 自動開啟瀏覽器
                webbrowser.open(download_url)
            else:
                print("Download URL not found in response.")
        else:
            print(f"Error: {response_data.get('message', 'Unknown error')}")

    except Exception as e:
        print(f"Error occurred: {e}")
