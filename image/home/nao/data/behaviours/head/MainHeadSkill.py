from BehaviourTask import BehaviourTask
from head.HeadTrackBall import HeadTrackBall 
from util.Timer import Timer
from head.KSI import KSI
from util.GameStatus import GameState, GamePhase, game_state, game_phase
from util.Global import usingGameSkill, getCurrentSkill
from util.GameStatus import we_are_kicking_team, penalised


class MainHeadSkill(BehaviourTask):
    SONG_LENGTH = 30 * (10**6)
    countdown_timer = Timer(SONG_LENGTH).start()
    
    def _initialise_sub_tasks(self):
        self._sub_tasks = {
            "Challenge2": HeadTrackBall(self),
            "Challenge1": KSI()
        }

    def _reset(self):
        self._current_sub_task = "Challenge1"
        self._is_first_time_scan = True

    def _tick (self):
        from util.Timer import Timer


    def _transition(self):
        if self.countdown_timer.finished():
            self._current_sub_task = "Challenge2"