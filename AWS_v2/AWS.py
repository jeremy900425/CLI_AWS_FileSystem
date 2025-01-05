import argparse
import os
import SignUp
import Authenticate
import FileUpload
import FileDownload
from dotenv import set_key
from dotenv import load_dotenv

auth = Authenticate.Authenticate()
    
def fileUpload(filePath):
    if not os.path.isfile(filePath):
        print(f"File {filePath} does not exist.")
        return False
    print(f"File {filePath} exists.")
    FileUpload.upload(filePath)

def signup(acc,pwd):
    print("acc:",acc, "pwd:",pwd)
    SignUp.signup(acc,pwd)

def login(acc, pwd):
    state = auth.normal_login(acc, pwd)
    if state:
        print(f"Sucess！Hello Account：{acc}")
    else:
        print("Login Fail! pls check your account or password")

def main():
    parser = argparse.ArgumentParser(description="===============================\nThis is AWS Access CLI \n ===============================")
    subparsers = parser.add_subparsers(dest="command")

    signup_parser = subparsers.add_parser("signup", help="<acc> <pwd>")
    signup_parser.add_argument("acc", help="使用者帳號")
    signup_parser.add_argument("pwd", help="使用者密碼")

    login_parser = subparsers.add_parser("login", help="<acc> <pwd>")
    login_parser.add_argument("acc", help="使用者帳號")
    login_parser.add_argument("pwd", help="使用者密碼")

    fileUpload_parser = subparsers.add_parser("fileUpload", help="<FilePath>")
    fileUpload_parser.add_argument("filePath", help="檔案路徑")

    fileDownload_parser = subparsers.add_parser("fileDownload", help="<FileName>")
    fileDownload_parser.add_argument("FileName", help="檔案名稱")

    
    checkToken_parser = subparsers.add_parser("checkToken", help="(No parameter)This command can check the token How long it will be expired")
    logout_parser = subparsers.add_parser("logout", help="(No parameter)This command can logout the user")


    args = parser.parse_args()

    # 處理登入
    load_dotenv()

    if args.command == "signup":
        signup(args.acc, args.pwd)
    elif args.command == "login":
        login(args.acc, args.pwd)
    elif args.command == "checkToken":
        auth.check_expiration()
    elif args.command == "fileUpload":
        fileUpload(args.filePath)
    elif args.command == "fileDownload":
        FileDownload.download(args.FileName)
    elif args.command == "logout":
        set_key("./AWS_v2/.env", "signature_", "")
        print("Logout success!")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
