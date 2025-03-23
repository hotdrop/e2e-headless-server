import time
from actions.base import BaseAction

class WaitAction(BaseAction):
    def execute(self, page):
        seconds = self.step.get("seconds", 1)
        time.sleep(seconds)
        return {"status": "executed"}