#to set a frequency generator for esc

esc_pin=8
#pin

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(esc_pin, GPIO.OUT)

servo = GPIO.PWM(esc_pin,50)#50 hz
servo.start(10) #start with full throttle
print('***Connect Battery & Press ENTER to calibrate')
res = raw_input()
servo.ChangeDutyCycle(5) #zero throttle
print('***Calibration Completed...Press ENTER to start')
res = raw_input()


dc=5
#duty cycle for zero throttle

print ('increase > a | decrease > z |  set throttle percentage > s |quit > q')

cycling = True
try:
    while cycling:
        servo.ChangeDutyCycle(dc)
        print('Option: ')
        res = raw_input()
        if res == 'a':
            dc = dc + 0.05
            print('throttle increased')
        if res == 'z':
            dc = dc - 0.05
            print('throttle decreased')
        if res == 's':
            print('Enter percentage')
            val = float(input(": "))
            dc = 5+(val*5/100)
            print('throttle set to')
            print(val)
        if res == 'q':
            cycling = False
finally:
    # shut down cleanly
    servo.stop()


print('***Press ENTER to quit')
res = raw_input()
servo.stop()
GPIO.cleanup()
