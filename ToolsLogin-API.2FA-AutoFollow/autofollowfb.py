from selenium import webdriver

from selenium.webdriver.common.by import By

from time import sleep as sl

import requests 

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

def convert_cookie_to_string(data):
	string_cookie = ""
	
	for d in data:
		
		string_cookie += d['name']+"="+d['value']+"; "
	
	return string_cookie	
	
	sl(2)
	
	driver.get ("https://www.facebook.com/Info.NguyenTheDat.Username")
	
	sl(2)

	btn_follow = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[4]/div/div/div[2]/div/div/div").click()
	
	# btn_follow.click()

	sl(10)
		
username = ""

password = ""

two_fa = ""
login(username,password,two_fa) 	 


