from actions.input import InputAction
from actions.click import ClickAction
from actions.wait import WaitAction
from actions.assert_exists import AssertExistsAction

class ActionFactory:
    @staticmethod
    def create(step: dict):
        action = step.get("action")
        if action == "input":
            return InputAction(step)
        elif action == "click":
            return ClickAction(step)
        elif action == "wait":
            return WaitAction(step)
        elif action == "assertExists":
            return AssertExistsAction(step)
        else:
            raise ValueError(f"Unknown action: {action}")