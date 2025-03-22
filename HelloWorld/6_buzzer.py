# All testing has been done in python 3.7.9
from pinouts import PhyComPins as pins
import pyfirmata
from pyfirmata import Arduino, util

from time import sleep
times=5
board = Arduino('COM7')

BUZZ = board.get_pin('d:11:p')
BUZZ.write(0.3)