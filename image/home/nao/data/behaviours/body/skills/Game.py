import robot
from BehaviourTask import BehaviourTask
from body.skills.Stand import Stand
from body.skills.Dance import Dance
from util.Timer import Timer
from body.skills.FindAndPass import FindAndPass
from body.roles.FieldPlayer import FieldPlayer 

from audio.whistle_controller import kill_all_python_processes, start_listening_for_whistles
from util.GameStatus import (
    GameState,
    whistle_detected,
)

class Game(BehaviourTask):

    """
    Description:
    Main entrypoint
    """
    CHALLENGE1_TIME = 30 * (10**6)
    CHALLENGE2_TIME = (30 + 60) * (10**6)
    CHALLENGE3_TIME = (30 + 60 + 60) * (10**6)
    CHALLENGE4_TIME = (30 + 60 + 60 + 60) * (10**6)
    


    def _initialise_sub_tasks(self):
        self._sub_tasks = {
            "Challenge1_Dance": Dance(self),
            "Stand": Stand(self),
            "Challenge3": FindAndPass(self),
            "Challenge4": FieldPlayer(self)
        }

    def _reset(self):
        self.current_timer = Timer().start()
        self._current_sub_task = "Challenge3"

    def _transition(self):
        if self.current_timer.elapsed < self.CHALLENGE1_TIME:
            self._current_sub_task = "Challenge1_Dance"
        elif self.current_timer.elapsed < self.CHALLENGE2_TIME:
            self._current_sub_task = "Stand"
        elif self.current_timer.elapsed < self.CHALLENGE3_TIME:
            self._current_sub_task = "Challenge3"
        elif self.current_timer.elapsed < self.CHALLENGE4_TIME:
            # TODO: Add task 4
            self._current_sub_task = "Challenge4"
        else:
            self._current_sub_task = "Stand" 

    def _tick(self):
        self._tick_sub_task()
