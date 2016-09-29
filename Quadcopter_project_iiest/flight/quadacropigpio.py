#to control quadcopter from raspberry pi 
#acro mode without sensor data
#QuadDarshan.......an initiative of Robodarshan IIEST,Shibpur

# Requires the pigpio daemon to be running
#
# sudo pigpiod
print("\nMake sure your pigpio daemon is running..\ni.e. sudo pigpiod")
print('\n***Press ENTER...')
res = raw_input()
print("\n\nQuadcopter *+* Configuration")
print("For Raspberry pi 2 model B")
print("\n***WARNING***\nThis is acro mode.\nYour quad may stall any time")


import pigpio
import RPi.GPIO as GPIO
import time


#pins
esc_pinH=17  #head Board 11
esc_pinL=27  #left Board 13
esc_pinR=22  #right Board 15
esc_pinT=23  #tail Board 16

relaypin=29 #relay using board config from rpi.gpio

#multipliers for calibration
#depends on resolution of escs...Defaults are 0.5
rollmultiplier=0.5  #give values between 0 and 1..if values greater than 1 is given then wobbling will occur 
pitchmultiplier=0.5  #give values between 0 and 1..if values greater than 1 is given then wobbling will occur
yawmultiplier=0.5  #give values between 0 and 1..if values greater than 1 is given then wobbling will occur

GPIO.setmode(GPIO.BOARD)

GPIO.setup(relaypin,GPIO.OUT)
GPIO.output(relaypin,False)

print("\nFor Relay using pin from BOARD CONFIG:")
print(relaypin)
print("\nFollowing GPIO.BCM config")
print("Please ensure the following:\n\n")
print("Head motor connected to pin:")
print(esc_pinH)
print("Left motor connected to pin:")
print(esc_pinL)
print("Right motor connected to pin:")
print(esc_pinR)
print("Tail motor connected to pin:")
print(esc_pinT)
print("GROUND pins connected too...\n")
print('Press ENTER to continue......')
res = raw_input()

print("Make sure your quad does not fly...\nAnd Relay light is off")
print('***Press ENTER to continue')
res = raw_input()


pi = pigpio.pi() # Connect to local Pi.

pi.set_mode(esc_pinH, pigpio.OUTPUT)
pi.set_mode(esc_pinL, pigpio.OUTPUT)
pi.set_mode(esc_pinR, pigpio.OUTPUT)
pi.set_mode(esc_pinT, pigpio.OUTPUT)


pi.set_servo_pulsewidth(esc_pinH, 2000)#start with full throttle to calibrate
pi.set_servo_pulsewidth(esc_pinL, 2000)#start with full throttle to calibrate
pi.set_servo_pulsewidth(esc_pinR, 2000)#start with full throttle to calibrate
pi.set_servo_pulsewidth(esc_pinT, 2000)#start with full throttle to calibrate






print("Do you want to calibrate(y/n):")
res = raw_input()


if res == 'y':
        GPIO.output(relaypin,True)
        print("\n***Calibrating...Escs turned on...")
        print("***Wait for music to stop..Then press enter")
        res = raw_input()
        pi.set_servo_pulsewidth(esc_pinH, 1000)#zero throttle
        pi.set_servo_pulsewidth(esc_pinL, 1000)#zero throttle
        pi.set_servo_pulsewidth(esc_pinR, 1000)#zero throttle
        pi.set_servo_pulsewidth(esc_pinT, 1000)#zero throttle
        print('***Calibration Completed...Press ENTER to start')
        res = raw_input()
        
else:
        pi.set_servo_pulsewidth(esc_pinH, 1000)#zero throttle
        pi.set_servo_pulsewidth(esc_pinL, 1000)#zero throttle
        pi.set_servo_pulsewidth(esc_pinR, 1000)#zero throttle
        pi.set_servo_pulsewidth(esc_pinT, 1000)#zero throttle
        GPIO.output(relaypin,True)
        print("\nEscs turned on...")
        print("***Not Calibrating\nWait for music to stop..Then press enter")
        res = raw_input()
        print('***Press ENTER to start')
        res = raw_input()


