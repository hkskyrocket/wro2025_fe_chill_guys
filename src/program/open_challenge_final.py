#!/usr/bin/env python3
'''Hello to the world from ev3dev.org'''

import os
import sys
import time

from math import cos,pi
from ev3dev2.sound import Sound
from ev3dev2.motor import MediumMotor, OUTPUT_C,OUTPUT_D,SpeedPercent;
from ev3dev2.sensor import INPUT_4,INPUT_3,INPUT_2;
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor,ColorSensor;
from ev3dev2.button import Button;

# state constants
ON = True
OFF = False
init_status = False

colour = ['white','orange','blue']
currentDetectedColour = 0
sessionMoved = int(0)
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
colourSensor = ColorSensor(INPUT_2)
sound = Sound()

gyroInit = float(gyro.angle)

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
    colourSensor.MODE_RGB_RAW
    

    # steering left to right 105 to 15
def getHeading(currentValue):
    currentValue = int(currentValue)
    return int(currentValue - gyroInit)

def wallFollower():
    distanceCorrection(8)
    print("wall follower")
    
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
    elif(abs(distanceError)<1):
        distanceError = 0
    elif (distanceError > 0):
        distanceError = distanceError * 12
    distance_output = float(distanceError * distance_kp)
    # distance_output = targetHeading
    headingCorrect(distance_output)
    print("distance actual error,calualted error,output",float(targetDistance - currentDistance),distanceError,distance_output)
    
def getWallDistance(detectDistance,currentHeading):
    currentHeading = float(currentHeading)
    detectDistance = float(detectDistance) 
    return float(cos(abs(currentHeading/180*pi)) * detectDistance)

def getColourDetected(rgb):
    r = rgb[0]
    g = rgb [1]
    b = rgb[2]
    if(b < 230):
        if (r>120):
            print(colour[1])
            return int(1)
        else:
            print(colour[2])
            return int(2)
    else:
        print(colour[0])
        return int(0)
    
# def getColourDetected(reflect):
#     reflect = int(reflect)
#     if(reflect < 40):
#         print(colour[2])
#         return int(2)
        
#     elif(reflect < 60):
#         print(colour[1])
#         return int(1)
#     else:
#         print(colour[0])
#         return int(0)    
        
    
# start init program
init()
sound.set_volume(75)
    
print('press to start')
sound.beep()
colourSensor.MODE_RGB_RAW
while button.right != True:
    debug_print("colour",colourSensor.rgb,colour[getColourDetected(colourSensor.rgb)])
# wait for start

steeringInit = int(steeringMotor.position + 62)
steeringMotor.on_to_position(SpeedPercent(100),steeringInit)
gyroInit = gyro.angle
time.sleep(0.5)
print('press up to go')
sound.beep()
print('steering motor position',int(steeringMotor.position - steeringInit))
currentDetectedColour = getColourDetected(colourSensor.rgb)
initDrive = driveMotor.position
driveMotor.on(SpeedPercent(30))
while(currentDetectedColour == 0):
        print("session moved",sessionMoved)
        wallFollower()
        currentDetectedColour = getColourDetected(colourSensor.rgb)
        print(colour[currentDetectedColour])
        currentDrive = driveMotor .position
finalDrive = 4500 - (currentDrive - initDrive)
if (currentDetectedColour == 1):
    while(sessionMoved<11):
        while (getWallDistance(horDis.distance_centimeters,getHeading(gyro.angle))<50):
            wallFollower()
        sound.beep()
        steeringMotor.on_to_position(SpeedPercent(100),int(-25 + steeringInit ))
        driveMotor.on_for_degrees(SpeedPercent(100),200)
        print("session moved",sessionMoved)
        sound.beep()
        while(getHeading(gyro.angle) < 68):
            print(getHeading(gyro.angle))
            steeringMotor.on_to_position(SpeedPercent(100),int(-25 + steeringInit ))
        sound.beep()
        gyroInit = gyroInit + 68
        currentDetectedColour = 0
        initDrive = driveMotor.position
        currentDrive = driveMotor .position
        while ((currentDetectedColour == 0) or 
               (currentDrive - initDrive)<3500):
            if(currentDrive - initDrive)<3500:
                driveMotor.on(SpeedPercent(100))
            else:
                driveMotor.on(SpeedPercent(25))
            wallFollower()
            currentDrive = driveMotor .position
            print(currentDrive - initDrive)
            currentDetectedColour = getColourDetected(colourSensor.rgb)
        sessionMoved = sessionMoved +1
        
    while (getWallDistance(horDis.distance_centimeters,getHeading(gyro.angle))<50):
        wallFollower()
    sound.beep()
    steeringMotor.on_to_position(SpeedPercent(100),int(-25 + steeringInit ))
    driveMotor.on_for_degrees(SpeedPercent(100),200)
    print("session moved",sessionMoved)
    sound.beep()
    while(getHeading(gyro.angle) < 60):
        print(getHeading(gyro.angle))
        steeringMotor.on_to_position(SpeedPercent(100),int(-25 + steeringInit ))
    sound.beep()
    gyroInit = gyroInit + 90
    currentDetectedColour = 0    
elif(currentDetectedColour == 2):
    while(sessionMoved<11):
        print("session moved",sessionMoved)
        sound.beep()
        driveMotor.on(SpeedPercent(50))
        while(getHeading(gyro.angle)>-60):
            print(getHeading(gyro.angle))
            steeringMotor.on_to_position(SpeedPercent(100),int(25 + steeringInit ))
        sound.beep()
        gyroInit = gyroInit - 90
        currentDetectedColour = 0
        initDrive = driveMotor.position
        currentDrive = driveMotor .position
        while (( currentDetectedColour == 0) or 
               (currentDrive - initDrive)<3500):
            currentDrive = driveMotor .position
            if(currentDrive - initDrive)<3500:
                driveMotor.on(SpeedPercent(100))
            else:
                driveMotor.on(SpeedPercent(25))
            print('drive position',currentDrive - initDrive)
            wallFollower()
            currentDetectedColour = getColourDetected(colourSensor.rgb)
        sessionMoved = sessionMoved +1
    sound.beep()
    driveMotor.on(SpeedPercent(50))
    while(getHeading(gyro.angle)>-60):
        print(getHeading(gyro.angle))
        steeringMotor.on_to_position(SpeedPercent(100),int(25 + steeringInit ))
    sound.beep()
initDrive = driveMotor.position
currentDrive = driveMotor .position
driveMotor.on(SpeedPercent(100))
while ((currentDrive - initDrive)<finalDrive):
    currentDrive = driveMotor .position
    wallFollower()
driveMotor.on(SpeedPercent(0))
print('end')
sys.exit()
