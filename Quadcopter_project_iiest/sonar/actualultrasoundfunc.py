#libray import------
import RPi.GPIO as GPIO
import time

#libray import------
#for help visit http://randomnerdtutorials.com/complete-guide-for-ultrasonic-sensor-hc-sr04/

#pins----
sonarTrigPin=32
sonarEchoPin=31
#pins----

#setup---
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sonarTrigPin,GPIO.OUT)
GPIO.setup(sonarEchoPin,GPIO.IN)
#setup----

#globals-----
sonarHeightOffset=12 #in cm for calibration of quad height for zero correction
quadHeight=0 #in cm
#globals-----

#function----

def updateSonar():
    global sonarHeightOffset
    global quadHeight

    absurdReadingHt=400#in cm

    
    GPIO.output(sonarTrigPin,False)
    time.sleep(0.000005)#5 microsecond
    GPIO.output(sonarTrigPin,True)
    time.sleep(0.00001)#10 microseconds
    GPIO.output(sonarTrigPin,False)
    while GPIO.input(sonarEchoPin)==0:
        t1=time.time()
    while GPIO.input(sonarEchoPin)==1:
        t2=time.time()
    t=t2-t1
    distance=t*17150
    #distance in cm
    if distance>=absurdReadingHt:
        print("height out of range..Not updating")
    else:
        quadHeight=distance-sonarHeightOffset

    #update complete....

#example---
while 1:
    updateSonar()
    print ("Distance in cm",quadHeight)



    
    
    