#throttle value will change during runtime...
throttle=0


#max throttle is 100 for each motor and min is zero.. Any value outside this can cause trouble
#for getting values
getval=0

#stabilization amounts:These will change until quad is stabilized during runtime....Can be positive or negative
rollstabamount=0
pitchstabamount=0
yawstabamount=0  

#offsets:These will make quad move.These will change during runtime...Can be positive or negative
#These are like joystick values..
rolloffset=0
pitchoffset=0
yawoffset=0  


def changethrottle( pitchoffsetloc=pitchstabamount,rolloffsetloc=rollstabamount,yawoffsetloc=yawstabamount ):
        "This changes throttle values of all motors"
        
        
        #variables ending with loc are local variables(i couldn't find better names :-[  )
        valH = throttle + (pitchoffsetloc*pitchmultiplier) + (yawoffsetloc*yawmultiplier)
        valR = throttle + (rolloffsetloc*rollmultiplier) - (yawoffsetloc*yawmultiplier)
        valT = throttle - (pitchoffsetloc*pitchmultiplier) + (yawoffsetloc*yawmultiplier)
        valL = throttle - (rolloffsetloc*rollmultiplier) - (yawoffsetloc*yawmultiplier)
        
        #initialising
        checklessgreater=0
        xvalH=0
        xvalL=0
        xvalR=0
        xvalT=0
        xgreatest=0
        
        if valH>100 :
                xvalH=valH-100
                checklessgreater=1
        if valT>100 :
                xvalT=valT-100
                checklessgreater=1
        if valL>100 :
                xvalL=valL-100
                checklessgreater=1
        if valR>100 :
                xvalR=valR-100
                checklessgreater=1
        
        
        
        if checklessgreater==1 :
                xgreatest=xvalH
                if xgreatest<xvalL :
                        xgreatest=xvalL
                if xgreatest<xvalR :
                        xgreatest=xvalR
                if xgreatest<xvalT :
                        xgreatest=xvalT
                valH-=xgreatest
                valL-=xgreatest
                valR-=xgreatest
                valT-=xgreatest
                
        #initialising
        checklessgreater=0
        xvalH=0
        xvalL=0
        xvalR=0
        xvalT=0
        xgreatest=0
        
        if valH<0 :
                xvalH=0-valH
                checklessgreater=2
        if valT<0 :
                xvalT=0-valT
                checklessgreater=2
        if valL<0 :
                xvalL=0-valL
                checklessgreater=2
        if valR<0 :
                xvalR=0-valR
                checklessgreater=2
                
        if checklessgreater==2 :
                xgreatest=xvalH
                if xgreatest<xvalL :
                        xgreatest=xvalL
                if xgreatest<xvalR :
                        xgreatest=xvalR
                if xgreatest<xvalT :
                        xgreatest=xvalT
                valH+=xgreatest
                valL+=xgreatest
                valR+=xgreatest
                valT+=xgreatest
                
                
                
                
        pwidthH = 1000+(valH*1000/100)
        pwidthL = 1000+(valL*1000/100)
        pwidthR = 1000+(valR*1000/100)
        pwidthT = 1000+(valT*1000/100)

        
        


        print('',pwidthH,'')
        print(pwidthL,pwidthR)
        print('',pwidthT,'')



        pi.set_servo_pulsewidth(esc_pinH, pwidthH)
        pi.set_servo_pulsewidth(esc_pinL, pwidthL)
        pi.set_servo_pulsewidth(esc_pinR, pwidthR)
        pi.set_servo_pulsewidth(esc_pinT, pwidthT)
        
        
        
        return


print ("\nEnter option \n t to change throttle")
print ("\n c to calibrate")
print ("\nto change direction....\n f for front \n l for left\n r for right\n b for back")
print ("\n a to turn counter clockwise\n d to turn clockwise\n g to get back stability")

