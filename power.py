import serial
import time
import logging
import mysql.connector
from datetime import datetime
from pymysql import*
#import xlwt
import pandas.io.sql as sql

MCUserialport = ""
data = ""
vdd_cam_1v2 = ""
vdd_cam_1v8 = ""
vreg_bob_3p3_3p5 = ""
vdd_cam_2v8 = ""
Measured_Voltage_1 = ""
Measured_Voltage_2 = ""
Measured_Voltage_3 = ""
Measured_Voltage_4 = ""
Resolution ="" 
vol_data = ""



def command_send(cmd):
	print('###################################################  BUZZER TEST   ###################################################')
	global MCUserialport
	MCUserialport.write(cmd + "\r")
	print("\n "+ cmd +" \n")
	time.sleep(5)
	read_data = MCUserialport.readline()
	print(read_data)
	        



command_send("BUZZER ON")

command_send("BUZZER OFF")



def command_1():
	print('###################################################  BUZZER TEST   ###################################################')
	global MCUserialport
	MCUserialport.write("BUZZER ON\r")
	print("\n BUZZER ON \n")
	time.sleep(5)
	read_data = MCUserialport.readline()
	print(read_data)
	        


 
        


def command_2():
	print('###################################################  CAM_AVDD_2P8_EN TEST START  ###################################################')
	global MCUserialport
	MCUserialport.write("CAM_AVDD_2P8_EN\r")
	print('\nCAM_AVDD_2P8_EN\n')
	print("done")
	time.sleep(1)

	#while True:

	read_data = MCUserialport.readline()
	print(read_data)
	    



def command_3():
	print('###################################################  CAM_AVDD_2P8_DI TEST START  ###################################################')
	global MCUserialport

	MCUserialport.write("CAM_AVDD_2P8_DI\r")
	print('\nCAM_AVDD_2P8_DI\n')
	print("done")
	time.sleep(1)

	#while True:

	read_data = MCUserialport.readline()
	print(read_data)
        





def command_4():
	print('###################################################  LED_R_EN / LED_R_DI TEST START  ###################################################')
	global MCUserialport
	MCUserialport.write("LED_R_EN / LED_R_DI\r")
	print('\nLED_R_EN / LED_R_DI\n')
	print("done")
	time.sleep(1)

	#while True:

	read_data = MCUserialport.readline()
	print(read_data)

	print('###################################################  ALL TEST DONE  ###################################################')








def port_check():
	global MCUserialport
	global data

	MCUserialport= serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=5)
	print('port open ')
	print('###################################################  IMPEDENCE TEST  START  ###################################################')

	out=MCUserialport.write("IMP TEST ALL\r\r")
	print('\nIMP TEST ALL\n')
	time.sleep(10)
	
	while True:

		read_data = MCUserialport.readline()
		print(read_data)
		time.sleep(2)
		data = data+read_data
		
		now = datetime.now()
		dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
		#print( dt_string)

		filepath = "/home/vvdn/Desktop/logfile/"+dt_string+".log"
		logging.basicConfig(filename=filepath, 
                    format='%(asctime)s %(message)s', 
                    filemode='wa')
		log = logging.getLogger()
		log.setLevel(logging.DEBUG)
		log.info(data)
		









		print(data[0])

		if 'done' in str(data).lower():
			print("IMpedence test done")
			print('###################################################  IMPEDENCE TEST  DONE  ###################################################')

			return data
		else:
			continue

def split_data():
	global vdd_cam_1v2
	global vdd_cam_1v8
	global vreg_bob_3p3_3p5
	global vdd_cam_2v8

	vdd_cam_1v2 = str(str(str(data).split("TP03 | |IMPEDENCE :")[1]).split("  |NEW VOLT :")[0])
	vdd_cam_1v8 = str(str(str(data).split("TP06 | |IMPEDENCE :")[1]).split("  |NEW VOLT :")[0])
	vreg_bob_3p3_3p5 = str(str(str(data).split("TP05 | |IMPEDENCE :")[1]).split("  |NEW VOLT :")[0])
	vdd_cam_2v8 = str(str(str(data).split("TP04 | |IMPEDENCE :")[1]).split("  |NEW VOLT :")[0])

def send_data():
	global vdd_cam_1v2
	global vdd_cam_1v8
	global vreg_bob_3p3_3p5
	global vdd_cam_2v8

	mydb=mysql.connector.connect(host='localhost',user='root',password='123',database='python1')
	cur=mydb.cursor()

	s="INSERT INTO  python1.impedence (vdd_cam_1v2,vdd_cam_1v8,vreg_bob_3p3_3p5,vdd_cam_2v8)"+\
	" values('{0}','{1}','{2}','{3}');".format(vdd_cam_1v2,vdd_cam_1v8,vreg_bob_3p3_3p5,vdd_cam_2v8)

	print(s)
	cur.execute(s)


	var= str(str(str(s).split(" values")[1]))
	print(var)
	a = open('impedence.txt', 'a')
	print("\n")
	a.writelines(var+'\n')
	a.close()
	print('\n')
	'''	
	mydb.commit()
	df=sql.read_sql('select * from impedence', mydb)
	df.to_excel('impedence.xls')
	'''
