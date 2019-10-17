from gpiozero import Button
import time

coinslot = Button(17)
confirm = Button(2)

counter = 0
global total
total = 0
coinslotState = True

while True:
    total = 0
    coinslotState = True
    counter = 0
    print(f'total: {total}, counter: {counter}, state: {coinslotState}')
    while coinslotState:
        if coinslot.is_pressed:
            counter+=1
            time.sleep(.1)

            print(counter)
            
        if confirm.is_pressed:
            print("test")
            coinslotState = False

            total = counter * 5
            print(f'total: {total}, counter: {counter}, state: {coinslotState}')
            

    