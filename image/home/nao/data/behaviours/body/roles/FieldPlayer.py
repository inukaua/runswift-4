import robot
from importlib import import_module
from util.Global import (
    ballLostTime,
    ballDistance,
    myPos,
    egoBallDistance,
    egoBallWorldPos,
    myHeading,
    timeSinceLastTeamBallUpdate,
    ballWorldPos,
)
from util.TeamStatus import (
    teammate_ego_ball,
    get_teammate_seconds_since_last_ball_update,
    i_kicked_the_ball_last,
    player_numbers_playing_ball,
    assistance_is_needed,
    player_numbers_assisting,
    my_player_number,
    get_teammate_pos,
    get_kick_off_target,
    check_teammate_already_kick_off,
    LEFT_KICK_OFF_TARGET,
    RIGHT_KICK_OFF_TARGET,
    teammate_is_near_centre_circle,
    get_teammate_heading,
    player_is_playing_ball,
    player_one_is_field_player,
    get_active_player_numbers,
)
from util.Vector2D import Vector2D
from BehaviourTask import BehaviourTask
from body.skills.Shoot import Shoot
from body.skills.Boot import Boot
from body.skills.Anticipate import Anticipate
from body.skills.FindBall import FindBall
from body.skills.TeamFindBall import TeamFindBall
from body.skills.BlockPushingFreeKick import BlockPushingFreeKick
from body.skills.BlockGoalFreeKick import BlockGoalFreeKick
from body.skills.BlockCornerKick import BlockCornerKick
from body.skills.Ready import Ready
from body.skills.Stand import Stand
from body.skills.Pass import Pass
from body.skills.WalkToPoint import WalkToPoint
from body.skills.MoveOutOfGoaliesWay import MoveOutOfGoaliesWay
from util.Constants import FIELD_LENGTH, PENALTY_AREA_LENGTH, CENTER_CIRCLE_DIAMETER, LEDColour
from util.GameStatus import (
    in_goal_kick,
    in_pushing_free_kick,
    in_corner_kick,
    in_kick_in,
    in_ready,
    in_set,
    we_are_kicking_team,
)
from util.FieldGeometry import (
    ENEMY_GOAL_BEHIND_CENTER,
    ball_near_our_goal,
    calculateTimeToReachBall,
    calculateTimeToReachPose,
)
from util.Timer import WallTimer
from util import LedOverride
from body.skills.BlockIntercept import BlockIntercept

OPPONENT_GOAL_CENTRE = Vector2D(FIELD_LENGTH / 2, 0)
KICK_OFF_MIN_DISTANCE = CENTER_CIRCLE_DIAMETER / 2 - 200
CENTER_DIVE_THRES = 200
DANGEROUS_BALL_THRES = 300
DIVE_VEL_THRES = 50
FREE_KICK_TARGET = ENEMY_GOAL_BEHIND_CENTER.add(Vector2D(0, 200))


class FieldPlayer(BehaviourTask):
    def _initialise_sub_tasks(self):
        self._sub_tasks = {
            "Set": Stand(self)
        }

    def _reset(self):
        self._current_sub_task = "Set"

    def _tick(self):
        pass
