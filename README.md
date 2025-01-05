# Welcome to CLI AWS FileSystem

This guide provides instructions for using the CLI AWS FileSystem project, primarily for macOS. If you're using Windows, you may need to adjust the commands accordingly.

---

## Installation and Preparation

### Prerequisites
- Ensure your Python version is **Python 3.9**.

### Steps to Install
1. Clone or download the repository:
   ```bash
   git clone https://github.com/jeremy900425/CLI_AWS_FileSystem.git
   cd CLI_AWS_FileSystem
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Optional Configuration
The main executable file is `./AWS_v2/AWS.py`. You can configure it as an environment variable for easier access. For example:
```bash
export AWS_CMD="python ./AWS_v2/AWS.py"
```
(Note: Adapt the command depending on your shell, e.g., `bash`, `zsh`, etc.)

### Test the Setup
Run the following command to verify the setup:
```bash
$AWS_CMD -h
```

---

## Feature Introduction
Ensure your working directory is set to `/User/.../CLI_AWS_FileSystem`. Check the manual with the following command:
```bash
python ./AWS_v2/AWS.py -h
```

### Manual Output:
```text
=============================== This is AWS Access CLI ===============================

positional arguments:
  {signup,login,fileUpload,fileDownload,checkToken,logout}
    signup              <acc> <pwd>
    login               <acc> <pwd>
    fileUpload          <FilePath>
    fileDownload        <FileName>
    checkToken          (No parameter) This command can check how long the token will remain valid
    logout              (No parameter) This command logs out the user

optional arguments:
  -h, --help            Show this help message and exit
```

### Commands Overview

#### 1. `python ./AWS_v2/AWS.py signup <acc> <pwd>`
- Use this command to create an account in the system. All data is encrypted using SSL-like mechanisms during signup.
- Example:
  ```bash
  python ./AWS_v2/AWS.py signup XiaoLai YYDS
  ```

#### 2. `python ./AWS_v2/AWS.py login <acc> <pwd>`
- Log in to the system using your credentials.
- Example:
  ```bash
  python ./AWS_v2/AWS.py login XiaoLai YYDS
  ```

#### 3. `python ./AWS_v2/AWS.py checkToken`
- Check the remaining time of your JWT-like Command Line Token stored in the `.env` file.
- Example:
  ```bash
  python ./AWS_v2/AWS.py checkToken
  ```

#### 4. `python ./AWS_v2/AWS.py fileUpload <FilePath>`
- Upload a file to the S3 bucket.
- Example:
  ```bash
  python ./AWS_v2/AWS.py fileUpload ./AWS_v2/UploadFile/link.pdf
  ```

#### 5. `python ./AWS_v2/AWS.py fileDownload <FileName>`
- Download a file from the S3 bucket.
- Example:
  ```bash
  python ./AWS_v2/AWS.py fileDownload link.pdf
  ```

#### 6. `python ./AWS_v2/AWS.py logout`
- Log out and clear the Command Line Token.
- Example:
  ```bash
  python ./AWS_v2/AWS.py logout
  ```

---

## Use Cases
Follow this step-by-step story to understand the full functionality of the system:

### 1. Ensure Logout
```bash
python ./AWS_v2/AWS.py logout
```
- Verify that you are logged out.

### 2. Attempt File Upload Without Login
```bash
python ./AWS_v2/AWS.py fileUpload ./AWS_v2/UploadFile/link.pdf
```
- Expected Output: `Please login first!`

### 3. Attempt Login Without Signup
```bash
python ./AWS_v2/AWS.py login XiaoLia YYDS
```
- Expected Output: `Login Fail! Please check your account or password.`

### 4. Signup a New Account
```bash
python ./AWS_v2/AWS.py signup XiaoLia YYDS
```
- Expected Output: `Account and password inserted successfully. Please try to login again!`

### 5. Login Successfully
```bash
python ./AWS_v2/AWS.py login XiaoLia YYDS
```
- Expected Output: `Success! Hello Account: XiaoLia`

### 6. Check Token Validity
```bash
python ./AWS_v2/AWS.py checkToken
```
- Expected Output: `Token remaining time: xx hours, xx minutes, xx seconds.`

### 7. Upload a File
```bash
python ./AWS_v2/AWS.py fileUpload ./AWS_v2/UploadFile/link.pdf
```
- Upload the file to the S3 bucket.

### 8. Download a File
```bash
python ./AWS_v2/AWS.py fileDownload link.pdf
```
- Download the previously uploaded file.

### 9. Logout
```bash
python ./AWS_v2/AWS.py logout
```
- Clear the Command Line Token.

### 10. Confirm Logout by Upload Attempt
```bash
python ./AWS_v2/AWS.py fileUpload ./AWS_v2/UploadFile/link.pdf
```
- Expected Output: `Please login first!`

---

## Notes
- Always ensure your working directory is correctly set to avoid errors.
- For further assistance, use the `-h` or `--help` flag with any command to see detailed usage instructions.

---

**Happy Coding!**
