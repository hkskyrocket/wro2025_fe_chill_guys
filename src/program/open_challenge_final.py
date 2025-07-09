#!/usr/bin/env python3
'''Hello to the world from ev3dev.org'''

import os
import sys
import time

from math import cos,pi
from ev3dev2.led import Leds
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
targetHeading = float
heading_kp = float(1)
distance_kp = float(1)

button = Button()
driveMotor = MediumMotor(OUTPUT_D)
steeringMotor = MediumMotor(OUTPUT_C)
gyro = GyroSensor(INPUT_4)
horDis = UltrasonicSensor(INPUT_3)
colourSensor = ColorSensor(INPUT_2)
sound = Sound()
led = Leds()

gyroInit = int(gyro.angle)

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
    distanceCorrection(11)
    print("wall follower")
    
def headingCorrect(targetHeading):
    targetHeading = float(targetHeading)
    headingError = float(targetHeading - getHeading(gyro.angle))
    heading_output = headingLimit(headingError)
    heading_output = float(heading_output * heading_kp)
    
    steeringMotor.on_to_position(SpeedPercent(100),int(steeringInit + heading_output ))
    print("heading error,output",headingError,heading_output)
        
def headingLimit(targetHeadingCorrection):
    targetHeadingCorrection = float(targetHeadingCorrection)
    if(getHeading(gyro.angle)>15 and targetHeadingCorrection <0):
        if getHeading(gyro.angle) <25:
            return int(15)
        else :
            return int(45)
    elif(getHeading(gyro.angle)<-15 and targetHeadingCorrection >0 ):
        if getHeading(gyro.angle) >-25:
            return int(-15)
        else:
            return int(-45)
    elif(abs(targetHeadingCorrection) >45):
        return int(targetHeadingCorrection / abs(targetHeadingCorrection) * 45)
    elif (abs(targetHeadingCorrection)< 10 and abs(targetHeadingCorrection)>3):
        return int(3 * targetHeadingCorrection / abs(targetHeadingCorrection))
    else:
        return targetHeadingCorrection/2       
        
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
    total = r + g + b
    debug_print("total",total)
    if(total < 400):
        if (r>135):
            print(colour[1])
            return int(1)
        else:
            print(colour[2])
            return int(2)
    elif((r-b)>10):
        print(colour[1])
        return int(1)
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
led.set_color("LEFT","RED")
led.set_color("RIGHT","RED")
init()
sound.set_volume(100)
    
print('press to start')
sound.beep()
colourSensor.MODE_RGB_RAW
led.set_color("LEFT","ORANGE")
led.set_color("RIGHT","ORANGE")
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
currentDrive = driveMotor.position
driveMotor.on(SpeedPercent(30))
while(currentDetectedColour == 0 ):
        print("session moved",sessionMoved)
        wallFollower()
        currentDetectedColour = getColourDetected(colourSensor.rgb)
        print(colour[currentDetectedColour])
        currentDrive = driveMotor .position
finalDrive = 4500 - (currentDrive - initDrive)
if (currentDetectedColour == 1):
    while(sessionMoved<11):
        sound.beep()
        driveMotor.on(SpeedPercent(30))
        while (getWallDistance(horDis.distance_centimeters,getHeading(gyro.angle))<40):
            wallFollower()
            debug_print("wall detected")
            
        sound.beep()
        debug_print("turning")
        driveMotor.on(SpeedPercent(0))
        gyroInit = gyroInit + 95
        time.sleep(0.2)
        sound.beep()
        currentDetectedColour = 0
        initDrive = driveMotor.position
        currentDrive = driveMotor.position
        steeringMotor.on_to_position(SpeedPercent(100),int(steeringInit ))
        while ((not currentDetectedColour == 1) or 
               (currentDrive - initDrive)<3000):
            wallFollower()
            currentDrive = driveMotor.position
            if(currentDrive - initDrive)<800:
                driveMotor.on(SpeedPercent(40))
            elif(currentDrive - initDrive)<4000:
                driveMotor.on(SpeedPercent(100))
            else:
                driveMotor.on(SpeedPercent(25))
            print(currentDrive - initDrive)
            currentDetectedColour = getColourDetected(colourSensor.rgb)
        sessionMoved = sessionMoved +1
        
    sound.beep()
    driveMotor.on(SpeedPercent(30))
    while (getWallDistance(horDis.distance_centimeters,getHeading(gyro.angle))<40):
        wallFollower()
   
    sound.beep()
    driveMotor.on(SpeedPercent(0))
    gyroInit = gyroInit + 90
    time.sleep(0.2)
    sound.beep()
    # gyroInit = gyroInit + 80
    time.sleep(0.2)
    sound.beep()
    currentDetectedColour = 0    
elif(currentDetectedColour == 2):
    while(sessionMoved<11):
        print("session moved",sessionMoved)
        sound.beep()
        driveMotor.on(SpeedPercent(0))
        gyroInit = gyroInit- 90
        time.sleep(0.2)
        sound.beep()
        currentDetectedColour = 0
        initDrive = driveMotor.position
        currentDrive = driveMotor.position
        while ((not currentDetectedColour == 2) or 
               (currentDrive - initDrive)<3000):
            currentDrive = driveMotor.position
            if(currentDrive - initDrive)<800:
                driveMotor.on(SpeedPercent(40))
            elif(currentDrive - initDrive)<4000:
                driveMotor.on(SpeedPercent(100))
            else:
                driveMotor.on(SpeedPercent(25))
            print('drive position',currentDrive - initDrive)
            wallFollower()
            currentDetectedColour = getColourDetected(colourSensor.rgb)
        sessionMoved = sessionMoved +1
    sound.beep()
    driveMotor.on(SpeedPercent(0))
    gyroInit = gyroInit- 90
    time.sleep(0.2)
initDrive = driveMotor.position
currentDrive = driveMotor.position
driveMotor.on(SpeedPercent(100))
while ((currentDrive - initDrive - 800)<finalDrive):
    if(currentDrive - initDrive)<800:
        driveMotor.on(SpeedPercent(40))
    else:
        driveMotor.on(SpeedPercent(100))
    currentDrive = driveMotor.position
    wallFollower()
driveMotor.on(SpeedPercent(0))
print('end')
sys.exit()
