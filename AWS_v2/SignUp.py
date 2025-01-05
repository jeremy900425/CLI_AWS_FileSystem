import requests
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import bcrypt
from cryptography.hazmat.primitives import padding as symmetric_padding
import secrets
import json
import base64
import os


def generate_symmetric_key(file_path):
    """
    生成一把對稱密鑰並儲存到指定檔案
    """
    # 生成 256 位元的隨機對稱密鑰
    symmetric_key = secrets.token_bytes(32)  # 256 bits = 32 bytes

    # 將密鑰寫入檔案
    with open(file_path, "wb") as key_file:
        key_file.write(symmetric_key)

    print(f"Symmetric key generated and saved to {file_path}")

def check_and_generate_symmetric_key():
    """
    檢查根目錄是否有對稱密鑰檔案，沒有則創建
    """
    file_path = "./AWS_v2/Symkey.pem"
    if not os.path.exists(file_path):
        print(f"{file_path} not found. Generating new symmetric key...")
        generate_symmetric_key(file_path)
    else:
        print(f"{file_path} already exists. No need to generate a new key.")

def load_public_key(public_key_path: str):
    """
    載入 PEM 格式的公鑰
    """
    with open(public_key_path, "rb") as public_key_file:
        return serialization.load_pem_public_key(public_key_file.read())

def encrypt_message(message: str, public_key) -> str:
    """
    使用公鑰加密訊息，並以 Base64 格式返回
    """
    encrypted_message = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted_message).decode()

def load_symmetric_key(file_path: str) -> bytes:
    """
    加載對稱密鑰
    """
    with open(file_path, "rb") as key_file:
        return key_file.read()


def encrypt_with_symmetric_key(message: str, symmetric_key: bytes) -> str:
    # """
    # 使用對稱密鑰加密訊息，並以 Base64 格式返回
    # """
    # iv = secrets.token_bytes(16)  # 128 bits IV
    # cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv))
    # encryptor = cipher.encryptor()
    # encrypted_message = encryptor.update(message.encode('utf-8')) + encryptor.finalize()
    # return base64.b64encode(iv + encrypted_message).decode()  # 包含 IV

    """
    使用 AES-CBC 模式加密訊息，並以 Base64 格式返回
    :param message: 要加密的明文
    :param symmetric_key: 對稱密鑰
    :return: 加密後的 Base64 字串，包含 IV 和密文
    """
    iv = secrets.token_bytes(16)
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    padder = symmetric_padding.PKCS7(algorithms.AES.block_size).padder()
    padded_message = padder.update(message.encode('utf-8')) + padder.finalize()

    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()

    return base64.b64encode(iv + encrypted_message).decode('utf-8')

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    # 將 bcrypt 雜湊結果編碼為 Base64 字符串（保持短小）
    return base64.b64encode(password_hash).decode('utf-8')

def send_to_lambda(account: str, password: str, public_key_path: str,sym_key_path: str, lambda_url: str):
    """
    加密帳號和密碼後，發送到 AWS Lambda 並返回解密結果
    """
    # 載入公鑰
    public_key = load_public_key(public_key_path)

    # 載入私鑰
    sym_key = load_symmetric_key(sym_key_path)

    # 使用對稱密鑰加密帳號和密碼
    account = encrypt_with_symmetric_key(account, sym_key)
    password = encrypt_with_symmetric_key(password, sym_key)
    # 使用公鑰加密對稱密鑰
    encrypted_symmetric_key = encrypt_message(base64.b64encode(sym_key).decode(), public_key)

    # 公鑰加密帳號和密碼
    encrypted_data = {
        "account": encrypt_message(account, public_key),
        "pwd": encrypt_message(password, public_key),
        "sym_key": encrypted_symmetric_key
    }
    # print("公鑰加密後的訊息（Base64 格式）：", encrypted_data)
    print("========= Data Securely Encrypted =========")

    # 發送請求到 Lambda
    headers = {"Content-Type": "application/json"}
    response = requests.post(lambda_url, headers=headers, data=json.dumps(encrypted_data))

    # 處理 Lambda 回應
    if response.status_code == 200:
        response_body = response.json()
        print(response_body["ReturnMessage"], ", pls try to login again !")
        return response_body 
    else:
        print("Lambda 處理失敗，狀態碼：", response.status_code, "回應內容：", response.text)
        return None
def signup(acc,pwd):
    # 檢查對稱密鑰
    check_and_generate_symmetric_key()

    account = acc
    password = pwd
    public_key_path = "./AWS_v2/Publickey.pem"
    sym_key_path = "./AWS_v2/Symkey.pem"
    lambda_url = "https://5nssduss2bfckb7d2cssndtkjm0jxowj.lambda-url.ap-northeast-1.on.aws/"
    print("========= Data Processing... pls wait ========= ")

    send_to_lambda(account, password, public_key_path, sym_key_path, lambda_url)
