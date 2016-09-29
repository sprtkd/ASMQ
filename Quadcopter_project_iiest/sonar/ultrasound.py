import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BOARD)
trig=16
echo=18
gpio.setup(trig,gpio.OUT)
gpio.setup(echo,gpio.IN)
for i in range (0,2):
    gpio.output(trig,False)
    time.sleep(2)
    gpio.output(trig,True)
    time.sleep(0.00001)#should be 0.000005
    gpio.output(trig,False)
    while gpio.input(echo)==0:
        t1=time.time()
    while gpio.input(echo)==1:
        t2=time.time()
    t=t2-t1
    distance=t*17150
    print ("Distance in cm",distance)
