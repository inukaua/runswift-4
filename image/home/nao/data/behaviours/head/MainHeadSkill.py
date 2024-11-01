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
    SONG_LENGTH = 30 * (10**6)
    current_timer = Timer(SONG_LENGTH).start()
    
    def _initialise_sub_tasks(self):
        self._sub_tasks = {
            "Challenge1": KSI(self),
            "Challenge2": HeadTrackBall(self),
        }

    def _reset(self):
        self._current_sub_task = "Challenge1"

    def _tick (self):
        self._tick_sub_task

    def _transition(self):
        if self.current_timer.finished():
            self._current_sub_task = "Challenge2"
