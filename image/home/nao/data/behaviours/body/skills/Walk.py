from BehaviourTask import BehaviourTask
from util.actioncommand import walk
from util.ObstacleAvoidance import sonar_left_obstacle, sonar_right_obstacle


class Walk(BehaviourTask):

    """
    Description:
    Skill associated with directly creating the walk actioncommand.
    SPEED should be increased for serious games.
    """

    # Range between 0.0 and 1.0. Use 0 in lab and 1 in serious games. v5 robots
    # do not work with low speed - 0.5 is functional. v6 need further testing.
    #
    # Lower speeds can be good sometimes, e.g. if the carpet/astroturf is really slippery
    # e.g. in Thailand 2022 a value of 0.4 on v6s was used
    # as any higher and the robots just fell over all the time
    # if the robot falls over in regular walking, then it'll be far slower going from point A to B
    # for logic when no config set see default value of walk_speed in options.cpp

    def _tick(self, forward=0, left=0, turn=0, speed=1.0, allow_shuffle=True, cap_speed=True):
        # Problems:
            # figure out how to deal with no config set
            # figure out interactions between other higher level walk functions
            # Is the config a max speed? Do higher levels overwrite

        if cap_speed:
            speed = min(self.world.blackboard.behaviour.walkSpeed, speed)

        useShuffle = sonar_left_obstacle() or sonar_right_obstacle() if allow_shuffle else False

        self.world.b_request.actions.body = walk(
            forward=forward,
            left=left,
            turn=turn,
            speed=speed,
            useShuffle=useShuffle,
            leftArmBehind=False,
            rightArmBehind=False,
        )
