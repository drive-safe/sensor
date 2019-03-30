import smbus
from time import sleep
import math

PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
Device_Address = 0x68

def MPU_Init():
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
		high = bus.read_byte_data(Device_Address, addr)
		low = bus.read_byte_data(Device_Address, addr+1
		)
		value = ((high << 8) | low)

		if(value > 32768):
				value = value - 65536
		return[] value


bus = smbus.SMBus(1)
   

MPU_Init()

print (" Reading Data of Accelerometer")

while True:
	
	acc_x = read_raw_data(ACCEL_XOUT_H)
	acc_y = read_raw_data(ACCEL_YOUT_H)
	acc_z = read_raw_data(ACCEL_ZOUT_H)

	Ax = acc_x/16384.0
	Ay = acc_y/16384.0
	Az = acc_z/16384.0
	sumXY = math.sqrt(Ax*Ax + Ay*Ay)
	print ("Ax=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az, "sumXY=%.2f g" %sumXY) 	
	sleep(1)
