#library import---
import RPi.GPIO as GPIO
import time
#library import---

#pins----
relaypin=29
#pins----

#setup-----
GPIO.setmode(GPIO.BOARD)

GPIO.setup(relaypin,GPIO.OUT)
GPIO.output(relaypin,False)
#setup-----

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

#example------

print("turning off")
quadRelaySet(0)
time.sleep(1)
print("turning on")
quadRelaySet(1)
time.sleep(1)
print("turning off")
quadRelaySet(0)
time.sleep(1)
print("toggling")
quadRelaySet(2)
time.sleep(1)
print("toggling")
quadRelaySet(2)
time.sleep(1)
print("toggling")
quadRelaySet(2)
time.sleep(1)
print("toggling")
quadRelaySet(2)
time.sleep(1)


#cleanup----
GPIO.cleanup()
