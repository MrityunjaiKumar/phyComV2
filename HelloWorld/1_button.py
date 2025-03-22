from pinouts import PhyComPins as pins
import pyfirmata
from pyfirmata import Arduino, util

from time import sleep
times=5
board = Arduino('COM3')

"""Buttons"""

board.digital[pins.PIN_BUTTON_1].mode = pyfirmata.INPUT  
board.digital[pins.PIN_BUTTON_2].mode = pyfirmata.INPUT  
board.digital[pins.PIN_BUTTON_3].mode = pyfirmata.INPUT  
board.digital[pins.PIN_BUTTON_4].mode = pyfirmata.INPUT
board.digital[pins.PIN_TILT].mode = pyfirmata.INPUT  
bt1=board.digital[pins.PIN_BUTTON_1]
bt2=board.digital[pins.PIN_BUTTON_2]
bt3=board.digital[pins.PIN_BUTTON_3]
bt4=board.digital[pins.PIN_BUTTON_4]
tilt=board.digital[pins.PIN_TILT]
it = pyfirmata.util.Iterator(board)  
it.start()  
while(1):
    print(f"bt1 = {bt1.read()},bt2= {bt2.read()},bt3= {bt3.read()},bt4= {bt4.read()}")
    sleep(1)
    print(f"tilt = {tilt.read()}")
    sleep(1)
