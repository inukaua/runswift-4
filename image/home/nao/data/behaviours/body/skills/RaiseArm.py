from util.actioncommand import raiseArm

from BehaviourTask import BehaviourTask


class RaiseArm(BehaviourTask):
    def _tick(self):
        self.world.b_request.actions.body = raiseArm()