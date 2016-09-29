#QuadDarshan.......an initiative of Robodarshan IIEST,Shibpur
#full fledged gui for controlling quad

#importing libraries------------
import os 
from Tkinter import *
import tkFont
import time
import pigpio
import tkMessageBox
import RPi.GPIO as GPIO
import smbus
import math

#importing libraries------------


#pins------
relaypin=29
sonarTrigPin=32
sonarEchoPin=31
esc_pinH=17  #head Board 11
esc_pinL=27  #left Board 13
esc_pinR=22  #right Board 15
esc_pinT=23  #tail Board 16
panservo=13#BCM PIN NUMBER equivalent to BOARD 33
tiltservo=16#BCM PIN NUMBER equivalent to BOARD 36
#pins------

#globals-------


#mpu globals----
bus = smbus.SMBus(1)
now = time.time()
angvelerrorz=0.0
x_error=2.0
y_error=5.0
angle_x=0.0
angle_y=0.0
linacc_x=0.0
linacc_y=0.0
angularVelocity_z=0.0
last_x=0.0
last_y=0.0
gyro_scale = 131.0
accel_scale = 16384.0
address = 0x68  # This is the address value read via the i2cdetect command
#mpu globals----

#sonar globals-----
sonarHeightOffset=12.5 #in cm for calibration of quad height for zero correction
quadHeight=0 #in cm
#sonar globals-----

#motorcontroller globals-----
#these are outputs of pid function

actualOutputThrottle=0#should be in range 0 to 100
actualOutputRoll=0#should be in range -50 to 50 so that actualOutputRoll*rollmultiplier lies within -50 to 50
actualOutputPitch=0#should be in range -50 to 50 so that actualOutputPitch*pitchmultiplier lies within -50 to 50
actualOutputYaw=0#should be in range -50 to 50 so that actualOutputYaw*yawmultiplier lies within -50 to 50
#motorcontroller globals-----

#pid-----
inputThrottle=0
inputRoll=0
inputYaw=0
inputPitch=0




rolliterm=0
pitchiterm=0
yawiterm=0

lastroll=0
lastpitch=0
lastyaw=0
#pid-----

#gimbal globals----
#limits
panservoleftlimit=650#should be greater than 500
panservomiddlelimit=1550#should be about 1500
panservorightlimit=2500#should be less than 2500
tiltservoleftlimit=650#should be greater than 500
tiltservomiddlelimit=1400#should be about 1500
tiltservorightlimit=2500#should be less than 2500

#calculations
tiltservoleftspan=tiltservomiddlelimit-tiltservoleftlimit
tiltservorightspan=tiltservorightlimit-tiltservomiddlelimit

panservoleftspan=panservomiddlelimit-panservoleftlimit
panservorightspan=panservorightlimit-panservomiddlelimit
#gimbal globals----


#globals-------




#setup-----
GPIO.setmode(GPIO.BOARD)#for pigpio use bcm----
GPIO.setup(relaypin,GPIO.OUT)
GPIO.output(relaypin,False)

GPIO.setup(sonarTrigPin,GPIO.OUT)
GPIO.setup(sonarEchoPin,GPIO.IN)

os.system("sudo pigpiod") #pigpiod init
pi = pigpio.pi() # Connect to local Pi.
pi.set_mode(esc_pinH, pigpio.OUTPUT)
pi.set_mode(esc_pinL, pigpio.OUTPUT)
pi.set_mode(esc_pinR, pigpio.OUTPUT)
pi.set_mode(esc_pinT, pigpio.OUTPUT)
pi.set_mode(panservo, pigpio.OUTPUT)
pi.set_mode(tiltservo, pigpio.OUTPUT)
#setup-----





#functions-------



