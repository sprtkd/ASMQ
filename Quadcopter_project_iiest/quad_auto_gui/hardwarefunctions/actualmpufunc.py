#include libraries-----
import smbus
import math
import time
#include libraries-----



#mpu-init-----
def mpuinit():
    global now
    global last_x
    global last_y
    global angvelerrorz
    power_mgmt_1 = 0x6b
    power_mgmt_2 = 0x6c
    bus.write_byte_data(address, power_mgmt_1, 0)
    now = time.time()
    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all()

    last_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    last_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    angvelerrorz=gyro_scaled_z
#mpu-init-----

#globals----
bus = smbus.SMBus(1)
now = time.time()
angvelerrorz=0.0
x_error=2.0
y_error=5.0
angle_x=0.0
angle_y=0.0
linacc_x=0.0
linacc_y=0.0
angularVelocity_z=0.0
last_x=0.0
last_y=0.0
gyro_scale = 131.0
accel_scale = 16384.0
address = 0x68  # This is the address value read via the i2cdetect command
#globals----



#accesory functions-----
def read_all():
    raw_gyro_data = bus.read_i2c_block_data(address, 0x43, 6)
    raw_accel_data = bus.read_i2c_block_data(address, 0x3b, 6)

    gyro_scaled_x = twos_compliment((raw_gyro_data[0] << 8) + raw_gyro_data[1]) / gyro_scale
    gyro_scaled_y = twos_compliment((raw_gyro_data[2] << 8) + raw_gyro_data[3]) / gyro_scale
    gyro_scaled_z = twos_compliment((raw_gyro_data[4] << 8) + raw_gyro_data[5]) / gyro_scale

    accel_scaled_x = twos_compliment((raw_accel_data[0] << 8) + raw_accel_data[1]) / accel_scale
    accel_scaled_y = twos_compliment((raw_accel_data[2] << 8) + raw_accel_data[3]) / accel_scale
    accel_scaled_z = twos_compliment((raw_accel_data[4] << 8) + raw_accel_data[5]) / accel_scale

    return (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z)
    
def twos_compliment(val):
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def calibrateMpu():
    global angvelerrorz
    global x_error
    global y_error
    global last_x
    global last_y
    print("Keep your quad straight and still.\nPress enter to continue....")
    raw_input()
    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all()
    x_error = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    y_error = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    mpuinit()
    print("Calibration complete..")
    
#accesory functions-----
#function

def updateMpu6050():
    global now
    global angle_x
    global angle_y
    global linacc_x
    global linacc_y
    global angularVelocity_z
    global last_x
    global last_y


    k = 0.85
    k1 = 1 - k
    dtime = 0
    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all()
    
    rotation_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    rotation_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

    dtime=time.time()-now
    
    now=time.time()
    
    last_x=(k*(last_x+(gyro_scaled_x*dtime)))+(k1*rotation_x)
    last_y=(k*(last_y+(gyro_scaled_x*dtime)))+(k1*rotation_y)


    angle_x=-(last_x-x_error)
    angle_y=-(last_y-y_error)
    
    linacc_x=(accel_scaled_x-(math.sin(math.radians(angle_y))))*9.81#m/s^2
    linacc_y=(accel_scaled_y+(math.sin(math.radians(angle_x))))*9.81#m/s^2
    #special manipulation using no logic---
    
    
    
    angularVelocity_z=-(gyro_scaled_z-angvelerrorz)







#example----------------
mpuinit()
calibrateMpu()
while 1:
    updateMpu6050()
    print (round(angle_x),round(angle_y),round(linacc_x),round(linacc_y),round(angularVelocity_z))
    
    
    
    
    





    
    
