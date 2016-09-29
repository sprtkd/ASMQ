import smbus
import math
import time
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
    return radians
def get_x_rotation(x,y,z):
    radians=math.atan2(y,dist(x,z))
    return radians
bus=smbus.SMBus(1)
bus.write_byte_data(address,power_mgmt_1,0)
now=time.time()
k=0.98
k1=1-k
time_diff=0.01
(gyro_scaled_x,gyro_scaled_y,gyro_scaled_z,accel_scaled_x,accel_scaled_y,accel_scaled_z)=read_all()
last_x=get_x_rotation(accel_scaled_x,accel_scaled_y,accel_scaled_z)
last_y=get_y_rotation(accel_scaled_x,accel_scaled_y,accel_scaled_z)
gyro_offset_x=gyro_scaled_x
gyro_offset_y=gyro_scaled_y
gyro_total_x=(last_x)-(gyro_offset_x)
gyro_total_y=(last_y)-(gyro_offset_y)
for i in range(0,5):
    time.sleep(time_diff-0.005)
    (gyro_scaled_x,gyro_scaled_y,gyro_scaled_z,accel_scaled_x,accel_scaled_y,accel_scaled_z)=read_all()
    gyro_scaled_x-=gyro_offset_x
    gyro_scaled_y-=gyro_offset_y
    gyro_x_delta=(gyro_scaled_x*time_diff)
    gyro_y_delta=(gyro_scaled_y*time_diff)
    gyro_total_x+=gyro_x_delta
    gyro_total_y+=gyro_y_delta
    rotation_x=get_x_rotation(accel_scaled_x,accel_scaled_y,accel_scaled_z)
    rotation_y=get_y_rotation(accel_scaled_x,accel_scaled_y,accel_scaled_z)
    last_x=k*(last_x+gyro_x_delta)+(k1*rotation_x)
    last_y=k*(last_y+gyro_y_delta)+(k1*rotation_y)
##    if (i==0):
##        x=math.degrees(last_x)
##        y=math.degrees(last_y)
    print("Rotation_X:",math.degrees(last_x))
    print("Rotation_Y:",math.degrees(last_y))
    
    



    
