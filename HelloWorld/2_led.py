# All testing has been done in python 3.7.9
from pinouts import PhyComPins as pins
from pyfirmata import Arduino, util

from time import sleep
times=5
board = Arduino('COM7')
try:
    while(times>0):
        board.digital[pins.PIN_RGB_R].write(1)
        sleep(1)
        board.digital[pins.PIN_RGB_R].write(0)
        sleep(1)
        times=times-1
except KeyboardInterrupt as ex:
    print(ex)

print("red led done")