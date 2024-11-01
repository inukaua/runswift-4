from BehaviourTask import BehaviourTask
from head.HeadCentre import HeadCentre
from head.HeadLocalise import HeadLocalise
from head.HeadBop import HeadBop
from util.GameStatus import whistle_detected


class MainHeadSkill(BehaviourTask):
    def _initialise_sub_tasks(self):
        self._sub_tasks = {
            "Centre": HeadCentre(self),
            "HeadBop": HeadBop(self),
        }

    def _reset(self):
        self._current_sub_task = "Centre"
        self._is_first_time_scan = True

    def _transition(self):
        # don't know how this whistle detected is calculated
        if whistle_detected():
            self._current_sub_task = "HeadBop"
        else:
            self._current_sub_task = "Centre"
