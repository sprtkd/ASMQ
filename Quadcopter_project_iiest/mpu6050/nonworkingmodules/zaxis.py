import pygame,sys
from pygame.locals import *
import smbus
import math
import time
zangle=0
pygame.init()
power_mgmt_1=0x6b
power_mgmt_2=0x6c
WINDOW=pygame.display.set_mode((400,300),0,32)
pygame.display.set_caption('MPU 6050 demo')
BLACK=(0,0,0)
WHITE=(255,255,255)
WINDOW.fill(WHITE)
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
bus.write_byte_data(address,power_mgmt_1,0)
t=time.time()
t1=time.time()
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        gyro_zout=read_word_2c(0x47)
        td=time.time()-t
        t=time.time()
        diff=t-t1
        zangle+=(gyro_zout*td)
        z=round(zangle-(diff/9))
        print ("ZAngle",z)
        zr=math.radians(z)
        x1=150+(100*math.sin(zr))
        y1=200+(100*math.cos(zr))
        x2=150-(100*math.sin(zr))
        y2=200-(100*math.cos(zr))
        WINDOW.fill(WHITE)
        pygame.draw.line(WINDOW,BLACK,(x1,y1),(x2,y2),1)
        pygame.display.update()
