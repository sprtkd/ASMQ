#to set a frequency generator for esc
# Requires the pigpio daemon to be running
#
# sudo pigpiod
print("\nMake sure your pigpio daemon is running..\nsudo pigpiod")
print('\n***Press ENTER...')
res = raw_input()
esc_pin=17
#pin BCM

import pigpio
print("From BCM using pin")
print(esc_pin)

pi = pigpio.pi() # Connect to local Pi.



pi.set_servo_pulsewidth(esc_pin, 2000) #start with full throttle
print('***Connect Battery & Press ENTER to calibrate')
res = raw_input()
pi.set_servo_pulsewidth(esc_pin, 1000)  #zero throttle
print('***Calibration Completed...Press ENTER to start')
res = raw_input()


pwidth=1000
#duty cycle for zero throttle

print ('set throttle percentage > s |quit > q')

cycling = True
try:
    while cycling:
        pi.set_servo_pulsewidth(esc_pin, pwidth)
        print('Option: ')
        res = raw_input()
        if res == 's':
            print('Enter percentage')
            val = float(input(": "))
            pwidth = 1000+(val*1000/100)
            print('throttle set to')
            print(val)
        if res == 'q':
            cycling = False
finally:
    # shut down cleanly
    pi.set_servo_pulsewidth(esc_pin, 1000)  #zero throttle
    pi.stop()


print('***Press ENTER to quit')
res = raw_input()
pi.stop()

