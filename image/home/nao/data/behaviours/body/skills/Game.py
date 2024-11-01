import robot
from BehaviourTask import BehaviourTask
from body.roles.FieldPlayer import FieldPlayer
from body.skills.Stand import Stand
from util.GameStatus import (
    in_initial,
    in_finished,
    in_standby,
    penalised,
    game_state,
    prev_game_state,
    GameState,
    whistle_detected,
)
from util.Constants import LEDColour, KICKOFF_MIN_WAIT
from audio.whistle_controller import kill_all_python_processes, start_listening_for_whistles
from util.Timer import Timer
from util.GameStatus import in_set, secs_till_unpenalised


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
            "FieldPlayer": FieldPlayer(self),
            "Stand": Stand(self),
        }

    def _reset(self):
        self._current_sub_task = "Stand"
        self._kick_off_timer = Timer(KICKOFF_MIN_WAIT)
        self._last_said_number = None

    def _transition(self):
        if penalised() or in_initial() or in_standby() or in_finished():
            self._current_sub_task = "Stand"
        else:
            self._current_sub_task = "FieldPlayer"

    def _tick(self):
        # Chest led must follow the rules in the rulebook
        if penalised():
            self.world.b_request.actions.leds.chestButton = LEDColour.red
        else:
            self.world.b_request.actions.leds.chestButton = self.GC_STATE_TO_CHEST_LED_MAP[game_state()]

        # Update kick off timer
        if prev_game_state() is GameState.SET and game_state() is GameState.PLAYING:
            # If we acted through the whistle, we start a timer
            if whistle_detected():
                self._kick_off_timer.restart()
                self.world.in_kick_off_wait_time = True
            # If we didn't hear a whistle, we got the "PLAYING" packet
            # from GC, we should immediately start playing
            else:
                self.world.in_kick_off_wait_time = False
        if self.world.in_kick_off_wait_time and self._kick_off_timer.finished():
            self.world.in_kick_off_wait_time = False

        # Tick sub task!
        self._tick_sub_task()

