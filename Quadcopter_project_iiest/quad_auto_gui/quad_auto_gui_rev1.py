#QuadDarshan.......an initiative of Robodarshan IIEST,Shibpur
#full fledged gui for controlling quad

#importing libraries------------
import os 
from Tkinter import *
import tkFont
#importing libraries------------


#functions-------

#exit-----
def exitProgram():
    print("Please press ok to exit...")
    window.quit()
    exit()
#exit-----

#reset------
def resetProgram():
    print("Resetting....")
    
#reset------

#emergency land-----
def emergencyLand():
    print("Emergency...Stopping relay..")
    
#emergency land-----   
#functions-------


#init-------

os.system("sudo pigpiod") #command line execution
window = Tk()
myFont = tkFont.Font(family = 'Helvetica', size = 20, )
headingFont = tkFont.Font(family = 'Helvetica', size = 14, weight = 'bold')
#init-------


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
#globals-------


#gui--------

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
rightframe2 = Frame(rightframeMaster,borderwidth=1,relief=GROOVE)#for contolling gimbal...
rightframe2.pack( side = BOTTOM )
#topframe----
heading = Label(topframe,font = headingFont,fg="blue", text="QuadDarshan..Robodarshan IIEST,Shibpur")
heading.pack()
statusVarLabel = Label(topframe,font = myFont,fg="Green", textvariable=statusVar)
statusVarLabel.pack(side = LEFT)
statusVar.set("STATUS: Ready All OK... ")
checkboxIsAutopilot = Checkbutton(topframe,font = myFont, text = "Autopilot", variable = IsAutopilot, onvalue = 1, offvalue = 0)
checkboxIsAutopilot.pack(side = LEFT)
checkboxIsAutogimbal = Checkbutton(topframe,font = myFont, text = "Auto Gimbal", variable = IsAutogimbal, onvalue = 1, offvalue = 0)
checkboxIsAutogimbal.pack(side = LEFT)
checkboxIsAcromode = Checkbutton(topframe,font = myFont, text = "Acro mode", variable = IsAcromode, onvalue = 1, offvalue = 0)
checkboxIsAcromode.pack(side = RIGHT)


#topframe----

#leftframe-----

#throttle-----
throttleNameLabel = Label(leftframe1,font = myFont,fg="blue", text="Quadcopter Throttle")
throttleNameLabel.pack()
throttleIncreaseButton  = Button(leftframe1, text = "+",font = myFont,width = 6,height = 2) 
throttleIncreaseButton.pack()

throttleslider = Scale(leftframe1, from_=100, to=0,tickinterval=10, length=230)
throttleslider.set(0)
throttleslider.pack()

throttleDecreaseButton  = Button(leftframe1, text = "-",font = myFont,width = 6,height = 2) 
throttleDecreaseButton.pack()
#throttle-----

#yaw------

yawNameLabel = Label(leftframe2_1,font = myFont,fg="blue", text="Yaw")
yawNameLabel.pack()

yawDecreaseButton  = Button(leftframe2_1, text = "-",font = myFont,width = 5,height = 2) 
yawDecreaseButton.pack(side = LEFT)

yawslider = Scale(leftframe2_1, from_=-10, to=10,tickinterval=5, orient=HORIZONTAL,length=140)
yawslider.set(0)
yawslider.pack(side = LEFT)

yawResetButton  = Button(leftframe2_1,font = myFont,height = 2, text = "Reset Yaw") 
yawResetButton.pack(side = RIGHT)

yawIncreaseButton  = Button(leftframe2_1, text = "+",font = myFont,width = 5,height = 2) 
yawIncreaseButton.pack(side = RIGHT)



#yaw------

#pitch------
pitchNameLabel = Label(leftframe2_2,font = myFont,fg="blue", text="Pitch")
pitchNameLabel.pack()
pitchResetButton  = Button(leftframe2_2, text = "Reset Pitch",font = myFont,width = 12) 
pitchResetButton.pack()
pitchIncreaseButton  = Button(leftframe2_2, text = "+",font = myFont,width = 5,height = 2) 
pitchIncreaseButton.pack()

pitchslider = Scale(leftframe2_2, from_=10, to=-10,tickinterval=5 )
pitchslider.set(0)
pitchslider.pack()

pitchDecreaseButton  = Button(leftframe2_2, text = "-",font = myFont,width = 5,height = 2) 
pitchDecreaseButton.pack()



#pitch------


#roll------
rollNameLabel = Label(leftframe2_3,font = myFont,fg="blue", text="Roll")
rollNameLabel.pack()

rollDecreaseButton  = Button(leftframe2_3, text = "-",font = myFont,width = 5,height = 2) 
rollDecreaseButton.pack(side = LEFT)

rollslider = Scale(leftframe2_3, from_=-10, to=10,tickinterval=5, orient=HORIZONTAL,length=140)
rollslider.set(0)
rollslider.pack(side = LEFT)

rollResetButton  = Button(leftframe2_3, text = "Reset Roll",height = 2,font = myFont) 
rollResetButton.pack(side = RIGHT)

rollIncreaseButton  = Button(leftframe2_3, text = "+",font = myFont,width = 5,height = 2) 
rollIncreaseButton.pack(side = RIGHT)
#roll------
#leftframe-----

#rightframe-----
#gimbal-----
gimbalNameLabel = Label(rightframe1,font = myFont,fg="blue", text="Gimbal Control")
gimbalNameLabel.pack()

panGimbal = Scale(rightframe1, from_=0, to=180,length=170,tickinterval=45)
panGimbal.set(90)
panGimbal.pack()
tiltGimbal = Scale(rightframe1, from_=0, to=180, orient=HORIZONTAL,length=170,tickinterval=45)
tiltGimbal.set(90)
tiltGimbal.pack()

resetGimbalButton = Button(rightframe1, text = "Reset Gimbal", font = myFont, height =2 , width = 10)
resetGimbalButton.pack(side = BOTTOM)
#gimbal-----

#autopilot------
autopilotNameLabel = Label(rightframe2,font = myFont,fg="blue", text="Autopilot")
autopilotNameLabel.pack()
autoHoverButton = Button(rightframe2, text = "Hover", font = myFont, height=2 , width = 10)
autoHoverButton.pack()
autoLandButton = Button(rightframe2, text = "Land", font = myFont, height =2 , width = 10)
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
calibrateButton  = Button(bottomframe3, text = "Calibrate",font = myFont, height =2 , width = 14) 
calibrateButton.pack(side = RIGHT)
helpButton  = Button(bottomframe3, text = "Help",font = myFont, height =2 , width = 6) 
helpButton.pack(side = RIGHT)
#bottomframe3----

window.mainloop()

#gui--------