#exit-----
def exitProgram():
    print("Please press ok to exit...")
    GPIO.cleanup()
    pi.set_mode(esc_pinH, pigpio.INPUT)
    pi.set_mode(esc_pinL, pigpio.INPUT)
    pi.set_mode(esc_pinR, pigpio.INPUT)
    pi.set_mode(esc_pinT, pigpio.INPUT)
    pi.set_mode(panservo, pigpio.INPUT)
    pi.set_mode(tiltservo, pigpio.INPUT)
    #disconnect
    pi.stop()
    time.sleep(2)
    window.destroy()
    exit()
#exit-----

    
#init-----
def quadInit():
    checkboxIsAutopilot.deselect()
    rightframe2.pack_forget()
    leftframeMaster.pack( side = LEFT )
    checkboxIsAcromode.pack(side = RIGHT)
    checkboxIsAutogimbal.deselect()
    rightframe1.pack( side = RIGHT )
    checkboxIsAcromode.deselect()
    throttleslider.set(0)
    yawslider.set(0)
    pitchslider.set(0)
    rollslider.set(0)
    panGimbal.set(90)
    tiltGimbal.set(90)
    altVar.set("0")
    rollVar.set("0")
    pitchVar.set("0")
    yawVar.set("0")
    xAcclVar.set("0")
    yAcclVar.set("0")
    
    pi.set_servo_pulsewidth(esc_pinH, 1000)#zero throttle
    pi.set_servo_pulsewidth(esc_pinL, 1000)#zero throttle
    pi.set_servo_pulsewidth(esc_pinR, 1000)#zero throttle
    pi.set_servo_pulsewidth(esc_pinT, 1000)#zero throttle
    quadRelaySet(1)#after this turn on relay
    mpuinit()
    statusVar.set("STATUS: Ready... ")
    
#init-----

    
#reset------
def resetProgram():
    statusVar.set("STATUS:Resetting")
    window.update()
    quadInit()
    statusVar.set("STATUS:Reset Complete")
    window.update()
#reset------

#emergency land-----
def emergencyLand():
    statusVar.set("STATUS:EMERGENCY land")
    quadRelaySet(0)
    window.update()
#emergency land-----

#autopilot-----
def autopilotChange():
    if IsAutopilot.get():
        
        leftframeMaster.pack_forget()
        checkboxIsAcromode.pack_forget()
        rightframe2.pack( side = BOTTOM )
        statusVar.set("STATUS:Autopilot on")
    else:
        rightframe2.pack_forget()
        leftframeMaster.pack( side = LEFT )
        checkboxIsAcromode.pack(side = RIGHT)
        statusVar.set("STATUS:Autopilot off")
    window.update()

#autopilot-----

#autogimbal-----
def autoGimbalChange():
    if IsAutogimbal.get():
        statusVar.set("STATUS:Autogimbal on")
    else:
        statusVar.set("STATUS:Autogimbal off")
        
    window.update()
#autogimbal-----

#acromode------
def acromodeChange():
    if IsAcromode.get():
        statusVar.set("STATUS:Acromode on")
    else:
        statusVar.set("STATUS:Acromode off")
    
    window.update()
#acromode------

#updatesensorsvalues-------
def updatesensors():
    altVar.set(str(round(quadHeight)))
    rollVar.set(str(round(angle_y)))
    pitchVar.set(str(round(angle_x)))
    yawVar.set(str(round(angularVelocity_z)))
    xAcclVar.set(str(round(linacc_x)))
    yAcclVar.set(str(round(linacc_y)))

#updatesensorsvalues-------

#update_sliders------

def updateThrottle(ThrottleValStr):
    global inputThrottle
    inputThrottle=float(ThrottleValStr)
    
def updateYaw(YawValStr):
    global inputYaw
    inputYaw=float(YawValStr)
    
def updatePitch(PitchValStr):
    global inputPitch
    inputPitch=float(PitchValStr)
    
def updateRoll(RollValStr):
    global inputRoll
    inputRoll=float(RollValStr)
    



#update_sliders------


#reset_sliders------
def resetYawfunc():
    yawslider.set(0)
def resetPitchfunc():
    pitchslider.set(0)
def resetRollfunc():
    rollslider.set(0)
def resetGimbalfunc():   
    panGimbal.set(90)
    tiltGimbal.set(90)
