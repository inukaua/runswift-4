from BehaviourTask import BehaviourTask
from util.actioncommand import head
from math import radians
from util.Global import ballHeading, ballDistance


class Challenge3(BehaviourTask):
    CLOSE_DISTANCE = 800.0

    BEHIND_ANGLE = radians(60)

    def _reset(self):
        self.PITCH_BEHIND = radians(19)
        self.PITCH_CLOSE = radians(19 + self.world.blackboard.kinematics.parameters.cameraPitchBottom)
        self.PITCH_FAR = radians(19 + self.world.blackboard.kinematics.parameters.cameraPitchBottom)

    def _tick(self):
        yaw = ballHeading()
        pitch = self.PITCH_CLOSE if ballDistance() < self.CLOSE_DISTANCE else self.PITCH_FAR
        pitch = self.PITCH_BEHIND if abs(yaw) > self.BEHIND_ANGLE else pitch

        self.world.b_request.actions.head = head(yaw, pitch, False, 0.50, 0.2)
