from BehaviourTask import BehaviourTask
from head.HeadCentre import HeadCentre
from head.HeadLocalise import HeadLocalise
from head.HeadTrackBall import HeadTrackBall
from util.GameStatus import GameState, GamePhase, game_state, game_phase
from util.Global import usingGameSkill, getCurrentSkill
from util.GameStatus import we_are_kicking_team, penalised


class MainHeadSkill(BehaviourTask):
    def _initialise_sub_tasks(self):
        self._sub_tasks = {
            "TrackBall": HeadTrackBall(self),
        }

    def _reset(self):
        self._current_sub_task = "TrackBall"

