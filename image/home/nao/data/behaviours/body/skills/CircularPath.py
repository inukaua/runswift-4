from BehaviourTask import BehaviourTask
from util.actioncommand import walk
from util.CircularMotion import angular_velocity


class CircularPath(BehaviourTask):

    """
    Description:
    A skill that can be used to test if the calculation for walking
    in a circle is done correct. The robot should walk in a circle
    of given radius, at given forward speed, facing forwards (along
    the tangent).
    """

    def _tick(self, radius=750, forward=150, clockwise=True):
        turn = angular_velocity(radius, forward) * (-1 if clockwise else 1)

        self.world.b_request.actions.body = walk(forward, 0, turn)