#reset_sliders------

#increasedecreasesliders--------

def incThrottlefunc():
    instval=int(throttleslider.get())
    instval=instval+1
    throttleslider.set(instval)
def decThrottlefunc():
    instval=int(throttleslider.get())
    instval=instval-1
    throttleslider.set(instval)
def incYawfunc():
    instval=int(yawslider.get())
    instval=instval+1
    yawslider.set(instval)
def decYawfunc():
    instval=int(yawslider.get())
    instval=instval-1
    yawslider.set(instval)
def incPitchfunc():
    instval=int(pitchslider.get())
    instval=instval+1
    pitchslider.set(instval)
def decPitchfunc():
    instval=int(pitchslider.get())
    instval=instval-1
    pitchslider.set(instval)
def incRollfunc():
    instval=int(rollslider.get())
    instval=instval+1
    rollslider.set(instval)
def decRollfunc():
    instval=int(rollslider.get())
    instval=instval-1
    rollslider.set(instval)
#increasedecreasesliders--------


#autopilotfunc-----
def autoHoverfunc():
    notimplemented()
def autoLandfunc():
    notimplemented()

#autopilotfunc-----

#calibrate-----
def EscCalfunc():
    quadRelaySet(0)
    pi.set_servo_pulsewidth(esc_pinH, 2000)
    pi.set_servo_pulsewidth(esc_pinL, 2000)
    pi.set_servo_pulsewidth(esc_pinR, 2000)
    pi.set_servo_pulsewidth(esc_pinT, 2000)
    quadRelaySet(1)
    time.sleep(1.5)    
    pi.set_servo_pulsewidth(esc_pinH, 1000)#zero throttle
    pi.set_servo_pulsewidth(esc_pinL, 1000)#zero throttle
    pi.set_servo_pulsewidth(esc_pinR, 1000)#zero throttle
    pi.set_servo_pulsewidth(esc_pinT, 1000)#zero throttle
def MpuSensorCalfunc():
    calibrateMpu()
def exitCalibratefunc():
    global isTrueCalibration
    isTrueCalibration =0

def CalibrateQuad():
    Calibrationbox=Tk()
    global isTrueCalibration
    isTrueCalibration =1
    Calibrationbox.geometry('640x480')
    Calibrationbox.title("Calibrate")
    Label(Calibrationbox,fg="blue", text="Quadcopter Calibration",font=("Helvetica", 20) ).pack()
    
    EscCalButton  = Button(Calibrationbox, text = "Esc Calibrate",font =("Helvetica", 16) ,command=EscCalfunc) 
    EscCalButton.pack()
    MpuSensorCalButton  = Button(Calibrationbox, text = "Mpu Calibrate",font =("Helvetica", 16) ,command=MpuSensorCalfunc) 
    MpuSensorCalButton.pack()
    ExitCalButton  = Button(Calibrationbox, text = "EXIT",font =("Helvetica", 19) ,command=exitCalibratefunc) 
    ExitCalButton.pack()
    while isTrueCalibration:
        Calibrationbox.update()
    Calibrationbox.destroy()

    
#calibrate-----

#help--------
def HelpQuad():
    message=Tk()
    message.geometry('640x480')
    message.title("HELP")
    diagram = PhotoImage(master = message,file='help.png')
    Label(message, font=("Helvetica", 20),text="Quadcopter *+* Config").pack()
    logolbl= Label(message, image = diagram)
    logolbl.image=diagram
    logolbl.pack()
    message.update()
   
#help--------

#hardware------


#relay-----

def quadRelaySet(mode):
    # mode: 0 to turn off 1 to turn on and 2 to toggle
    if mode==0:
        GPIO.output(relaypin,False)
    elif mode==1:
        GPIO.output(relaypin,True)
    elif mode==2:
        if GPIO.input(relaypin):
            GPIO.output(relaypin,False)
        else:
            GPIO.output(relaypin,True)

#relay-----

#mpu6050-------

