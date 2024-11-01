from BehaviourTask import BehaviourTask

from head.HeadCentre import HeadCentre
from head.HeadLocalise import HeadLocalise

from util.Timer import Timer
from util.Global import usingGameSkill, getCurrentSkill
from util.GameStatus import whistle_detected


from head.KSI import KSI
from head.HeadBop import HeadBop
from head.HeadTrackBall import HeadTrackBall 
from head.Challenge3 import Challenge3 


class MainHeadSkill(BehaviourTask):
    SONG_LENGTH = 30 * (10**6)
    song_timer = Timer(SONG_LENGTH).start()
    
    def _initialise_sub_tasks(self):
        self._sub_tasks = {
            "Challenge1": KSI(self),
            "Challenge2": HeadTrackBall(self),
            "Centre": HeadCentre(self),
            "HeadBop": HeadBop(self)
        }

    def _reset(self):
        self._current_sub_task = "Challenge2"
        self._is_first_time_scan = True

    def _tick (self):
        self._tick_sub_task

    def _transition(self):
        
        # Jennifer's task
        #self._current_sub_task = "Centre"
        #self._current_sub_task = "HeadBop"
            
        if self.song_timer.finished():
            self._current_sub_task = "Challenge2"
