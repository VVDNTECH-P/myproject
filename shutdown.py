from flask import Flask

import  os
import platform
import time 

def clear_terminal():
	print(f"\nPLATFORM = {platform.system()}")
	if 'Linux' in platform.system():
		print("aman")
		time.sleep(5)
		os.system("clear")
		print("hii vivek")

	if 'Windows' in platform.system():
		os.system("cls")
		

#os.system("shutdown -c")
if __name__ == '__main__':
	clear_terminal()
hwDFJGSABVHWGVXFVWFDASV JEWFDHXGabnSVdwVA
hfffjnffffffjjjjjjjjjjjjjjjdcsbahdf
app=Flask(__name__)
@app.route('/')
def simple():
	return ("well come to API program ")
if __name__=="__main__":
	app.run(debug=True)
	krhejs


