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
            "Anticipate": Anticipate(self),
            "FindBall": FindBall(self),
            "TeamFindBall": TeamFindBall(self),
            "Shoot": Shoot(self),
            "Boot": Boot(self),
            "Ready": Ready(self),
            "Set": Stand(self),
            "BlockGoalFreeKick": BlockGoalFreeKick(self),
            "BlockPushingFreeKick": BlockPushingFreeKick(self),
            "KickOffCharge": WalkToPoint(self),
            "Pass": Pass(self),
            "BlockCornerKick": BlockCornerKick(self),
            "BlockKickIn": BlockPushingFreeKick(
                self
            ),  # its pretty much the same as what we do in a pushing free kick, right?  # noqa
            "MoveOutOfGoaliesWay": MoveOutOfGoaliesWay(self),
            "KickOffBlock": BlockIntercept(self),
        }

    def _reset(self):
        self._current_sub_task = "Anticipate"
        self._my_player_number = my_player_number()
        self._kick_timer = None
        self._already_kick_off = False
        self._create_positioning()
        self._crouched = False

    def _transition(self):
        # Ready check
        if in_ready():
            self._current_sub_task = "Ready"
            self._already_kick_off = False

        # Set check
        elif in_set():
            self._current_sub_task = "Set"
            self._already_kick_off = False

        # kick off check
        elif self._in_kick_off() and not self._already_kick_off:
            if we_are_kicking_team():
                if self._should_kick_off_charge():
                    self._current_sub_task = "KickOffCharge"
                else:
                    self._already_kick_off = True
            else:
                self._current_sub_task = "KickOffBlock"
                if self._defensive_kick_off_started():
                    self._already_kick_off = True
        elif my_player_number() > 1 or self._should_play_ball():
            self.world.b_request.behaviourSharedData.playingBall = True

            if self._should_block_goal_kick():
                self._current_sub_task = "BlockGoalFreeKick"
            elif self._should_block_corner_kick():
                self._current_sub_task = "BlockCornerKick"
            elif self._should_find_ball():
                self.world.b_request.behaviourSharedData.needAssistance = self._need_assistance()
                self._current_sub_task = "FindBall"
            elif self._should_block_pushing_free_kick():
                self._current_sub_task = "BlockPushingFreeKick"
            elif self._should_block_kick_in():
                self._current_sub_task = "BlockKickIn"
            elif self._should_kick_off_play():
                self._current_sub_task = "Pass"
            elif player_is_playing_ball(1) and not player_one_is_field_player():  # if goalie is playing
                self._current_sub_task = "MoveOutOfGoaliesWay"
            elif self._should_take_free_kick():
                self._current_sub_task = "Shoot"
            elif self._should_boot():
                self._current_sub_task = "Boot"
            else:
                self._current_sub_task = "Shoot"
        # elif self._should_team_find_ball():
            # self._current_sub_task = "TeamFindBall"

        elif self._should_provide_assistance():
            self.world.b_request.behaviourSharedData.isAssisting = True
            if self._should_block_goal_kick():
                self._current_sub_task = "BlockGoalFreeKick"
            elif self._should_block_pushing_free_kick():
                self._current_sub_task = "BlockPushingFreeKick"
            elif self._should_take_free_kick():
                self._current_sub_task = "Shoot"
            elif self._should_boot():
                self._current_sub_task = "Boot"
            else:
                self._current_sub_task = "Shoot"
        else:
            self._current_sub_task = "Anticipate"

    def _tick(self):
        if self._in_kick_off():
            self.world.b_request.behaviourSharedData.isKickedOff = self._already_kick_off

        # Tick Sub Task

        # print self._current_sub_task

        if self._current_sub_task == "Anticipate":
            # Evaluate the new positioning
            self._positioning.evaluate()
            # Transmit what your role is going to be
            self.world.b_request.behaviourSharedData.role = self._positioning.get_my_role_enum()

            # Crouch if ball is close, stand if ball is far away
            if self._crouched:
                if ballDistance() > 3500:
                    self._crouched = False
            else:
                if ballDistance() < 2500:
                    self._crouched = True

            self._tick_sub_task(
                position=self._positioning.get_position(),
                heading=self._positioning.get_heading(),
                position_error=self._positioning.get_position_error(),
                dist_to_face_final_heading=1500,  # face final heading if we're within 1500mm of the final position  # noqa
                speed=1.0,
                stay_crouched=self._crouched,
            )
        elif self._current_sub_task == "Ready":
            self._tick_sub_task()
        elif self._current_sub_task == "KickOffCharge":
            charge_pos, _ = get_kick_off_target()
            if charge_pos is None:
                self._tick_sub_task(speed=1.0)
            else:
                self._tick_sub_task(charge_pos, 0, speed=1.0)
        else:
            if self._current_sub_task in ("Shoot", "Boot", "Pass"):
                if self._sub_tasks[self._current_sub_task].has_finished_kick:
                    self._kick_timer = WallTimer()  # this resets the timer
            if self._current_sub_task == "Pass":
                if self._should_kick_off_play():
                    _pass_target, _ = get_kick_off_target()
                    if _pass_target is None:
                        _pass_target = RIGHT_KICK_OFF_TARGET
                    elif _pass_target.y > 0:
                        _pass_target = LEFT_KICK_OFF_TARGET
                    else:
                        _pass_target = RIGHT_KICK_OFF_TARGET
                    # Don't allow aborting, because we often lose sight of
                    # the ball on the centre line because of balldetection
                    # failure. So, don't abort, just take a swing!
                    self._tick_sub_task(pass_target=_pass_target, can_abort=False)
                else:
                    self._tick_sub_task()
            else:
                self._tick_sub_task()

        # If kick timer is None, we haven't kicked yet. The defaults values of
        # these variables assume the ball hasn't been kicked yet, so we should
        # overwrite them if we have kicked the ball
        if self._kick_timer:
            self.world.b_request.behaviourSharedData.secondsSinceLastKick = int(self._kick_timer.elapsedSeconds())

            # Keep notifying others if we have kicked in the last two seconds.
            # Check if the kickNotification has already been set by skills such
            # as Kick.py or ApproachBall.py
            if not self.world.b_request.behaviourSharedData.kickNotification:
                self.world.b_request.behaviourSharedData.kickNotification = self._kick_timer.elapsedSeconds() < 1.0

        if self.world.b_request.behaviourSharedData.playingBall:
            LedOverride.override(LedOverride.leftEye, LEDColour.red)
        elif self.world.b_request.behaviourSharedData.isAssisting:
            LedOverride.override(LedOverride.leftEye, LEDColour.blue)
        else:
            LedOverride.override(LedOverride.leftEye, LEDColour.off)

    def _should_boot(self):
        if ball_near_our_goal():
            return True
        return False

    def _should_find_ball(self):
        if ballLostTime() > 2.0:
            return True
        return False

    def _need_assistance(self):
        if ballLostTime() > 2.0:
            return True
        return False

    def _should_play_ball(self):
        """
        Whether or not robot should be playing the ball, depending
        on time to reach ball.
        """

        near_our_goal = ballWorldPos().x < -FIELD_LENGTH / 2 + PENALTY_AREA_LENGTH + 1000

        for player in player_numbers_playing_ball():
            # If its me, ignore it.
            if player is self._my_player_number:
                continue

            # Just because goalie is playing the ball, we don't want to switch
            # out of ballPlayer (because then we can have up to 4 anticipators,
            # which causes undefined behaviour in our current positioning). So,
            # we keep the closest FieldPlayer as a ballPlayer, and deal with
            # preventing clashing inside ball player behaviour.
            # If goalie is playing as a field player, then we don't go into
            # this if statement.
            if player == 1 and not player_one_is_field_player():
                continue

            if get_teammate_seconds_since_last_ball_update(player) > 1.5:
                ball = ballWorldPos()
            else:
                ball = teammate_ego_ball(player)

            teammate_ttrb = calculateTimeToReachPose(get_teammate_pos(player), get_teammate_heading(player), ball)
            my_ttrb = calculateTimeToReachBall(myPos(), myHeading())

            if near_our_goal:
                if get_teammate_pos(player).x < ball.x and myPos().x >= ball.x:
                    # The other robot is behind the ball and I am infront. They should be the ball player
                    return False
                elif get_teammate_pos(player).x >= ball.x and myPos().x < ball.x:
                    # The other robot is infront the ball and i am behind.
                    # I should be the ball player (provided we don't find a better option)
                    continue
                else:
                    # We are both infront or behind the ball between the ball and the goal.
                    # Whoever is closer should be the ball player
                    if teammate_ttrb < my_ttrb:
                        return False

            else:
                # If another ball player is closer to the ball, i shouldn't play
                # the ball
                if teammate_ttrb < my_ttrb:
                    return False

        # if there are no suitable players for playing the ball,
        # i have to play the ball
        return True

    def _should_provide_assistance(self):
        """
        Whether or not robot should be providing assistance to ball
        player that hasn't seen the ball in a while. BallPlayer might
        have its vision to the ball obstructed, or is chasing the team
        ball while mislocalised
        """

        # Don't assist if you're not asked to
        if not assistance_is_needed():
            return False

        # If I kicked the ball last, I should go and find it
        if i_kicked_the_ball_last():
            return True

        # If I haven't seen the ball recently, don't assist
        if ballLostTime() > 1.5:
            return False

        for player in player_numbers_assisting():
            # If its me, ignore it.
            if player is self._my_player_number:
                continue

            # If another robot is closer to the ball and is providing
            # assistance, I shouldn't
            teammate_ttrb = calculateTimeToReachBall(get_teammate_pos(player), get_teammate_heading(player))
            my_ttrb = calculateTimeToReachBall(myPos(), myHeading())
            if teammate_ttrb < my_ttrb:
                return False

        return True

    def _in_kick_off(self):
        if self.world.in_kick_off_wait_time is True:
            return True
        return False

    def _defensive_kick_off_started(self):
        if not self.world.in_kick_off_wait_time:
            return True

        if check_teammate_already_kick_off():
            robot.say("Kick off comfirmed by Teammates")
            return True

        seen_ball_recently = ballLostTime() < 1
        i_am_near_centre_circle = myPos().length() < 1500
        i_am_near_ball = egoBallDistance() < 1000
        if (i_am_near_centre_circle or i_am_near_ball) and seen_ball_recently:
            # Only care about ego ball here
            if egoBallWorldPos().length() > KICK_OFF_MIN_DISTANCE:
                return True
        return False

    def _should_take_free_kick(self):
        return (
            in_goal_kick() or in_pushing_free_kick() or in_corner_kick() or in_kick_in()
        ) and we_are_kicking_team()  # noqa

    def _should_block_goal_kick(self):
        return in_goal_kick() and not we_are_kicking_team()

    def _should_block_pushing_free_kick(self):
        return in_pushing_free_kick() and not we_are_kicking_team()

    def _should_block_corner_kick(self):
        return in_corner_kick() and not we_are_kicking_team()

    def _should_block_kick_in(self):
        return in_kick_in() and not we_are_kicking_team()

    def _get_ball_player_positions(self):
        ball_player_positions = []
        for player in player_numbers_playing_ball():
            ball_player_positions.append(get_teammate_pos(player))
        return ball_player_positions

    def _should_kick_off_charge(self):
        _, target_player = get_kick_off_target()
        if ballDistance() <= 500:
            return False
        if not teammate_is_near_centre_circle():
            return False
        if ballWorldPos().distanceTo(Vector2D(0, 0)) > 1000:
            return False
        if self._my_player_number == target_player:
            return True
        return False

    def _should_kick_off_play(self):
        if not self.world.in_kick_off_wait_time:
            return False
        if not teammate_is_near_centre_circle():
            return False
        if not we_are_kicking_team():
            return False
        return True

    # Function to create the _positioning object, as specified in
    # the configs
    def _create_positioning(self):
        positioning_name = self.world.blackboard.behaviour.positioning
        positioning_path = "positioning." + positioning_name
        positioning_module = import_module(positioning_path)
        PositioningClass = getattr(positioning_module, positioning_name)
        self._positioning = PositioningClass()

    def _should_team_find_ball(self):
        if len(get_active_player_numbers()) == 0:
            return False
        return timeSinceLastTeamBallUpdate() > 8.0  # seconds
