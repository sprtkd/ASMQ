#program to control relay for esc's....

import RPi.GPIO as GPIO

relaypin=29

GPIO.setmode(GPIO.BOARD)

GPIO.setup(relaypin,GPIO.OUT)


print("\nFor Relay using pin:")
print(relaypin)

print("press enter to turn on relay..")
res=raw_input()

GPIO.output(relaypin,True)
print("\nEscs turned on...")
print("press enter to turn off relay..")
res=raw_input()


GPIO.output(relaypin,False)
print("\nEscs turned off...")
GPIO.cleanup()