#mpu-init-----
def mpuinit():
    global now
    global last_x
    global last_y
    global angvelerrorz
    power_mgmt_1 = 0x6b
    power_mgmt_2 = 0x6c
    bus.write_byte_data(address, power_mgmt_1, 0)
    now = time.time()
    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all()

    last_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    last_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    angvelerrorz=gyro_scaled_z
#mpu-init-----
#accesory functions-----
def read_all():
    raw_gyro_data = bus.read_i2c_block_data(address, 0x43, 6)
    raw_accel_data = bus.read_i2c_block_data(address, 0x3b, 6)

    gyro_scaled_x = twos_compliment((raw_gyro_data[0] << 8) + raw_gyro_data[1]) / gyro_scale
    gyro_scaled_y = twos_compliment((raw_gyro_data[2] << 8) + raw_gyro_data[3]) / gyro_scale
    gyro_scaled_z = twos_compliment((raw_gyro_data[4] << 8) + raw_gyro_data[5]) / gyro_scale

    accel_scaled_x = twos_compliment((raw_accel_data[0] << 8) + raw_accel_data[1]) / accel_scale
    accel_scaled_y = twos_compliment((raw_accel_data[2] << 8) + raw_accel_data[3]) / accel_scale
    accel_scaled_z = twos_compliment((raw_accel_data[4] << 8) + raw_accel_data[5]) / accel_scale

    return (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z)
    
def twos_compliment(val):
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def calibrateMpu():
    global angvelerrorz
    global x_error
    global y_error
    global last_x
    global last_y
    print("Keep your quad straight and still.\nPress enter to continue....")
    raw_input()
    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all()
    x_error = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    y_error = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    mpuinit()
    print("Calibration complete..")
    
#accesory functions-----
#function

def updateMpu6050():
    global now
    global angle_x
    global angle_y
    global linacc_x
    global linacc_y
    global angularVelocity_z
    global last_x
    global last_y


    k = 0.85
    k1 = 1 - k
    dtime = 0
    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all()
    
    rotation_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    rotation_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

    dtime=time.time()-now
    
    now=time.time()
    
    last_x=(k*(last_x+(gyro_scaled_x*dtime)))+(k1*rotation_x)
    last_y=(k*(last_y+(gyro_scaled_x*dtime)))+(k1*rotation_y)


    angle_x=-(last_x-x_error)
    angle_y=-(last_y-y_error)
    
    linacc_x=(accel_scaled_x-(math.sin(math.radians(angle_y))))*9.81#m/s^2
    linacc_y=(accel_scaled_y+(math.sin(math.radians(angle_x))))*9.81#m/s^2
    
    
    
    
    angularVelocity_z=-(gyro_scaled_z-angvelerrorz)





#mpu6050-------

    
#sonar----

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

#sonar----
    
#motor controller functions----

#function to reset all sliders----
def resetAllYawPitchRoll():
    resetYawfunc()
    resetPitchfunc()
    resetRollfunc()
    


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

    
    valH = actualOutputThrottle - (actualOutputPitch*pitchmultiplier) + (actualOutputYaw*yawmultiplier)
    valR = actualOutputThrottle - (actualOutputRoll*rollmultiplier) - (actualOutputYaw*yawmultiplier)
    valT = actualOutputThrottle + (actualOutputPitch*pitchmultiplier) + (actualOutputYaw*yawmultiplier)
    valL = actualOutputThrottle + (actualOutputRoll*rollmultiplier) - (actualOutputYaw*yawmultiplier)


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
        
#motor controller function-----

#gimbal functions-----
def updatePanGimbal(panvalstr):
    panval=float(panvalstr)
    if(panval<=90):
        scaling=panservoleftspan/90.0*panval
        val=scaling + panservoleftlimit

    if(panval>90):
        scaling=panservorightspan/90.0*(panval-90.0)
        val=scaling + panservomiddlelimit
       
    pi.set_servo_pulsewidth(panservo,val)



    
