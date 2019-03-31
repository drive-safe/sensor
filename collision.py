from bluetooth import *
import smbus
import time
import math
import threading
import RPi.GPIO as GPIO

PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
Device_Address = 0x68

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)

server_sock=BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service(server_sock, "SAFE_DRIVE", service_id= uuid, service_classes = [uuid, SERIAL_PORT_CLASS], profiles = [SERIAL_PORT_PROFILE], protocols = [OBEX_UUID])

collided = False
time1 = time.time()
Ax = 0.0
Ay = 0.0
Az = 0.0

GPIO.output(26, GPIO.LOW)

def MPU_Init():
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
    bus.write_byte_data(Device_Address, CONFIG, 0)

    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

    time1 = time.time()

def read_raw_data(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    value = ((high << 8) | low)
    if(value > 32768):
        value = value - 65536
    return value


def impact():
    time1 = time.time()
    oldx = Ax
    oldy = Ay
    oldz = Az
    
    newx = read_raw_data(ACCEL_XOUT_H)/16384.0
    newy = read_raw_data(ACCEL_YOUT_H)/16384.0
    newz = read_raw_data(ACCEL_ZOUT_H)/16384.0

    deltx = newx - oldx
    delty = newy - oldy
    deltz = newz - oldz

    magnitude = math.sqrt(deltx**2 + delty**2 + deltz**2)
    #print(magnitude)

    if(magnitude > 3.5):
        print("High magnitude sensed")
        if(delty > 3):
            print(delty)
            print("Forward collision sensed")
            GPIO.output(26, GPIO.HIGH)
            return 1
        
        if(abs(deltx) > 3):
            print(abs(deltx))
            print("Sideways collision sensed")
            GPIO.output(26, GPIO.HIGH)
            return 1


bus = smbus.SMBus(1)
   

MPU_Init()

connected = False

if(not connected):
    print ("Waiting for connection on RFCOMM channel")
    client_sock, client_info = server_sock.accept()
    connected=True
    data = client_sock.recv(1024)

print (" Reading Data of Accelerometer")
while True:
    GPIO.output(26, GPIO.LOW)
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)

    Ax = acc_x/16384.0
    Ay = acc_y/16384.0
    Az = acc_z/16384.0
    collision = impact()
    if(collision):
        if(connected):
            client_sock.send("AccidentDetected")
        time.sleep(5)
    

