#!/usr/bin/env python3
'''Hello to the world from ev3dev.org'''

import os
import sys
import time

from ev3dev2.motor import MediumMotor, OUTPUT_C,OUTPUT_D,SpeedPercent;
from ev3dev2.sensor import INPUT_4,INPUT_3;
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor;
from ev3dev2.button import Button;

# state constants
ON = True
OFF = False
init_status = False
steeringInit = int
steeringInit = 0
runTime = int
runTime = 0

button = Button()
driveMotor = MediumMotor(OUTPUT_D)
steeringMotor = MediumMotor(OUTPUT_C)
gyro = GyroSensor(INPUT_4)
horDis = UltrasonicSensor(INPUT_3)

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


def reset_console():
    '''Resets the console to the default state'''
    print('\x1Bc', end='')


def set_cursor(state):
    '''Turn the cursor on or off'''
    if state:
        print('\x1B[?25h', end='')
    else:
        print('\x1B[?25l', end='')


def set_font(name):
    '''Sets the console font

    A full list of fonts can be found with `ls /usr/share/consolefonts`
    '''
    os.system('setfont ' + name)

def init():
    print('initing!')
    reset_console()
    set_cursor(OFF)
    set_font('Lat15-Terminus24x12')
    driveMotor.reset
    steeringMotor.reset
    print(steeringMotor.position)
    gyro.reset
    
    steeringInit = steeringMotor.position
    
    # steering left to right 105 to 15

    print('press right to start!')

def main():
    print('press up to go')
    '''The main function of our program'''

    if button.up != False:
        driveMotor.on_for_degrees(SpeedPercent(50),360)
        print("finish")
        time.sleep(1)


if __name__ == '__main__':
    init()
    steeringMotor.on_to_position(SpeedPercent(100),int(60 + steeringInit))
    time.sleep(1)
    print('press to start')
    while button.right != True:
        time.sleep(0.1)
    while button.backspace != True:
        print(steeringMotor.position)
        main()
