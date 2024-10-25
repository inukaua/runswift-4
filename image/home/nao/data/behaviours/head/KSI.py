from BehaviourTask import BehaviourTask
from util.actioncommand import head
from math import radians
from util.Global import ballHeading, ballDistance


import os


class KSI(BehaviourTask):
    CLOSE_DISTANCE = 800.0

    BEHIND_ANGLE = radians(60)

    def _reset(self):
        os.system(f"espeak -a 100 -vf5 -p75 -g20 -m \"Hey guys\" &")
        os.system(f"aplay KSI.wav")
        pass
        # Play the song

    def _tick(self):
        yaw = ballHeading()
        pitch = self.PITCH_CLOSE if ballDistance() < self.CLOSE_DISTANCE else self.PITCH_FAR
        pitch = self.PITCH_BEHIND if abs(yaw) > self.BEHIND_ANGLE else pitch


        self.world.b_request.actions.head = head(yaw, pitch, False, 0.50, 0.2)