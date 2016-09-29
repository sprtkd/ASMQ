#libray import------
import time
import pigpio 
#libray import------

#pins----
panservo=13#BCM PIN NUMBER equivalent to BOARD 33
tiltservo=16#BCM PIN NUMBER equivalent to BOARD 36
#pins----

#globals----
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
#globals----

#setup----
pi = pigpio.pi()
pi.set_mode(panservo, pigpio.OUTPUT)
pi.set_mode(tiltservo, pigpio.OUTPUT)
#setup----

#functions-----
def updatepan(panvalstr):
    panval=float(panvalstr)
    if(panval<=90):
        scaling=panservoleftspan/90.0*panval
        val=scaling + panservoleftlimit

    if(panval>90):
        scaling=panservorightspan/90.0*(panval-90.0)
        val=scaling + panservomiddlelimit
       
    pi.set_servo_pulsewidth(panservo,val)



    
def updatetilt(tiltvalstr):
    tiltval=float(tiltvalstr)
    if(tiltval<=90):
        scaling=tiltservoleftspan/90.0*tiltval
        val=scaling + tiltservoleftlimit

    if(tiltval>90):
        scaling=tiltservorightspan/90.0*(tiltval-90.0)
        val=scaling + tiltservomiddlelimit
        
    pi.set_servo_pulsewidth(tiltservo,val)




#functions-----








#cleanup
    pi.set_mode(panservo, pigpio.INPUT)
    pi.set_mode(tiltservo, pigpio.INPUT)
    #disconnect
    pi.stop()
    exit()
#functions-----
