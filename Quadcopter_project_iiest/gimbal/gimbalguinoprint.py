
#Quadcopter gimbal....2 axis movement mainly for ground vision
from Tkinter import *
import tkFont
import time
import pigpio 

panservo=13#BCM PIN NUMBER equivalent to BOARD 33
tiltservo=16#BCM PIN NUMBER equivalent to BOARD 36


print("\nMake sure your pigpio daemon is running..\ni.e. sudo pigpiod")
print('\n***Press ENTER...')
res = raw_input()


win = Tk()
myFont = tkFont.Font(family = 'Helvetica', size = 22, weight = 'bold')

#limits
panservoleftlimit=650#should be greater than 500
panservomiddlelimit=1500#should be about 1500
panservorightlimit=2500#should be less than 2500
tiltservoleftlimit=650#should be greater than 500
tiltservomiddlelimit=1500#should be about 1500
tiltservorightlimit=2500#should be less than 2500

#calculations
tiltservoleftspan=tiltservomiddlelimit-tiltservoleftlimit
tiltservorightspan=tiltservorightlimit-tiltservomiddlelimit

panservoleftspan=panservomiddlelimit-panservoleftlimit
panservorightspan=panservorightlimit-panservomiddlelimit

#connect to pigpiod daemon
pi = pigpio.pi()
 
# setup pin as an output
pi.set_mode(panservo, pigpio.OUTPUT)
pi.set_mode(tiltservo, pigpio.OUTPUT)

def resetpos():
    pan.set(90)
    tilt.set(90)





def exitProgram():
    
    resetpos()
    print("Exiting gimbal....Press ok in messagebox")
    #cleanup
    pi.set_mode(panservo, pigpio.INPUT)
    pi.set_mode(tiltservo, pigpio.INPUT)
    #disconnect
    pi.stop()
    win.quit()
    exit()

def updatepan(panval2):
    panval=float(panval2)
    if(panval<=90):
        scaling=panservoleftspan/90.0*panval
        val=scaling + panservoleftlimit

    if(panval>90):
        scaling=panservorightspan/90.0*(panval-90.0)
        val=scaling + panservomiddlelimit
       
    pi.set_servo_pulsewidth(panservo,val)



    
def updatetilt(tiltval2):
    tiltval=float(tiltval2)
    if(tiltval<=90):
        scaling=tiltservoleftspan/90.0*tiltval
        val=scaling + tiltservoleftlimit

    if(tiltval>90):
        scaling=tiltservorightspan/90.0*(tiltval-90.0)
        val=scaling + tiltservomiddlelimit
    
    pi.set_servo_pulsewidth(tiltservo,val)




    
win.title("Raspberry Pi Camera Gimbal")
win.geometry('320x240')


exitButton  = Button(win, text = "Exit", font = myFont, command = exitProgram, height =1 , width = 3) 
exitButton.pack(side = BOTTOM)

resetbutton = Button(win, text = "Reset", font = myFont, command = resetpos, height =1 , width = 3)
resetbutton.pack(side = BOTTOM)
pan = Scale(win, from_=0, to=180,command=updatepan)
pan.set(90)
pan.pack()
tilt = Scale(win, from_=0, to=180, orient=HORIZONTAL,command=updatetilt)
tilt.set(90)
tilt.pack()


win.mainloop()