print ("\n\n e for emergency stop***\n And q to quit\n\n")
cycling = True
try:
        while cycling:
                
                print('Enter Option: ')
                res = raw_input()
                
                if res == 't':
                        throttle = float(input("Enter percentage(0-100): "))
                        print "throttle set to",throttle
                        changethrottle()
                if res == 'c':
                        cycling2 = True
                        changethrottle()
                        print("Quad stabilized at first")
                        print ("\nEnter option to indicate the direction of tilt\n f for front \n l for left\n r for right\n b for back")
                        print ("\n a if turning counter clockwise\n d if turning clockwise\n q to quit calibration")
                                
                        while cycling2:
                                print("Enter option :")
                                res2 = raw_input()
                                if res2 == 'f':
                                        pitchstabamount+=1
                                        changethrottle()
                                        print("Quad is tilted back.")
                                if res2 == 'l':
                                        rollstabamount-=1
                                        changethrottle()
                                        print("Quad is tilted right.")
                                if res2 == 'r':
                                        rollstabamount+=1
                                        changethrottle()
                                        print("Quad is tilted left.")
                                if res2 == 'b':
                                        pitchstabamount-=1
                                        changethrottle()
                                        print("Quad is tilted front.")
                                if res2 == 'a':
                                        yawstabamount+=1
                                        changethrottle()
                                        print("Quad is rotated clockwise.")
                                if res2 == 'd':
                                        yawstabamount-=1
                                        changethrottle()
                                        print("Quad is rotated counterclockwise.")
                                if res2 == 'q':
                                        cycling2 = False
                                        print("Printing Stability amounts...\n")
                                        print "pitchstabamount=" ,pitchstabamount 
                                        print "rollstabamount=",rollstabamount
                                        print "yawstabamount=",yawstabamount
                                        print("Note them down.Press enter to continue..")
                                        res3 = raw_input()
                if res == 'f':
                        getval = float(input("Enter level(1-5): "))
                        pitchoffset=pitchstabamount-getval
                        changethrottle(pitchoffsetloc=pitchoffset)
                        print("Quad moving forward")
                if res == 'l':
                        getval = float(input("Enter level(1-5): "))
                        rolloffset=rollstabamount+getval
                        changethrottle(rolloffsetloc=rolloffset)
                        print("Quad moving left")
                if res == 'r':
                        getval = float(input("Enter level(1-5): "))
                        rolloffset=rollstabamount-getval
                        changethrottle(rolloffsetloc=rolloffset)
                        print("Quad moving right")
                if res == 'b':
                        getval = float(input("Enter level(1-5): "))
                        pitchoffset=pitchstabamount+getval
                        changethrottle(pitchoffsetloc=pitchoffset)
                        print("Quad moving back")
                
                if res == 'a':
                        getval = float(input("Enter level(1-5): "))
                        yawoffset=yawstabamount-getval
                        changethrottle(yawoffsetloc=yawoffset)
                        print("Quad rotating counterclockwise")
                if res == 'd':
                        getval = float(input("Enter level(1-5): "))
                        yawoffset=yawstabamount+getval
                        changethrottle(yawoffsetloc=yawoffset)
                        print("Quad rotating clockwise")
                
                if res == 'g':
                        changethrottle()
                        print("Quad stabilized")
                
                if res == 'e':
                        print("Emergency stop conditioon!!!!")
                        GPIO.output(relaypin,False)
                        throttle=0
                        print("Enter q to quit")
                if res == 'q':
                    if throttle > 0 :
                        print("Cannot quit..Please land!!!")
                    else:
                        cycling = False
                        

                
                
finally:
        pi.set_servo_pulsewidth(esc_pinH, 1000)#zero throttle
        pi.set_servo_pulsewidth(esc_pinL, 1000)#zero throttle
        pi.set_servo_pulsewidth(esc_pinR, 1000)#zero throttle
        pi.set_servo_pulsewidth(esc_pinT, 1000)#zero throttle

print('***Press ENTER to quit')
res = raw_input()
#cleanup
GPIO.output(relaypin,False)
print("\nEscs turned off...")
GPIO.cleanup()
pi.set_mode(esc_pinH, pigpio.INPUT)
pi.set_mode(esc_pinL, pigpio.INPUT)
pi.set_mode(esc_pinR, pigpio.INPUT)
pi.set_mode(esc_pinT, pigpio.INPUT)
#disconnect
pi.stop()

exit()







