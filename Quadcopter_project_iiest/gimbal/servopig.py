import time
import pigpio 

servopin=13#BCM PIN NUMBER


print("\nMake sure your pigpio daemon is running..\ni.e. sudo pigpiod")
print('\n***Press ENTER...')
res = raw_input()
#connect to pigpiod daemon
pi = pigpio.pi()
 
# setup pin as an output
pi.set_mode(servopin, pigpio.OUTPUT)

print("Enter s to set angle and q to quit")

cycling=True
while cycling:
    time.sleep(1)
    print('Option: ')
    res = raw_input()
    if res == 's':
        val = float(input("Enter vlaue between 500 and 2500: "))
        pi.set_servo_pulsewidth(servopin,val)
        print('Position set to')
        print(val)
    if res == 'q':
        cycling = False
#cleanup
pi.set_mode(servopin, pigpio.INPUT)
#disconnect
pi.stop()
exit()
