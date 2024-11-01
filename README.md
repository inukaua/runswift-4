[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repo contains Team 4's challenge solutions. 

## Challenge 1 (Jennifer):
For task 1, we decided to attempt an added layer of complexity to the dance by transitioning between different skills using the in-built whistle detection within a Dance.py skill. Taking a look at whistle_detector.py and learning the way it worked, my first attempt was to at initilisation, count the number of initials files in the found_whistle directory using os.listdir(), and then at every tick, calculate the number of whistles found since the start of the program. This in theory would allow us to keep track of the numbered whistle we were up to and transition between skills accordingly.
Another attempt was to simply use the dictionary of self._current_sub_tasks to get the 'index' of the current subtask, and then increment it to be the next task, until the last task switched over to the first task. 
Finally, another attempt involved the use of a timer, initialised at the start and then checked whether self._timer.elapsed() fell within a certain range, for then the skill to switch.

For the acutal skills used within Dance, I took inspiration for Crouch and Raise Arm from the 2024 release, and Spin simply used the Walk skill however with just the turn parameter.
Additionally, I had created a head skill named HeadBop which adjusted the pitch to continuously move the head up and down, using a sinusodial function to calculate the next pitch, while the yew was set to 0 and relied on FixedHeadYewAndPitch. This was to be called everytime found_whistle() was set true, which was when a whistle was detected within the last three seconds.

The audio playing on the system was explored by Inuka who copied the file over to the robot and used a system command to play the wav file.

-- Jennifer

Relevant files:
- image/home/nao/data/behaviours/head/KSI.py
- image/home/nao/data/behaviours/body/skills/Dance.py

## Challenge 2 (Ishita):
For task 2, we scoured the code base for an existing function that allowed the behaviour of the robot's head to track the ball. Found HeadTrackBall function in Head/Skills. From here I edited the behaviour itself to not tilt the yaw and only pitch. Then from MainHeadSkills, the entry point for the head behaviour - I edited it and only called the HeadTrackBall function. Thus, after testsing, the task was succesfully completed. The robot followed a soccer ball on the floor as it was moved around with minimal lag - only moving its head sideways.

-- Ishita

Relevant files:
- image/home/nao/data/behaviours/head/HeadTrackBall.py

## Challenge 3 (Inuka):
The challenge was to pass the ball to another robot. In the end, we used the RobotVisionInfo struct (e.g. RR heading and distance which is relative polar coordinates of detected robots w.r.t self robot) to find the robot's heading. When a robot is detected, the nao walks forward with the turn rate set to the heading towards the robot, causing it to approach the other robot. To make this information accessible from the python codebase, we added a blackboard wrapper for `VisionBlackboard::robots`. Webnao was used to test vision and adjust camera parameters to improve robot detection (increasing brightness was sufficient to get a good level of consistency).

-- Inuka

Relevant files:
- image/home/nao/data/behaviours/body/skills/FindAndPass.py
- robot/perception/behaviour/python/wrappers/VisionBlackboard_wrap.cpp

## Challenge 4 (Ishita, Eric)
For task 4 I began with using the FindBall function that already existed, which would make the robot move to where it thinks the ball is. I then implemented an if statement using the _should_go_to_ball function from FindBall that makes the robot stop moving once it reaches a certain distance from the ball. Then I made the robot do a 90 degree turn, this was done by using the walk function to make it turn left for a certain period of time until it had done a 90 degree turn, this was done to ensure that the robot could then walk in a circle clockwise without running into the ball. Once turn complete I made the robot raise its arm to point at the ball, this was done by editing the raiseArm.pos file. Then I used the code from walk in circle that we had done in week 2 to make it walk around the ball with the distance between the ball and the robot being the radius.

-- Eric

Relevant files:
- image/home/nao/data/behaviours/body/skills/WalkToBallCirclePoint.py


