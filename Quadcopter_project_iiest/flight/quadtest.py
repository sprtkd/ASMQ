#to connect raspberry pi to esc's in a quadcopter 


print("\n\nQuadcopter *+* Configuration")
print("For Raspberry pi 2 model B")

#pins
esc_pinH=11  #head
esc_pinL=13  #left
esc_pinR=15  #right
esc_pinT=16  #tail
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

print("***If you want to calibrate Connect Battery & wait for music to stop..Then press enter")
res = raw_input()

motorH.ChangeDutyCycle(5) #zero throttle
motorL.ChangeDutyCycle(5) #zero throttle
motorR.ChangeDutyCycle(5) #zero throttle
motorT.ChangeDutyCycle(5) #zero throttle
print('***Calibration Completed...Press ENTER to start.\nIf you have not opted to calibrate connect battery now and press enter...')
res = raw_input()


#duty cycles for zero throttle
dcH=5
dcL=5
dcR=5
dcT=5
#throttle values
valH=0
valL=0
valR=0
valT=0


print ("\nEnter option to change motor throttle percentage\n h for head \n l for left\n r for right\n t for tail\n p to print throttle values\n And q to quit")
cycling = True
try:
    while cycling:
        motorH.ChangeDutyCycle(dcH)
        motorL.ChangeDutyCycle(dcL)
        motorR.ChangeDutyCycle(dcR)
        motorT.ChangeDutyCycle(dcT)
        print('Enter Option: ')
        res = raw_input()
        if res == 'h':
            print("Enter percentage(0-100)")
            valH = float(input(": "))
            dcH = 5+(valH*5/100)
            print("Head motor throttle set to")
            print(valH)	
        if res == 'l':
            print("Enter percentage(0-100)")
            valL = float(input(": "))
            dcL = 5+(valL*5/100)
            print("Left motor throttle set to")
            print(valL)
        if res == 'r':
            print("Enter percentage(0-100)")
            valR = float(input(": "))
            dcR = 5+(valR*5/100)
            print("Right motor throttle set to")
            print(valR)
        if res == 't':
            print("Enter percentage(0-100)")
            valT = float(input(": "))
            dcT = 5+(valT*5/100)
            print("Tail motor throttle set to")
            print(valT)
        if res == 'p':
            print("\nHead throttle:")
            print(valH)
            print("\nLeft throttle:")
            print(valL)
            print("\nRight throttle:")
            print(valR)
            print("\nTail throttle:")
            print(valT)
        if res == 'q':
            cycling = False
finally:
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







