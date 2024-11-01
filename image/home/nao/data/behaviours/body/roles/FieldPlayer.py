import robot
from util.Timer import WallTimer
from util import LedOverride
from body.skills.BlockIntercept import BlockIntercept
from BehaviourTask import BehaviourTask

from body.skills.FindAndPass import FindAndPass
from body.skills.Stand import Stand 

class FieldPlayer(BehaviourTask):
    def _initialise_sub_tasks(self):
        self._sub_tasks = {
            "Set": Stand(self),
            "Pass": FindAndPass(self),
        }

    def _reset(self):
        print("STARTED!")
        self._current_sub_task = "Pass"
    
    def _transition(self):
        print("Transition In FieldPlayer")
        pass

    def _tick(self):
        print("ticking FieldPlayer")
        self._tick_sub_task()


