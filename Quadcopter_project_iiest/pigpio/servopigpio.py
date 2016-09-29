import time
import pigpio 

LED_PIN =13
 
#connect to pigpiod daemon
pi = pigpio.pi()
 
# setup pin as an output
pi.set_mode(LED_PIN, pigpio.OUTPUT)
 
pi.set_servo_pulsewidth(LED_PIN, 500)
time.sleep(1)
pi.set_servo_pulsewidth(LED_PIN, 2500)
time.sleep(1)
 
#cleanup
pi.set_mode(LED_PIN, pigpio.INPUT)
#disconnect
pi.stop()
