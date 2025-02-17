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

driver = webdriver.Chrome('chromedriver.exe')

driver.get("https://fb.com")

sl(1)

input_username = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input") 
# input_username.click()

input_username.send_keys("100084701153823")

input_password = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input")

input_password.send_keys("vOU7J9B")

btn_login = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button")

btn_login.click()

sl(3)

input_2fa = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div[1]/div/form/div/div[2]/div[3]/span/input")

input_2fa.send_keys("826839")

btn_continue = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div[1]/div/form/div/div[3]/div[1]/button")

btn_continue.click()

btn_continue_save_browse = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div[1]/div/form/div/div[3]/div[1]/button")


btn_continue_save_browse.click()

