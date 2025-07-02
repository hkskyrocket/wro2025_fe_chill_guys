Brief introduction to our software system
====

This introduction mainly included three parts, Environment of the EV3, Open Challenge and Obstacle Challenge

## Environment of the EV3

At the very beginning of the preparation, we decided not to use the original system on the ev3, instead, we use ev3dev which provides a more powerful environment for coding. ev3dev can set the maximum Hz of the cpu up to 456 Hz and the organ maximum Hz is 375 Hz. It increases our running efficiency very much. Moreover, we can use more powerful languages such as python to write code. At last, we choose to use python as it is easy to pick up and for maintenance. 

To use the ev3dev, we flashed the system to a sd card and put it into the ev3. Next, we download the ev3dev python library for typing ev3dev python codes. Which is the wro2025_fe_chill_guys/src/ev3dev2/ file. This file allows us to directly use the ev3 electrical components such as medium motors. Which minimizes our time to work on coding basic environments. 

After That, we use Microsoft Visual Code Studio to manage our code, to send our code to ev3, we use an extension called EV3DEV Device Browser and bluetooth connection. With the help of the extension and the launch.json file, we can send our program to ev3 wirelessly. 

However, due to the large amount of code in the ev3dev python library, it required lots of time to load the program from our competition. In view of this, we also use ssh connection to communicate with our robot. We use PuTTY to send orders to the robot. We often use the ‘nano’ function which can change the code saved in ev3 directly. It nearly requires zero seconds for us to load the code. Moreover, we often use the ‘brickrun’ function via ssh connection as it can send back data collected to the computer which allows us to quickly find out what is the problem and quickly resolve it.

Nevertheless, as game rule 9.11 said we can only use one start button to start our program after turning on the ev3 and ev3dev required more than one button to start the program. Therefore, we edit the booting document to automatically start our preselected program after turning on the ev3. After the program finished initiation, ev3 will have a beep sound to signal us the robot is ready for competition and we can start our vehicle.


## Open Challenge

As our principle is to make everything as simple as possible, we didn’t use our camera during the Open Challenge. We used an ultrasonic sensor to measure the distance between the wall and the vehicle. However, we found the value is not precise as the heading of the vehicle keeps changing. Therefore, we get our heading from the gyro sensor and by doing some simple maths, we can find the actual distance between the wall and the vehicle, which is actual distance = cosine(heading in degree / 180 degree * pi) * detected distance.

Next, we used two P-controls algorithms, and we got the current heading by a gyro sensor. As the heading is not consistent during the round. After having actual distance and the heading, we use two P-control algorithms to ensure the vehicle has a consistent distance with the wall. We calculate the target heading by (target distance - actual distance with the wall) times heading_kp which we set it to 0.5. Moreover, to prevent losing the moving direction, we set the heading limit between -15 to +15 degrees. If the heading exceeds the limit, the vehicle will automatically correct back to the correct direction by setting the target heading opposite to the current heading. Then, we calculate target steering motor position by (target heading - current heading) times distance_kp which we set it to 1. Furthermore, to prevent the front wheel in contact with other parts of the vehicle which interrupt the forward movement of the vehicle, we set the steering motor position to -45 to +45 unit. If the steering motor position is lower than -45, we will set the steering motor position to -45, and vice versa.

When the colour sensor detects the blue line first, the vehicle will turn left and run a forward direction part of the program after selection, vice versa. To improve the accuracy of turning, we implemented a gyro sensor, once the gyro reading shows it has turned 90 degrees, it will stop turning and go to wall follower mode. After turning once, we will add our moved sessions variable by 1. After the moved sessions reach 12, we will stop at the next session.


## Obstacle Challenge

For the Obstacle Challenge, we use all four sensors. We use a pixy2 camera built-in function which is colour detection to detect the traffic signs as it is easy for both training and access. We calculate the centre of the traffic signs and compare it to the middle of the camera. After having the distance difference, we calculate the target heading and targeting to put green traffic lights to the left of the camera, and vice versa. After moving across the traffic lights, we set our target heading to 0. After that, we detect the blue and orange lines, and we set our vehicle to turning mode. We use the same method in Open Challenge to determine when our vehicle should be stopped.
