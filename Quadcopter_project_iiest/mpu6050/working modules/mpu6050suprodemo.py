import pygame,sys
from pygame.locals import *
import smbus
import math
import time

pygame.init()

error=4.5#error to be seen and incorporated

WINDOW=pygame.display.set_mode((400,300),0,32)
pygame.display.set_caption('MPU 6050 demo')

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
WINDOW.fill(WHITE)

power_mgmt_1=0x6b
power_mgmt_2=0x6c
gyro_scale=131
accel_scale=16384.0
address=0x68

def read_all():
    raw_gyro_data=bus.read_i2c_block_data(address,0x43,6)
    raw_accel_data=bus.read_i2c_block_data(address,0x3b,6)
    gyro_scaled_x=twos_compliment((raw_gyro_data[0]<<8)+raw_gyro_data[1])/(-420)
    gyro_scaled_y=twos_compliment((raw_gyro_data[2]<<8)+raw_gyro_data[3])/(-180)
    gyro_scaled_z=twos_compliment((raw_gyro_data[4]<<8)+raw_gyro_data[5])/gyro_scale
    accel_scaled_x=twos_compliment((raw_accel_data[0]<<8)+raw_accel_data[1])/accel_scale
    accel_scaled_y=twos_compliment((raw_accel_data[2]<<8)+raw_accel_data[3])/accel_scale
    accel_scaled_z=twos_compliment((raw_accel_data[4]<<8)+raw_accel_data[5])/accel_scale
    return(gyro_scaled_x,gyro_scaled_y,gyro_scaled_z,accel_scaled_x,accel_scaled_y,accel_scaled_z)

def twos_compliment(val):
    if (val>=0x8000):
        return -((65535-val)+1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians=math.atan2(x,dist(y,z))
    return math.degrees(radians)

def get_x_rotation(x,y,z):
    radians=math.atan2(y,dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for Revision 1 boards

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

now = time.time()

k = 0.85
k1 = 1 - k

dtime = 0

(gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all()

last_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
last_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)





while 1:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    
    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all()
    
    rotation_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    rotation_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

    dtime=time.time()-now

    now=time.time()
    
    last_x=(k*(last_x+(gyro_scaled_x*dtime)))+(k1*rotation_x)
    last_y=(k*(last_y+(gyro_scaled_x*dtime)))+(k1*rotation_y)

    print ((last_x), (last_y))
    
    delta_y=math.radians(last_y-error)
    z=2*int(last_x)
    if z<0:
        z=-z
        COLOR=RED
    else:
        COLOR=BLUE
    if z==0:
        z=1
    x1=200-(100*math.cos(delta_y))
    y1=150+(100*math.sin(delta_y))
    x2=200+(100*math.cos(delta_y))
    y2=150-(100*math.sin(delta_y))
    WINDOW.fill(WHITE)
    pygame.draw.line(WINDOW,COLOR,(x1,y1),(x2,y2),z)
    pygame.display.update()
            




