def updateTiltGimbal(tiltvalstr):
    tiltval=float(tiltvalstr)
    if(tiltval<=90):
        scaling=tiltservoleftspan/90.0*tiltval
        val=scaling + tiltservoleftlimit

    if(tiltval>90):
        scaling=tiltservorightspan/90.0*(tiltval-90.0)
        val=scaling + tiltservomiddlelimit
        
    pi.set_servo_pulsewidth(tiltservo,val)


def autoGimbalUpdate():
    if(IsAutogimbal.get()):
        panGimbal.set(90-angle_x)
        tiltGimbal.set(90-angle_y)

#gimbal functions-----





#hardware------

#pid-----
def pid():

    global actualOutputThrottle
    global actualOutputRoll
    global actualOutputPitch
    global actualOutputYaw
    global lastroll
    global lastpitch
    global lastyaw
    global rolliterm
    global pitchiterm
    global yawiterm

    actualOutputThrottle=inputThrottle#no mapping reqd.


    #mapping inputRoll,inputYaw,inputPitch to mappedRoll,mappedYaw,mappedPitch
    if (inputRoll>=0):
        mappedRoll=inputRoll*inputRoll*0.5
    elif (inputRoll<0):
        mappedRoll=inputRoll*inputRoll*(-0.5)
        
    if (inputYaw>=0):
        mappedYaw=inputYaw*inputYaw*0.5
    elif (inputYaw<0):
        mappedYaw=inputYaw*inputYaw*(-0.5)
        
    if (inputPitch>=0):
        mappedPitch=inputPitch*inputPitch*0.5
    elif (inputPitch<0):
        mappedPitch=inputPitch*inputPitch*(-0.5)

    if (IsAcromode.get()==0):
        
        ##  pid constants
        rkp=0.1
        pkp=0.2
        ykp=0.3
        rki=0.1
        pki=0.2
        yki=0.3
        rkd=0.1
        pkd=0.2
        ykd=0.3

        #mapping mappedangle_x,mappedangle_y,ZangularvelMapped pid with angle_x ,angle_y,angularVelocity_z
        if (angularVelocity_z>0):
            Zthreshold=2
        elif (angularVelocity_z<0):
            Zthreshold=-2
        else:
            Zthreshold=0
        
        ZangularvelMapped=(angularVelocity_z-Zthreshold)*(50.0/35.0)

        mappedangle_x=angle_x*(50.0/90.0)
        mappedangle_y=angle_y*(50.0/90.0)

        ## taking roll as angle with X axis and pitch as the angle with Y axis
    
        rollerror=mappedRoll-mappedangle_x
        pitcherror=mappedPitch-mappedangle_y
        yawerror=mappedYaw-ZangularvelMapped
    
        rolliterm+=rki*rollerror
        pitchiterm+=pki*pitcherror
        yawiterm+=yki*yawerror
    
        if (rolliterm>50):
            rolliterm=50
        if (rolliterm<(-50)):
            rolliterm=(-50)
        if (pitchiterm>50):
            pitchiterm=50
        if (pitchiterm<(-50)):
            pitchiterm=(-50)
        if (yawiterm>50):
            yawiterm=50
        if (yawiterm<(-50)):
            yawiterm=(-50)
        
        delroll=lastroll-mappedangle_x
        delpitch=lastpitch-mappedangle_y
        delyaw=lastyaw-ZangularvelMapped
    
        actualOutputRoll=rkp*rollerror+rolliterm-rkd*delroll
        actualOutputPitch=pkp*pitcherror+pitchiterm-pkd*delpitch
        actualOutputYaw=ykp*yawerror+yawiterm-ykd*delyaw
    
        lastroll=mappedangle_x
        lastpitch=mappedangle_y
        lastyaw=ZangularvelMapped

    else:
        actualOutputRoll=mappedRoll
        actualOutputPitch=mappedPitch
        actualOutputYaw=mappedYaw
        lastroll=0
        lastpitch=0
        lastyaw=0
    
    return ()
    
#pid-----


            
#functions-------


#gui-init-------


