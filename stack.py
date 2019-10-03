import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN,pull_up_down=GPIO.PUD_UP)

counter = 0
total = 0
vendoState = True

while True:
    while vendoState:
        if GPIO.input(17) == 0:
            counter+=1
            time.sleep(.1)

            print(counter)
            total = counter * 5
print(total)
