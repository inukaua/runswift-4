import robot
from BehaviourTask import BehaviourTask
from body.skills.Stand import Stand
from util.GameStatus import (
    GameState,
)
from util.Constants import LEDColour, KICKOFF_MIN_WAIT
from audio.whistle_controller import kill_all_python_processes, start_listening_for_whistles
from util.Timer import Timer
from body.skills.FindAndPass import FindAndPass

class Game(BehaviourTask):

    """
    Description:
    A skill to deal with a game environment.
    """

    # Colours to display on chest for each GC state.
    GC_STATE_TO_CHEST_LED_MAP = {
        GameState.INITIAL: LEDColour.off,
        GameState.STANDBY: LEDColour.cyan,
        GameState.READY: LEDColour.blue,
        GameState.SET: LEDColour.yellow,
        GameState.PLAYING: LEDColour.green,
        GameState.FINISHED: LEDColour.off,
    }

    def _initialise_sub_tasks(self):
        self._sub_tasks = {
            "Stand": Stand(self),
            "Challenge3": FindAndPass(self),
        }

    def _reset(self):
        self._current_sub_task = "Challenge3"

    def _transition(self):
        pass

    def _tick(self):
        self._tick_sub_task()
