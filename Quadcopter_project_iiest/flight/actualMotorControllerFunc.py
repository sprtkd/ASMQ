#importing libraries-----
import pigpio

#importing libraries-----


#pins-----
esc_pinH=17  #head Board 11
esc_pinL=27  #left Board 13
esc_pinR=22  #right Board 15
esc_pinT=23  #tail Board 16
#pins-----

#globals-----
#these are outputs of pid function

actualOutputThrottle=0#should be in range 0 to 100
actualOutputRoll=0#should be in range -100 to 100 so that actualOutputRoll*rollmultiplier lies within -50 to 50
actualOutputPitch=0#should be in range -100 to 100 so that actualOutputPitch*pitchmultiplier lies within -50 to 50
actualOutputYaw=0#should be in range -100 to 100 so that actualOutputYaw*yawmultiplier lies within -50 to 50
#globals-----


#setup-----
pi = pigpio.pi() # Connect to local Pi.
pi.set_mode(esc_pinH, pigpio.OUTPUT)
pi.set_mode(esc_pinL, pigpio.OUTPUT)
pi.set_mode(esc_pinR, pigpio.OUTPUT)
pi.set_mode(esc_pinT, pigpio.OUTPUT)
#after this turn on relay
pi.set_servo_pulsewidth(esc_pinH, 1000)#zero throttle
pi.set_servo_pulsewidth(esc_pinL, 1000)#zero throttle
pi.set_servo_pulsewidth(esc_pinR, 1000)#zero throttle
pi.set_servo_pulsewidth(esc_pinT, 1000)#zero throttle
#setup-----

#functions----

#function to reset all sliders----
def resetAllYawPitchRoll():
    global actualOutputRoll
    global actualOutputPitch
    global actualOutputYaw
    actualOutputRoll=0
    actualOutputPitch=0
    actualOutputYaw=0


#function to reset all sliders----

#actual function-----
def changeAllMotorsThrottleFunc():
    
    #multipliers for calibration
    #depends on resolution of escs...Defaults are 0.5
    rollmultiplier=0.5  #give values between 0 and 1..if values greater than 1 is given then wobbling will occur 
    pitchmultiplier=0.5  #give values between 0 and 1..if values greater than 1 is given then wobbling will occur
    yawmultiplier=0.5  #give values between 0 and 1..if values greater than 1 is given then wobbling will occur

    #checking for throttle =0 to stop all motors
    if actualOutputThrottle==0:
        resetAllYawPitchRoll()

    
    valH = actualOutputThrottle - (actualOutputPitch*pitchmultiplier) - (actualOutputYaw*yawmultiplier)
    valR = actualOutputThrottle - (actualOutputRoll*rollmultiplier) +(actualOutputYaw*yawmultiplier)
    valT = actualOutputThrottle + (actualOutputPitch*pitchmultiplier) - (actualOutputYaw*yawmultiplier)
    valL = actualOutputThrottle + (actualOutputRoll*rollmultiplier) + (actualOutputYaw*yawmultiplier)


    #checking for values less or greater than 0 and 100    
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

    #these should lie within 1000 and 2000
    pwidthH = 1000+(valH*1000/100)
    pwidthL = 1000+(valL*1000/100)
    pwidthR = 1000+(valR*1000/100)
    pwidthT = 1000+(valT*1000/100)


    
        

    #comment out these lines if you dont want to see######
    print("Thease are actual outputs for motors")   #
    print " ",pwidthH                               #
    print pwidthL,pwidthR                           #
    print " ",pwidthT                               #
    #comment out these lines if you dont want to see######

    
    pi.set_servo_pulsewidth(esc_pinH, pwidthH)    
    pi.set_servo_pulsewidth(esc_pinL, pwidthL)
    pi.set_servo_pulsewidth(esc_pinR, pwidthR)
    pi.set_servo_pulsewidth(esc_pinT, pwidthT)
        
#actual function-----



#example----
cycling = True
print ("\nEnter option \n t to change throttle")
print ("\n r for roll \n p for pitch\n y for yaw")
print ("\n g to get back stability")
print ("\n\nAnd q to quit\n\n")
while cycling:
    changeAllMotorsThrottleFunc()
    
    print('Enter Option: ')
    res = raw_input()
                
    if res == 't':
        actualOutputThrottle = float(input("Enter percentage(0-100): "))
        print "throttle set to",actualOutputThrottle

    elif res == 'r':
        actualOutputRoll = float(input("Enter percentage(-100 to 100): "))
        print "Roll set to",actualOutputRoll

    elif res == 'p':
        actualOutputPitch = float(input("Enter percentage(-100 to 100): "))
        print "Pitch set to",actualOutputPitch

    elif res == 'y':
        actualOutputYaw= float(input("Enter percentage(-100 to 100): "))
        print "Yaw set to",actualOutputYaw
        
    elif res == 'g':
        resetAllYawPitchRoll()
        print("Quad stabilized")

    elif res == 'q':
        cycling=False




                
#exit        
pi.set_mode(esc_pinH, pigpio.INPUT)
pi.set_mode(esc_pinL, pigpio.INPUT)
pi.set_mode(esc_pinR, pigpio.INPUT)
pi.set_mode(esc_pinT, pigpio.INPUT)
#disconnect
pi.stop()

exit()



    
