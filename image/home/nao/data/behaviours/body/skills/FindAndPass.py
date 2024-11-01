from util.actioncommand import stand
from util.actioncommand import walk
from util.Global import myPos, myHeading, ballRelPos
from body.skills.Stand import Stand
from body.skills.Walk import Walk

import numpy as np

from BehaviourTask import BehaviourTask
from math import radians


class FindAndPass(BehaviourTask):
    """
        Description: Kick ball to othr robot
        
        Detect the ball and target robot. Position self to be aligned with
        target robot and ball (collinear). Walk to kicking distance. Kick ball.

        The hardest part of this challenge is actually detecting the robot. There are a number of possible approaches (Sonar, Localisation + network packets), but the one we opted to take here is to use the robot's RobotVisionInfo blackboard variable which provides the detected robot's relative coordinates, including the heading.
        
        Using `self.world.blackboard.vision.robots.rr.heading`, we align the robot so the rr heading is 0 (i.e. the robot is facing the )
    """  

    def _initialise_sub_tasks(self):
        self._sub_tasks = {
            "Stand": Stand(self),
            "Walk": Walk(self),
        }


    def _reset(self):
        self._current_sub_task = "Stand"
        print("Started FindAndPass!")
        self.close = False
        self.position_aligned = False  # The kick_foot's position is colinear \
        # with the kick_target and ball
        self.heading_aligned = False  # The robot is facing kick_target
        self.n = 20
        self.last_n_detections = np.array([0] * self.n)
        self.detections = 0
        self.detected = False



    def _tick(self,
              forward = 150,
              distance_error=50,
              heading_error=radians(10),
              ):
        
        self._tick_sub_task()

        my_pos = myPos()
        my_heading = myHeading() 

        try:
            self.robot_heading = self.world.blackboard.vision.robots[0].rr.heading
            self.robot_distance = self.world.blackboard.vision.robots[0].rr.distance
            self.detections += 1
            # Keep track of the last 5 detections
            
            print(f"I see you (at {self.robot_heading / (3.14/180)} degrees and distance {self.robot_distance})")
        except:
            try:
                self.robot_heading == 1 # test whether robot heading exists
                if (self.robot_distance) < 100:
                    self.world.b_request.actions.body = stand(0)
                    print(f"Standing")
                else:
                    print(f"Walking")
                    self.world.b_request.actions.body = walk(forward, 0, 0.3*self.robot_heading)
            except:
                    print(f"Standing")
                    self.world.b_request.actions.body = stand(0)