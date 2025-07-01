#!/usr/bin/env python3
'''Hello to the world from ev3dev.org'''

import os
import sys
import time

from math import cos,pi
from ev3dev2.motor import MediumMotor, OUTPUT_C,OUTPUT_D,SpeedPercent;
from ev3dev2.sensor import INPUT_4,INPUT_3;
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor;
from ev3dev2.button import Button;

# state constants
ON = True
OFF = False
init_status = False

runTime = int(0)
steeringInit = int(0)
gyroInit = float(0)
targetHeading = float
heading_kp = float(0.5)
distance_kp = float(1)

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
    gyro.reset

    # steering left to right 105 to 15
def getHeading(currentValue):
    currentValue = int(currentValue)
    return int(currentValue - gyroInit)

def wallFollower():
    distanceCorrection(15)
    
def headingCorrect(targetHeading):
    targetHeading = float(targetHeading)
    headingError = float(targetHeading - getHeading(gyro.angle))
    heading_output = headingLimit(headingError)
    heading_output = float(heading_output * heading_kp)
    
    steeringMotor.on_to_position(SpeedPercent(100),int(heading_output + steeringInit ))
    print("heading error,output",headingError,heading_output)
        
def headingLimit(targetHeadingCorrection):
    targetHeadingCorrection = float(targetHeadingCorrection)
    if(getHeading(gyro.angle)>15 and targetHeadingCorrection <0):
        return int(15)
    elif(getHeading(gyro.angle)<-15 and targetHeadingCorrection >0):
        return int(-15) 
    elif(abs(targetHeadingCorrection) >45):
        return int(targetHeadingCorrection / abs(targetHeadingCorrection) * 45)
    elif (abs(targetHeadingCorrection)< 10 and abs(targetHeadingCorrection)>3):
        return int(10 * targetHeadingCorrection / abs(targetHeadingCorrection))
    else:
        return targetHeadingCorrection       
        
def distanceCorrection(targetDistance):
    targetDistance = float(targetDistance)
    currentDistance = getWallDistance(horDis.distance_centimeters,getHeading(gyro.angle))
    distanceError = float(targetDistance - currentDistance)
    if (abs(distanceError) > 50):
        distanceError = 0
    elif(abs(distanceError)<2):
        distanceError = 0
    elif (distanceError > 0):
        distanceError = distanceError * 4
    distance_output = float(distanceError * distance_kp)
    # distance_output = targetHeading
    headingCorrect(distance_output)
    print("distance actual error,calualted error,output",float(targetDistance - currentDistance),distanceError,distance_output)
    
def getWallDistance(detectDistance,currentHeading):
    currentHeading = float(currentHeading)
    detectDistance = float(detectDistance)
    return float(cos(abs(currentHeading/180*pi)) * detectDistance)

def main():
    print(gyro.angle,getHeading(gyro.angle))
    wallFollower()
    if button.up == True:
        driveMotor.on(SpeedPercent(100))
    elif button.down == True:
        driveMotor.on(SpeedPercent(0))
    

if __name__ == '__main__':
    init()
    
    steeringInit = int(steeringMotor.position + 62)
    
    
    print('press to start')
    while button.right != True:
        time.sleep(0.1)
    steeringMotor.on_to_position(SpeedPercent(100),steeringInit)
    time.sleep(1)
    gyroInit = gyro.angle
    print('press up to go')
    while button.backspace != True:
        print('steering motor position',int(steeringMotor.position - steeringInit))
        if (button.enter == True):
           gyroInit = gyro.angle
        main()