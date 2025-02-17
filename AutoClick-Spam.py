import pyautogui as autospam 	# as là dùng để đổi tên thư viện 
import time 					# thư viện có sẵn trên máy 

time.sleep(2)						# thời gian delay autospam 
	
	#auto click 
print(autospam.position()) 		# lấy chuột để định hướng tọa độ rồi ctrl + b để tìm tọa độ   
#(x=1761, y=1044)					# tọa độ được tìm thấy  
for i in range(10):				# số lần muốn click  
	autospam.click(x=1761, y=1044) 	# click vào tạo độ đã được tìm thấy  

	#auto spam 
for i in range(100):              	# số lần muốn spam  
	time.sleep(2)                  	# thời gian spam giữa các lệnh 
	autospam.write("nhap noi dung cua ban vao day "+str(i)) 	# +str(i) là dùng để đếm số lần in ra "dcm "
	autospam.hotkey("enter")		# nhấn vào phím ở bàn phím ( enter, space , shift...)
# 									# muốn thêm câu spam thì lại dùng for tiếp 
# for i in range(10):
# 	time.sleep(3)
# 	autospam.write(" nhap noi dung cua ban vao day  "+str(i))
# 	autospam.hotkey("enter")