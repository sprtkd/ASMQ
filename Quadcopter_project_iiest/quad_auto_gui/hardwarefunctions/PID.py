#constants-----
inputThrottle=0
inputRoll=0
inputYaw=0
inputPitch=0


angle_x=0
angle_y=0
angularVelocity_z=0

actualOutputThrottle=0
actualOutputRoll=0
actualOutputPitch=0
actualOutputYaw=0

IsAcromode=0

rolliterm=0
pitchiterm=0
yawiterm=0

lastroll=0
lastpitch=0
lastyaw=0
#constants-----


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

    if (IsAcromode==0):
        
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
    

