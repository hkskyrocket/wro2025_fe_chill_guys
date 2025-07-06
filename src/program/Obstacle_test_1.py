#!/usr/bin/env python3
import os
import sys
import time

from time import sleep
from smbus import SMBus
from math import cos,pi;

from ev3dev2.display import Display
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sound import Sound
from ev3dev2.motor import MediumMotor, OUTPUT_C,OUTPUT_D,SpeedPercent;
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor,ColorSensor;
from ev3dev2.port import LegoPort
from ev3dev2.button import Button;

ON = True
OFF = False

colour = ['white','orange','blue']
currentDetectedColout = colour[1]
sessionMoved = int(0)
steeringInit = int(0)
gyroInit = float(0)
targetHeading = float
distance_kp = float(1)

# EV3 Display
button = Button()
driveMotor = MediumMotor(OUTPUT_D)
steeringMotor = MediumMotor(OUTPUT_C)
gyro = GyroSensor(INPUT_4)
horDis = UltrasonicSensor(INPUT_3)
colourSensor = ColorSensor(INPUT_2)
sound = Sound()
lcd = Display()
button = Button()
signFound = bool(False)
# Connect ToucSensor

# Set LEGO port for Pixy2 on input port 1
in1 = LegoPort(INPUT_1)
in1.mode = 'other-i2c'
# Short wait for the port to get ready
sleep(0.5)
print("in1 finish")

# Settings for I2C (SMBus(3) for INPUT_1)
bus = SMBus(3)
print("smbus ok (v1)")
# Make sure the same address is set in Pixy2
address = 0x54

# Signatures we're interested in (SIG1)
sigs = 3

# Data for requesting block
data = [174, 193, 32, 2, sigs, 1]

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
    
def headingCorrect(targetHeading,heading_kp):
    targetHeading = float(targetHeading)
    heading_kp = float(heading_kp)
    headingError = float(targetHeading - getHeading(gyro.angle))
    heading_output = headingLimit(headingError)
    try:
        print(heading_kp)
    except NameError:
        heading_kp = 0.5
    heading_output = float(heading_output * heading_kp)
    if (abs(heading_output)>45):
        heading_output = 45 * heading_output / abs(heading_output)
    steeringMotor.on_to_position(SpeedPercent(100),int(heading_output + steeringInit ))
    print("heading error,output",headingError,heading_output)
        
def headingLimit(targetHeadingCorrection):
    targetHeadingCorrection = float(targetHeadingCorrection)
    if(getHeading(gyro.angle)>20 and targetHeadingCorrection <0):
        return int(20)
    elif(getHeading(gyro.angle)<-15 and targetHeadingCorrection >0):
        return int(-20) 
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
    headingCorrect(distance_output,0.5)
    print("distance actual error,calualted error,output",float(targetDistance - currentDistance),distanceError,distance_output)
    
def getWallDistance(detectDistance,currentHeading):
    currentHeading = float(currentHeading)
    detectDistance = float(detectDistance)
    return float(cos(abs(currentHeading/180*pi)) * detectDistance)

def signPathing(area):
    area = int(area)
    if (area > 1000 ):
        print("target found")
        signFound = True
        dxc = 158 - x
        print("x,y",x,y)
        print("dxc",dxc)
        if(sig == 1):
            # red traffic sign
            if (dxc > -100):
                if (abs(dxc)< 30):
                    dxc = 30 * dxc / abs(dxc)
                headingCorrect(abs(dxc)*0.2,3)
            else:
                headingCorrect(15,0.5)
        elif (sig == 2):
            # green traffic sign
            print(dxc)
            if (dxc < 100):
                if (abs(dxc)< 30):
                    dxc = 30 * dxc / abs(dxc)
                headingCorrect(-abs(dxc)*0.2,3)
            else:
                headingCorrect(15,0.5)
    else:
        if (signFound):
            initDrivePosition = driveMotor.position
            while(driveMotor.position - initDrivePosition <200):
                headingCorrect(getHeading(gyro.angle),0.5)
            signFound = False
        else:
             wallFollower()
        print("target not found")
        heading_kp = 0.5
    

# start init
init()
sound.set_volume(75)
steeringInit = int(steeringMotor.position + 62)
    
print('press to start')
sound.beep()
while button.right != True:
    time.sleep(0.1)
# wait for start

steeringMotor.on_to_position(SpeedPercent(100),steeringInit)
time.sleep(0.5)
gyroInit = gyro.angle
print('press up to go')
sound.beep()
# Read and display data until TouchSensor is pressed
while not button.enter:
    # Clear display
    lcd.clear()
    bus = SMBus(3)
    print("smbus ok(v2)")
    # Request block
    bus.write_i2c_block_data(address, 0, data)
    # Read block
    block = bus.read_i2c_block_data(address, 0, 20)
    # Extract data
    sig = block[7]*256 + block[6]
    x = block[9]*256 + block[8]
    y = block[11]*256 + block[10]
    w = block[13]*256 + block[12]
    h = block[15]*256 + block[14]
    # Scale to resolution of EV3 display:
    # Resolution Pixy2 while color tracking; (316x208)
    # Resolution EV3 display: (178x128)
    signPathing(int(w*h))
    if(button.up):
        driveMotor.on(SpeedPercent(25))
    elif(button.down):
        driveMotor.on(SpeedPercent(0))
    
    x *= 0.6
    y *= 0.6
    w *= 0.6
    h *= 0.6
    # Calculate rectangle to draw on display
    dx = int(w/2)
    dy = int(h/2)
    xa = x - dx
    ya = y + dy
    xb = x + dx
    yb = y - dy
    # Draw rectangle on display
    lcd.draw.rectangle((xa, ya, xb, yb), fill='black')
    # Update display to how rectangle
    lcd.update()
