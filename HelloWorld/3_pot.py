# All testing has been done in python 3.7.9
from pinouts import PhyComPins as pins
import pyfirmata
from pyfirmata import Arduino, util

from time import sleep
times=5
board = Arduino('COM7')

it = util.Iterator(board)
it.start()
board.analog[pins.PIN_POT_1].enable_reporting()
while 1:
    _t=board.analog[pins.PIN_POT_1].read()
    print(_t)
    sleep(1)