window = Tk()
myFont = tkFont.Font(family = 'Helvetica', size = 20, )
headingFont = tkFont.Font(family = 'Helvetica', size = 14, weight = 'bold')
#gui-init-------

#gui globals----
statusVar =StringVar()
IsAutopilot = IntVar()
IsAutogimbal = IntVar()
IsAcromode = IntVar()
altVar = StringVar()
rollVar =StringVar()
pitchVar =StringVar()
yawVar =StringVar()
xAcclVar = StringVar()
yAcclVar = StringVar()


isTrueCalibration=0
#gui globals----

#gui--------
#gui-set----
window.title("QuadDarshan..Robodarshan IIEST,Shibpur")
window.geometry('900x680')

topframe = Frame(window,borderwidth=1,relief=GROOVE)#for checkboxes...
topframe.pack()
bottomframe3 = Frame(window,borderwidth=1,relief=GROOVE)#for special buttons..
bottomframe3.pack( side = BOTTOM )
bottomframe2 = Frame(window,borderwidth=1,relief=GROOVE)#for acceleration values..
bottomframe2.pack( side = BOTTOM )
bottomframe1 = Frame(window,borderwidth=1,relief=GROOVE)#for Orientation values..
bottomframe1.pack( side = BOTTOM )
leftframeMaster = Frame(window,borderwidth=1,relief=GROOVE)#for controlling quad..
leftframeMaster.pack( side = LEFT )
leftframe1 = Frame(leftframeMaster,borderwidth=1,relief=GROOVE)#for controlling throttle quad..
leftframe1.pack( side = LEFT )
leftframe2Master = Frame(leftframeMaster,borderwidth=1,relief=GROOVE)
leftframe2Master.pack( side = RIGHT )
leftframe2_1 = Frame(leftframe2Master,borderwidth=1,relief=GROOVE)#for controlling throttle quad..
leftframe2_1.pack()
leftframe2_2 = Frame(leftframe2Master,borderwidth=1,relief=GROOVE)#for controlling throttle quad..
leftframe2_2.pack()
leftframe2_3 = Frame(leftframe2Master,borderwidth=1,relief=GROOVE)#for controlling throttle quad..
leftframe2_3.pack()

rightframeMaster = Frame(window,borderwidth=1,relief=GROOVE)#for contolling gimbal...
rightframeMaster.pack( side = RIGHT )
rightframe1 = Frame(rightframeMaster,borderwidth=1,relief=GROOVE)#for contolling gimbal...
rightframe1.pack()
rightframe2 = Frame(rightframeMaster,borderwidth=1,relief=GROOVE)#for autopilot...
rightframe2.pack( side = BOTTOM )
#gui-set----

#topframe----
heading = Label(topframe,font = headingFont,fg="blue", text="QuadDarshan..Robodarshan IIEST,Shibpur")
heading.pack()
statusVarLabel = Label(topframe,font = myFont,fg="Green", textvariable=statusVar)
statusVarLabel.pack(side = LEFT)
statusVar.set("STATUS: Pls wait... ")
checkboxIsAutopilot = Checkbutton(topframe,font = myFont, text = "Autopilot", variable = IsAutopilot, onvalue = 1, offvalue = 0,command=autopilotChange)
checkboxIsAutopilot.pack(side = LEFT)
checkboxIsAutogimbal = Checkbutton(topframe,font = myFont, text = "Auto Gimbal", variable = IsAutogimbal, onvalue = 1, offvalue = 0,command=autoGimbalChange)
checkboxIsAutogimbal.pack(side = LEFT)
checkboxIsAcromode = Checkbutton(topframe,font = myFont, text = "Acro mode", variable = IsAcromode, onvalue = 1, offvalue = 0,command=acromodeChange)
checkboxIsAcromode.pack(side = RIGHT)


#topframe----

#leftframe-----

#throttle-----
throttleNameLabel = Label(leftframe1,font = myFont,fg="blue", text="Quadcopter Throttle")
throttleNameLabel.pack()
throttleIncreaseButton  = Button(leftframe1, text = "+",font = myFont,width = 6,height = 2,command=incThrottlefunc) 
throttleIncreaseButton.pack()

