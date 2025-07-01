#!/usr/bin/env python3
'''Hello to the world from ev3dev.org'''

import os
import sys
import time

from ev3dev2.motor import MediumMotor, OUTPUT_C,OUTPUT_D,SpeedPercent;
from ev3dev2.sensor import INPUT_4,INPUT_3,INPUT_2;
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor,ColorSensor;
from ev3dev2.button import Button;

# state constants
ON = True
OFF = False
init_status = False
blueDetected = bool(False)
forward = bool(False)

runTime = int(0)
steeringInit = int(0)
gyroInit = float(0)
targetHeading = float
heading_kp = float(0.1)

button = Button()
driveMotor = MediumMotor(OUTPUT_D)
steeringMotor = MediumMotor(OUTPUT_C)
gyro = GyroSensor(INPUT_4)
horDis = UltrasonicSensor(INPUT_3)
colourSensor = ColorSensor(INPUT_2)

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
    gyro.reset
    colourSensor.MODE_COL_REFLECT

    # steering left to right 105 to 15
def getHeading(currentValue):
    return float(currentValue - gyroInit)

def wallFollower():
    distanceError = float
    distanceError = float(4-horDis)
    steeringMotor.on_to_position(SpeedPercent(100),int(62+steeringInit))
    
def headingCorrect(targetHeading):
    targetHeading = float(targetHeading)
    headingError = float(targetHeading - getHeading(gyro.angle))
    heading_output = float(headingError * heading_kp)
    if (heading_output >45):
        heading_output = 45
    elif (heading_output <-45):
        heading_output = -45

def main():
    print(gyro.angle)
    print(getHeading(gyro.angle))
    '''The main function of our program'''
    if button.up == True:
        forward = True
    elif button.down == True:
        forward = False 
        
    if forward == True:
        if blueDetected == False :
            if(colourSensor.value >30):
                steeringMotor.on_to_position(SpeedPercent(100),int(62 + steeringInit))
                driveMotor.on(SpeedPercent(50))
            else:
                blueDetected = True
        elif blueDetected == True:
            if (getHeading(gyro.angle)>-90):
                steeringMotor.on_to_position(SpeedPercent(100),int(75 + steeringInit))
                driveMotor.on(SpeedPercent(50))
            else:
                forward = False
                blueDetected = False


if __name__ == '__main__':
    init()
    
    steeringInit = steeringMotor.position
    gyroInit = gyro.angle
    
    print('press to start')
    while button.right != True:
        time.sleep(0.1)
    steeringMotor.on_to_position(SpeedPercent(100),int(62 + steeringInit))
    time.sleep(1)
    print('press up to go')
    runMain = False
    while button.backspace != True:
        print(steeringMotor.position)
        main()