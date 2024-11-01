from util.actioncommand import crouch

from BehaviourTask import BehaviourTask


class Crouch(BehaviourTask):
    def _tick(self):
        self.world.b_request.actions.body = crouch()