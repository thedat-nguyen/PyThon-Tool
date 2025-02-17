# import os
# for i in range(5):	
# 	os.system(" start browser.exe ")

#########

# import webbrowser as wb 

# key = "youtube"
# wb.open("https://www.google.com/search?q="+key)

#selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep as sl
import requests 
driver = webdriver.Chrome('chromedriver.exe')
def login(username,password,two_fa):
	driver.get("https://fb.com")
	sl(1)
	input_username = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input") 
	# input_username.click()
	input_username.send_keys(username)
	input_password = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input")
	input_password.send_keys(password)
	btn_login = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button")
	btn_login.click()
	btn_login 
	sl(3)
	val_2fa = get_2fa(two_fa) 
	input_2fa = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div[1]/div/form/div/div[2]/div[3]/span/input")
	input_2fa.send_keys(val_2fa)
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
# def get_cookie():
# 	data = [{'domain': '.facebook.com', 'expiry': 1669021635, 'httpOnly': False, 'name': 'wd', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1036x758'}, {'domain': '.facebook.com', 'expiry': 1669021629, 'httpOnly': False, 'name': 'locale', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'en_GB'}, {'domain': '.facebook.com', 'expiry': 1669021635, 'httpOnly': False, 'name': 'dpr', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1.25'}, {'domain': '.facebook.com', 'expiry': 1702976826, 'httpOnly': True, 'name': 'datr', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'OQVyYyBHjwmMoeH5yM6eFlFK'}, {'domain': '.facebook.com', 'httpOnly': True, 'name': 'checkpoint', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '%7B%22u%22%3A100084701153823%2C%22t%22%3A1668416833%2C%22step%22%3A0%2C%22n%22%3A%22qxLIENnKPWc%3D%22%2C%22inst%22%3A130738279759543%2C%22f%22%3A190115151632257%2C%22st%22%3A%22c%22%2C%22aid%22%3Anull%2C%22ca%22%3Anull%2C%22la%22%3A%221%22%2C%22ta%22%3A%221668416834.ch.s%3Aat%3Aat%3As%3Apw.tDBEAiAyPh5VzbYQu8qN-V5TAG-DMMXewGREYcQqa9RYNdxfAwIgHXMpc7vQJW3W_mmdVm1hkpuaYl9JUYncTb5ErAJ8I50%22%2C%22ffvaid%22%3Anull%2C%22ffvasec%22%3Anull%2C%22tfvaid%22%3Anull%2C%22tfvasec%22%3Anull%2C%22sat%22%3Anull%2C%22idg%22%3Afalse%2C%22cidue%22%3A%22%22%2C%22tfdsn%22%3Anull%2C%22tfvri%22%3Anull%2C%22s%22%3A%22AWU4K8wVbREByIPuuss%22%2C%22cs%22%3A%5B%5D%2C%22ssp%22%3A1%7D'}, {'domain': '.facebook.com', 'expiry': 1676192830, 'httpOnly': True, 'name': 'fr', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '0hWTDzGDqM30fR8oB..BjcgU5.VJ.AAA.0.0.BjcgU_.AWUKrfxfDuw'}, {'domain': '.facebook.com', 'expiry': 1702976825, 'httpOnly': True, 'name': 'sb', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'OQVyY_UqbIqQP7z7SyUAWfD5'}]
# 	cookie = dict()
# 	for d in data:
# 		cookie[d['name']] = d['value']
# 	return cookie
def convert_cookie_to_string(data):
	string_cookie = ""
	for d in data:
		string_cookie += d['name']+"="+d['value']+"; "
	return string_cookie
username = "100085052388120" 				#nhap id vao day
password = "2q1XZFN"						#nhap password 
two_fa = "WU4L722XXUAORNMGCJSADBLIAENPMVOM"	#nhap 2fa

login(username,password,two_fa) 
