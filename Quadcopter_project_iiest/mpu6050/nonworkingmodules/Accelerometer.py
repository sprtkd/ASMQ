import smbus
import math
import time
power_mgmt_1=0x6b
power_mgmt_2=0x6c
def read_byte(adr):
    return bus.read_byte_data(address,adr)
def read_word(adr):
    high=bus.read_byte_data(address,adr)
    low=bus.read_byte_data(address,adr+1)
    val=(high<<8)+low
    return val
def read_word_2c(adr):
    val=read_word(adr)
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
bus=smbus.SMBus(1)
address=0x68
Xangle=0
Yangle=0
Zangle=0
accoffx=read_word_2c(0x3b)
accoffy=read_word_2c(0x3d)
goffx=read_word_2c(0x43)
goffy=read_word_2c(0x45)
goffz=read_word_2c(0x47)
t=time.time()
t1=time.time()
for i in range (1,100):
    td=time.time()-t
    diff=time.time()-t1
    t=time.time()
    gyro_xout=(goffx-read_word_2c(0x43))/131.0
    gyro_yout=(goffy-read_word_2c(0x45))/131.0
    gyro_zout=(goffz-read_word_2c(0x47))/131.0
    accel_xout=(read_word_2c(0x3b)-accoffx)/16384.0
    accel_yout=(read_word_2c(0x3d)-accoffy)/16384.0
    accel_zout=(read_word_2c(0x3f))/16384.0
    Xangle+=(round(gyro_xout))*td
    Yangle+=(round(gyro_yout))*td
    Zangle+=(round(gyro_zout))*td
    lx=round(accel_xout-(math.sin(math.radians(Xangle))),1)
    ly=round(accel_yout-(math.sin(math.radians(Yangle))),1)
    X=get_x_rotation(accel_xout,accel_yout,accel_zout)
    Y=get_y_rotation(accel_xout,accel_yout,accel_zout)
##  print ("Xangle",X)
##  print ("Angle From Gyro",Xangle)
#    print ("Gyro",gyro_xout)
    Xang=0.9*Xangle+0.1*X
#    print ("Xangle",Xang)
 #   print ("***********************")
##    print ("Yangle",Y)
    print ("Linear X",(lx*9.81),"m/s2")
#    print ("Linear Y",(ly*9.81),"m/s2")
##    print ("AccX",accel_xout)
##    print ("AccY",accel_yout)    
##    print ("Xangle",Xangle)
##    print ("Yangle",Yangle)
##    print ("Zangle",Zangle)
##    print ("diff",diff)
##    print ("Zacc",accel_zout)
    
