from BehaviourTask import BehaviourTask

from body.skills.Stand import Stand
from body.skills.Walk import Walk
from util.GameStatus import whistle_detected
import os

from body.skills.Crouch import Crouch
from body.skills.RaiseArm import RaiseArm
from body.skills.Spin import Spin
#from whistle_detector import WhistleState

#will create a new file in foundwhistles wen whistle encountered


# relatie to behaviours folder
# run whistle_detector and runswift in different terminals

WHISTLE_PATH = "../../whistles/heard_whistles"



class Dance(BehaviourTask):
    def _initialise_sub_tasks(self):
      self._sub_tasks = {
          "Walk": Walk(self),
          "Stand": Stand(self),
          "Spin": Spin(self),
          "RaiseArm": RaiseArm(self),
          "Crouch": Crouch(self)
      }
      self.start_files = 0
      

    def _reset(self):
      self._current_sub_task = "Stand"
      if not os.path.exists(WHISTLE_PATH):
        return
      index = 0
      self.start_files = len(os.listdir(WHISTLE_PATH))

      

    def _transition(self):
      if whistle_detected():
         self._current_sub_task = self.get_current_task()
      # if (self.count_whistle() % 5 == 0):
      #    self._current_sub_task = "Walk"
      # if (self.count_whistle() % 5 == 1):
      #   self._current_sub_task = "RaiseArm"
      # if (self.count_whistle() % 5 == 2):
      #   self._current_sub_task = "Spin"
      # if (self.count_whistle() % 5 == 3):
      #   self._current_sub_task = "Crouch"
      # if (self.count_whistle() % 5 == 4):
      #     self._current_sub_task = "Stand"
      

   
    def _tick(self):
      print(self._current_sub_task)
      if (self._current_sub_task == "Walk"):
         self._tick_sub_task(forward=10)
      if (self._current_sub_task == "Spin"):
          self._tick_sub_task(turn=10)
      else:
        self._tick_sub_task()
    
    def get_current_task(self):
      keys = list(self._sub_tasks.keys())
      index = keys.index(self._current_sub_task)
      index = index + 1
      if index >= 5:
        index = 0
      return keys[index]


    # def count_whistle(self):
    #   files = os.listdir(WHISTLE_PATH)
    #   return (len(files) - self.start_files)