throttleslider = Scale(leftframe1, from_=100, to=0,tickinterval=10, length=230,command=updateThrottle)
throttleslider.set(0)
throttleslider.pack()

throttleDecreaseButton  = Button(leftframe1, text = "-",font = myFont,width = 6,height = 2,command=decThrottlefunc) 
throttleDecreaseButton.pack()
#throttle-----

#yaw------

yawNameLabel = Label(leftframe2_1,font = myFont,fg="blue", text="Yaw")
yawNameLabel.pack()

yawDecreaseButton  = Button(leftframe2_1, text = "-",font = myFont,width = 5,height = 2,command=decYawfunc) 
yawDecreaseButton.pack(side = LEFT)

yawslider = Scale(leftframe2_1, from_=-10, to=10,tickinterval=5, orient=HORIZONTAL,length=140,command=updateYaw)
yawslider.set(0)
yawslider.pack(side = LEFT)

yawResetButton  = Button(leftframe2_1,font = myFont,height = 2, text = "Reset Yaw",command=resetYawfunc) 
yawResetButton.pack(side = RIGHT)

yawIncreaseButton  = Button(leftframe2_1, text = "+",font = myFont,width = 5,height = 2,command=incYawfunc) 
yawIncreaseButton.pack(side = RIGHT)



#yaw------

#pitch------
pitchNameLabel = Label(leftframe2_2,font = myFont,fg="blue", text="Pitch")
pitchNameLabel.pack()
pitchResetButton  = Button(leftframe2_2, text = "Reset Pitch",font = myFont,width = 12,command=resetPitchfunc) 
pitchResetButton.pack()
pitchIncreaseButton  = Button(leftframe2_2, text = "+",font = myFont,width = 5,height = 2,command=incPitchfunc) 
pitchIncreaseButton.pack()

pitchslider = Scale(leftframe2_2, from_=10, to=-10,tickinterval=5,command=updatePitch )
pitchslider.set(0)
pitchslider.pack()

pitchDecreaseButton  = Button(leftframe2_2, text = "-",font = myFont,width = 5,height = 2,command=decPitchfunc) 
pitchDecreaseButton.pack()



#pitch------


#roll------
rollNameLabel = Label(leftframe2_3,font = myFont,fg="blue", text="Roll")
rollNameLabel.pack()

rollDecreaseButton  = Button(leftframe2_3, text = "-",font = myFont,width = 5,height = 2,command=decRollfunc) 
rollDecreaseButton.pack(side = LEFT)

rollslider = Scale(leftframe2_3, from_=-10, to=10,tickinterval=5, orient=HORIZONTAL,length=140,command=updateRoll)
rollslider.set(0)
rollslider.pack(side = LEFT)

rollResetButton  = Button(leftframe2_3, text = "Reset Roll",height = 2,font = myFont,command=resetRollfunc) 
rollResetButton.pack(side = RIGHT)

rollIncreaseButton  = Button(leftframe2_3, text = "+",font = myFont,width = 5,height = 2,command=incRollfunc) 
rollIncreaseButton.pack(side = RIGHT)
#roll------
#leftframe-----

#rightframe-----
#gimbal-----
gimbalNameLabel = Label(rightframe1,font = myFont,fg="blue", text="Gimbal Control")
gimbalNameLabel.pack()

panGimbal = Scale(rightframe1, from_=0, to=180,length=170,tickinterval=45,command=updatePanGimbal)
panGimbal.set(90)
panGimbal.pack()
tiltGimbal = Scale(rightframe1, from_=0, to=180, orient=HORIZONTAL,length=170,tickinterval=45,command=updateTiltGimbal)
tiltGimbal.set(90)
tiltGimbal.pack()

resetGimbalButton = Button(rightframe1, text = "Reset Gimbal", font = myFont, height =2 , width = 10,command=resetGimbalfunc)
resetGimbalButton.pack(side = BOTTOM)
#gimbal-----

