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
bus=smbus.SMBus(1)
address=0x68
xangle=0
yangle=0
zangle=0
##goffx=(read_word_2c(0x43))/131.0
##goffy=(read_word_2c(0x45))/131.0
goffz=(read_word_2c(0x47))/131.0
t=time.time()
t1=time.time()
for i in range (0,5000):
    td=time.time()-t
    t=time.time()
    difference=t-t1
##    gyro_xout=(read_word_2c(0x43))/131.0
##    gyro_yout=(read_word_2c(0x45))/131.0
    gyro_zout=(read_word_2c(0x47))/131.0
##    xangle+=(round(goffx-gyro_xout))*td
##    yangle+=(round(goffy-gyro_yout))*td
    zangle+=(round(goffz-gyro_zout))*(round(td,2))
##    z=round(zangle-(difference/0.9))
##    print ("Xangle",xangle)
##    print ("Yangle",yangle)
    print ("Zangle",zangle)
##    print ("Gyro_Zout",gyro_zout)
##    print ("time",difference)
##    print ("***********************")
    
