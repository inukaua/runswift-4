from BehaviourTask import BehaviourTask
from body.skills.Walk import Walk

class WalkInLine(BehaviourTask):
    """
        Description:
            Walk in a straight line.
    """

    def _initialise_sub_tasks(self):
        self._sub_tasks = {"Walk": Walk(self)}

    def _reset(self):
        self._current_sub_task = "Walk"

    def _tick(self):
        self._tick_sub_task(forward=50)

# def _tick(self, forward=0, left=0, turn=0, speed=1.0, allow_shuffle=True, cap_speed=True):

