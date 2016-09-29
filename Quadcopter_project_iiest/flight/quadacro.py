#to control quadcopter from raspberry pi 
#acro mode without sensor data
#QuadDarshan.......an initiative of Robodarshan IIEST,Shibpur

print("\n\nQuadcopter *+* Configuration")
print("For Raspberry pi 2 model B")
print("\n***WARNING***\nThis is acro mode.\nYour quad may stall any time")


#pins
esc_pinH=11  #head
esc_pinL=13  #left
esc_pinR=15  #right
esc_pinT=16  #tail

#multipliers for calibration
#depends on resolution of escs...Defaults are 0.5
rollmultiplier=0.5  #give values between 0 and 1..if values greater than 1 is given then wobbling will occur 
pitchmultiplier=0.5  #give values between 0 and 1..if values greater than 1 is given then wobbling will occur
yawmultiplier=0.5  #give values between 0 and 1..if values greater than 1 is given then wobbling will occur



print("\nFollowing GPIO.BOARD config")
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

print("Make sure your quad does not fly...\nAnd battery is disconnected from escs")
print('***Press ENTER to continue')
res = raw_input()

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(esc_pinH, GPIO.OUT)
GPIO.setup(esc_pinL, GPIO.OUT)
GPIO.setup(esc_pinR, GPIO.OUT)
GPIO.setup(esc_pinT, GPIO.OUT)


motorH = GPIO.PWM(esc_pinH,50)#50 hz
motorL = GPIO.PWM(esc_pinL,50)#50 hz
motorR = GPIO.PWM(esc_pinR,50)#50 hz
motorT = GPIO.PWM(esc_pinT,50)#50 hz





motorH.start(10) #start with full throttle to calibrate
motorL.start(10) #start with full throttle to calibrate
motorR.start(10) #start with full throttle to calibrate
motorT.start(10) #start with full throttle to calibrate


print("Do you want to calibrate(y/n):")
res = raw_input()


if res == 'y':
        print("***Connect Battery & wait for music to stop..Then press enter")
        res = raw_input()
        motorH.ChangeDutyCycle(5) #zero throttle
        motorL.ChangeDutyCycle(5) #zero throttle
        motorR.ChangeDutyCycle(5) #zero throttle
        motorT.ChangeDutyCycle(5) #zero throttle
        print('***Calibration Completed...Press ENTER to start')
        res = raw_input()
        
else:
        motorH.ChangeDutyCycle(5) #zero throttle
        motorL.ChangeDutyCycle(5) #zero throttle
        motorR.ChangeDutyCycle(5) #zero throttle
        motorT.ChangeDutyCycle(5) #zero throttle
        print("***Connect Battery & wait for music to stop..Then press enter")
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
                
                
                
                
        dcH = 5+(valH*5/100)
        dcL = 5+(valL*5/100)
        dcR = 5+(valR*5/100)
        dcT = 5+(valT*5/100)    
        
        motorH.ChangeDutyCycle(dcH)
        motorL.ChangeDutyCycle(dcL)
        motorR.ChangeDutyCycle(dcR)
        motorT.ChangeDutyCycle(dcT)
        checklessgreater=0
        return


print ("\nEnter option \n t to change throttle")
print ("\n c to calibrate")
print ("\nto change direction....\n f for front \n l for left\n r for right\n b for back")
print ("\n a to turn counter clockwise\n d to turn clockwise\n g to get back stability")

print ("\n\n And q to quit\n\n")
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
                
                
                if res == 'q':
                    if throttle > 0 :
                        print("Cannot quit..Please land!!!")
                    else:
                        cycling = False
                        

                
                
finally:
        motorH.ChangeDutyCycle(5)
        motorL.ChangeDutyCycle(5)
        motorR.ChangeDutyCycle(5)
        motorT.ChangeDutyCycle(5)
        motorH.stop()
        motorL.stop()
        motorR.stop()
        motorT.stop()

print('***Press ENTER to quit')
res = raw_input()
motorH.stop()
motorL.stop()
motorR.stop()
motorT.stop()
GPIO.cleanup()
exit()







