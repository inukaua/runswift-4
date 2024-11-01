import time
from BehaviourTask import BehaviourTask
from util.actioncommand import head
from util.Sensors import angles
from robot import Joints
from math import pi, radians, sin
from util.MathUtil import stdev
from collections import deque


class HeadBop(BehaviourTask):

    """
    Description:
    A headskill associated with moving the head up and down continuously
    """


    def _reset(self):
        self._yaw = 0
        self._pitch = 0
        self._bop_speed = 1.0
        self._start_time = time.time()


    def _tick(self, pitch_amplitude=0.1, bop_speed=1.0):
        # Read in new yaw and pitch aims
        self._bop_speed = bop_speed

        # calculate new pitch based on sin function
        elapsed_time = time.time() - self._start_time
        # 2Pi is one full cycle, multiplied by the speed/frequency and elapsed_time to vary the motion with time
        next_pitch = pitch_amplitude * sin(2 * pi * self._bop_speed * elapsed_time)

        self.world.b_request.actions.head = head(0, next_pitch, False, 0, bop_speed)
