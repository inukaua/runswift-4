from BehaviourTask import BehaviourTask
from util.actioncommand import head
from util.Global import ballHeading, ballDistance


import math
from math import radians
import os
import time


class KSI(BehaviourTask):
    CLOSE_DISTANCE = 800.0
    BEHIND_ANGLE = radians(60)
    EQUILIBRIUM = 0
    AMPLITUDE = 0

    def _reset(self):
        self.PITCH_BEHIND = radians(19)
        self.PITCH_CLOSE = radians(19 + self.world.blackboard.kinematics.parameters.cameraPitchBottom)
        self.PITCH_FAR = radians(19 + self.world.blackboard.kinematics.parameters.cameraPitchBottom)

        self.EQUILIBRIUM = (self.PITCH_BEHIND + self.PITCH_CLOSE)/2
        self.AMPLITUDE = abs((self.PITCH_BEHIND - self.PITCH_CLOSE)/2)
        
        #os.system(f"espeak -a 100 -vf5 -p75 -g20 -m -f ~/data/thick_of_it_lyrics.txt &")
        #os.system(f"aplay ~/data/KSI.wav &")
        # Play the song

    def _tick(self):
        yaw = ballHeading()
        pitch = self.AMPLITUDE * math.sin(time.time()) + self.EQUILIBRIUM

        print(pitch)

        self.world.b_request.actions.head = head(yaw, pitch, False, 0.50, 0.2)