def create_table():
	global MCUserialport
	mydb=mysql.connector.connect(host='localhost',user='root',password='123',database='python1')
	cur=mydb.cursor()
	querry = "CREATE TABLE IF NOT EXISTS python1.impedence ("+\
		"vdd_cam_1v2 varchar(100) COLLATE utf8mb4_unicode_ci,"+\
		"vdd_cam_1v8 varchar(100) COLLATE utf8mb4_unicode_ci,"+\
		"vreg_bob_3p3_3p5 varchar(100) COLLATE utf8mb4_unicode_ci,"+\
		"vdd_cam_2v8 varchar(100) COLLATE utf8mb4_unicode_ci"+\
		") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"

	print(querry)
	cur.execute(querry)
	mydb.commit()



                                           
						

def voltage():
	global MCUserialport 
	global Resolution 
	global vol_data

	#MCUserialport= serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=5)
	#print('port open ')
	print('###################################################  VOLT TEST  START  ###################################################')


	MCUserialport.write("VOLT TEST ALL\r\r")
	print('\nVOLT TEST ALL\n')
	#time.sleep(10)
	while True:

		read_data = MCUserialport.readline()
		print(read_data)
		vol_data = vol_data + read_data
		#print(vol_data)
		
		now = datetime.now()
		dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
		#print( dt_string)

		filepath = "/home/vvdn/Desktop/logfile/"+dt_string+".log"
		logging.basicConfig(filename=filepath, 
                    format='%(asctime)s %(message)s', 
                    filemode='wa')
		log = logging.getLogger()
		log.setLevel(logging.DEBUG)
		log.info(data)
		
		if "done" in str(vol_data).lower():
			#if read_data.count("Measured") == 4:
			print("\nvoltage check == {}".format(vol_data))
			print("VOLT test done")
			#return vol_data
			break
		else:
			continue

def volt_data():
	global vol_data
	global Measured_Voltage_1
	global Measured_Voltage_2
	global Measured_Voltage_3
	global Measured_Voltage_4
	global Resolution

	Measured_Voltage_1 = str(str(str(vol_data).split("Measured Voltage : ")[1]).split("| Resolution :")[0])
	Measured_Voltage_2 = str(str(str(vol_data).split("Measured Voltage : ")[1]).split("| Resolution :")[0])
	Measured_Voltage_3 = str(str(str(vol_data).split("Measured Voltage : ")[1]).split("| Resolution :")[0])
	Measured_Voltage_4 = str(str(str(vol_data).split("Measured Voltage : ")[1]).split("| Resolution :")[0])

def volt_send():
	global MCUserialport
	global Measured_Voltage_1
	global Measured_Voltage_2
	global Measured_Voltage_3
	global Measured_Voltage_4 
	global Resolution

	mydb=mysql.connector.connect(host='localhost',user='root',password='123',database='python1')
	cur=mydb.cursor()

	s=" INSERT INTO  python1.voltage (measured_voltage_1,measured_voltage_2,measured_voltage_3,measured_voltage_4)"+\
	" values('{0}','{1}','{2}','{3}');".format(Measured_Voltage_1,Measured_Voltage_2,Measured_Voltage_3,Measured_Voltage_4)

	print(s)
	cur.execute(s)





	var= str(str(str(s).split(" ")))
	print(var)
	a = open('voltage.txt', 'a')
	print("\n")
	a.writelines(var+'\n')
	a.close()
	print('\n')
	print('###################################################  VOLTAGE TEST  DONE ###################################################')
	'''	
	mydb.commit()
	df=sql.read_sql('select * from voltage', mydb)
	df.to_excel('voltagetge.xls')
	'''
def create_table_volt():

	mydb=mysql.connector.connect(host='localhost',user='root',password='123',database='python1')
	cur=mydb.cursor()
	querry = "CREATE TABLE IF NOT EXISTS python1.voltage ("+\
		"measured_voltage_1 varchar(100) COLLATE utf8mb4_unicode_ci,"+\
		"measured_voltage_2 varchar(100) COLLATE utf8mb4_unicode_ci,"+\
		"measured_voltage_3 varchar(100) COLLATE utf8mb4_unicode_ci,"+\
		"measured_voltage_4 varchar(100) COLLATE utf8mb4_unicode_ci"+\
		") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"

	print(querry)
	cur.execute(querry)
	mydb.commit()








if __name__ == '__main__':
	
	var_data = port_check()
	print("\nFunction return = {}".format(var_data))
	
	split_data()
	create_table()
	send_data()
	
	voltage()
	volt_data()
	create_table_volt()
	volt_send()
	command_1()
	command_2()
	command_3()
	command_4()







var= str(str(str(s).split(" ")))
	print(var)
	a = open('voltage.txt', 'a')
	print("\n")
	a.writelines(var+'\n')
	a.close()
	print('\n')
	print('###################################################  VOLTAGE TEST  DONE ###################################################')
	'''	
	mydb.commit()
	df=sql.read_sql('select * from voltage', mydb)
	df.to_excel('voltagetge.xls')
	'''
def create_table_volt():

	mydb=mysql.connector.connect(host='localhost',user='root',password='123',database='python1')
	cur=mydb.cursor()
	querry = "CREATE TABLE IF NOT EXISTS python1.voltage ("+\
		"measured_voltage_1 varchar(100) COLLATE utf8mb4_unicode_ci,"+\
		"measured_voltage_2 varchar(100) COLLATE utf8mb4_unicode_ci,"+\
		"measured_voltage_3 varchar(100) COLLATE utf8mb4_unicode_ci,"+\
		"measured_voltage_4 varchar(100) COLLATE utf8mb4_unicode_ci"+\
		") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"

	print(querry)
	cur.execute(querry)
	mydb.commit()


srjgfsjdkbfjw3egfbcHegfhsDvbfed
efkghsfdvfgwjh
ewfkkkgsdhfe
