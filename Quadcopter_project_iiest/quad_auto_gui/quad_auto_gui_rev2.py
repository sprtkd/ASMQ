#QuadDarshan.......an initiative of Robodarshan IIEST,Shibpur
#full fledged gui for controlling quad

#importing libraries------------
import os 
from Tkinter import *
import tkFont
import time
import pigpio
import tkMessageBox
#importing libraries------------


#functions-------


#notimplemented-----
def notimplemented():
    statusVar.set("STATUS: :-( Not implemented")
    window.update()
#notimplemented-----
#exit-----
def exitProgram():
    print("Please press ok to exit...")
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
    zAcclVar.set("0")
    statusVar.set("STATUS: Ready... ")
    window.update()
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
        rightframe1.pack_forget()
    else:
        statusVar.set("STATUS:Autogimbal off")
        rightframe1.pack( side = RIGHT )
        
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

#updatesensors-------
def updatesensors():
    notimplemented()
#updatesensors-------

#update_sliders------

def updateThrottle(ThrottleValStr):
    ThrottleVal=float(ThrottleValStr)
    print(ThrottleVal)
def updateYaw(YawValStr):
    notimplemented()
def updatePitch(PitchValStr):
    notimplemented()
def updateRoll(RollValStr):
    notimplemented()
def updatePanGimbal(PanGimbalValStr):
    notimplemented()
def updateTiltGimbal(TiltGimbalValStr):
    notimplemented()


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
    notimplemented()
def MpuSensorCalfunc():
    notimplemented()
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

    
#functions-------


#gui-init-------


window = Tk()
myFont = tkFont.Font(family = 'Helvetica', size = 20, )
headingFont = tkFont.Font(family = 'Helvetica', size = 14, weight = 'bold')
#gui-init-------


#globals-------
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
zAcclVar = StringVar()

isTrueCalibration=0
#globals-------


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
zAcclNameLabel = Label(bottomframe2,font = myFont,fg="blue", text="  Z Accl: ")
zAcclNameLabel.pack(side = LEFT)
zAcclVarLabel = Label(bottomframe2,font = myFont,fg="red", textvariable=zAcclVar)
zAcclVarLabel.pack(side = LEFT)
zAcclVar.set("0")

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
os.system("sudo pigpiod") #pigpiod init
quadInit()


#starting-------

#mainloop------
while 1:
    
    window.update()
#mainloop------



