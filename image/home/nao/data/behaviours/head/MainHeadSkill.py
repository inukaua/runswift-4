from BehaviourTask import BehaviourTask

from head.HeadCentre import HeadCentre
from head.HeadLocalise import HeadLocalise

from head.HeadTrackBall import HeadTrackBall 
from head.Challenge3 import Challenge3 
from util.Timer import Timer
from head.KSI import KSI

from util.GameStatus import GameState, GamePhase, game_state, game_phase
from util.Global import usingGameSkill, getCurrentSkill
from util.GameStatus import we_are_kicking_team, penalised


class MainHeadSkill(BehaviourTask):
    CHALLENGE1_TIME = 30 * (10**6)
    CHALLENGE2_TIME = (30 + 60) * (10**6)
    CHALLENGE3_TIME = (30 + 60 + 60) * (10**6)
    CHALLENGE4_TIME = (30 + 60 + 60 + 60) * (10**6)
    
    def _initialise_sub_tasks(self):
        self._sub_tasks = {
            "Challenge1": KSI(self),
            "Challenge2": HeadTrackBall(self),
            "Challenge3": HeadCentre(self),
            "Challenge4": HeadCentre(self),
        }

    def _reset(self):
        current_timer = Timer().start()    
        self._current_sub_task = "Challenge1"

    def _tick (self):
        self._tick_sub_task

    def _transition(self):
        if self.current_timer.elapsed < self.CHALLENGE1_TIME:
            self._current_sub_task = "Challenge1"
        elif self.current_timer.elapsed < self.CHALLENGE2_TIME:
            self._current_sub_task = "Challenge2"
        elif self.current_timer.elapsed < self.CHALLENGE3_TIME:
            self._current_sub_task = "Challenge3"
        elif self.current_timer.elapsed < self.CHALLENGE4_TIME:
            # TODO: Add task 4
            self._current_sub_task = "Challenge4"
        else:
            self._current_sub_task = "Stand" 