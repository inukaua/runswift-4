from BehaviourTask import BehaviourTask
from util.actioncommand import walk
from util.ObstacleAvoidance import sonar_left_obstacle, sonar_right_obstacle


class Spin(BehaviourTask):

    """
    Description:
    Skill associated with turning the robot on the spot
    """
    def _tick(self, turn=0, speed=1.0):
        self.world.b_request.actions.body = walk(
            forward=0,
            left=0,
            turn=turn,
            speed=speed,
            useShuffle=False,
            leftArmBehind=False,
            rightArmBehind=False,
        )