#autopilot------
autopilotNameLabel = Label(rightframe2,font = myFont,fg="blue", text="Autopilot")
autopilotNameLabel.pack()
autoHoverButton = Button(rightframe2, text = "Hover", font = myFont, height=2 , width = 10,command=autoHoverfunc)
autoHoverButton.pack()
autoLandButton = Button(rightframe2, text = "Land", font = myFont, height =2 , width = 10,command=autoLandfunc)
autoLandButton.pack()
#autopilot------
#rightframe-----



#bottomframe1----
altNameLabel = Label(bottomframe1,font = myFont,fg="blue", text="  Altitude: ")
altNameLabel.pack(side = LEFT)
altVarLabel = Label(bottomframe1,font = myFont,fg="red", textvariable=altVar)
altVarLabel.pack(side = LEFT)
altVar.set("0")                   
rollNameLabel = Label(bottomframe1,font = myFont,fg="blue", text="  Roll: ")
rollNameLabel.pack(side = LEFT)
rollVarLabel = Label(bottomframe1,font = myFont,fg="red", textvariable=rollVar)
rollVarLabel.pack(side = LEFT)
rollVar.set("0")
pitchNameLabel = Label(bottomframe1,font = myFont,fg="blue", text="  Pitch: ")
pitchNameLabel.pack(side = LEFT)
pitchVarLabel = Label(bottomframe1,font = myFont,fg="red", textvariable=pitchVar)
pitchVarLabel.pack(side = LEFT)
pitchVar.set("0")
yawNameLabel = Label(bottomframe1,font = myFont,fg="blue", text="  Yaw: ")
yawNameLabel.pack(side = LEFT)
yawVarLabel = Label(bottomframe1,font = myFont,fg="red", textvariable=yawVar)
yawVarLabel.pack(side = LEFT)
yawVar.set("0")
#bottomframe1----



#bottomframe2----
xAcclNameLabel = Label(bottomframe2,font = myFont,fg="blue", text="  X Accl: ")
xAcclNameLabel.pack(side = LEFT)
xAcclVarLabel = Label(bottomframe2,font = myFont,fg="red", textvariable=xAcclVar)
xAcclVarLabel.pack(side = LEFT)
xAcclVar.set("0")                   
yAcclNameLabel = Label(bottomframe2,font = myFont,fg="blue", text="  Y Accl: ")
yAcclNameLabel.pack(side = LEFT)
yAcclVarLabel = Label(bottomframe2,font = myFont,fg="red", textvariable=yAcclVar)
yAcclVarLabel.pack(side = LEFT)
yAcclVar.set("0")

#bottomframe2----



#bottomframe3----
exitButton  = Button(bottomframe3, text = "Exit",font = myFont, command = exitProgram, height =2 , width = 6) 
exitButton.pack(side = LEFT)
resetButton  = Button(bottomframe3, text = "Reset",font = myFont, command = resetProgram, height =2 , width = 6) 
resetButton.pack(side = RIGHT)
emergencyLandButton  = Button(bottomframe3, text = "Emergency Land",font = myFont, command = emergencyLand, height =2 , width = 16) 
emergencyLandButton.pack(side = RIGHT)
calibrateButton  = Button(bottomframe3, text = "Calibrate",font = myFont, height =2 , width = 14,command=CalibrateQuad) 
calibrateButton.pack(side = RIGHT)
helpButton  = Button(bottomframe3, text = "Help",font = myFont, height =2 , width = 6,command=HelpQuad) 
helpButton.pack(side = RIGHT)
#bottomframe3----

window.update()

#gui--------

#starting-------
statusVar.set("STATUS: Starting... ")
window.update()
quadInit()


#starting-------

#mainloop------
while 1:
    
    window.update()
    updateMpu6050()
    #updateSonar() #pls uncomment it
    updatesensors()
    autoGimbalUpdate()
    pid()
    changeAllMotorsThrottleFunc()
    
#mainloop------



