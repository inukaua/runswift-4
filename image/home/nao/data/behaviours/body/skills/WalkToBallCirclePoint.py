from BehaviourTask import BehaviourTask
from body.skills.FindBall import FindBall
from body.skills.CircularPath import CircularPath
from body.skills.Stand import Stand

from util.actioncommand import walk, stand, raiseArm
from util.Global import ballDistance
from util.Timer import Timer
from util.CircularMotion import angular_velocity
from util.GameStatus import in_corner_kick, we_are_kicking_team, in_goal_kick, in_kick_in, in_pushing_free_kick


class WalkToBallCirclePoint(BehaviourTask):
    """
    Skill that walks to ball, circles around and points at it, and says "I found the ball!"
    """

    def _initialise_sub_tasks(self):
        self._sub_tasks = {
            "FindBall": FindBall(self),
            "CircularPath": CircularPath(self),
            "Stand": Stand(self)
        }
    
    def _reset(self):
        self._current_sub_task = "FindBall"
        self.my_timer = Timer()
        self.my_timer.start()
        self.radius = 500
        self.forward = 0
        self.clockwise = False
                
    def _tick(self):
        if self._current_sub_task == "FindBall":
            self._tick_sub_task()
            if self._should_go_to_ball() == False:
                self._current_sub_task == "Stand"
        
        if self._current_sub_task == "Stand":
            turn = angular_velocity(self.radius, self.forward) * (-1 if self.clockwise else 1)
            self.world.b_request.actions.body = walk(self.forward, 0, turn)
            if self.my_timer.elapsed() == 1000000:
                self.world.b_request.actions.body = stand()
                self.world.b_request.actions.body = raiseArm()
                self._current_sub_task = "CircularPath"
                
        if self._current_sub_task == "CircularPath":
            self._tick_sub_task()

    def _should_go_to_ball(self):
        ball_distance = ballDistance()

        # If we're in a free kick and opponent is kicking, and we
        # go into findball, dont go to within 1000mm of where
        # you think the ball is
        # https://youtu.be/8IOcv4ZqKu4?t=2185
        if in_goal_kick() or in_corner_kick() or in_kick_in() or in_pushing_free_kick():
            if not we_are_kicking_team():
                if ball_distance < 1000:
                    return False

        # If we've got close to the ball, no need to go to
        # ball anymore
        if ball_distance < 500:
            return False
        return True