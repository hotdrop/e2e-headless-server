from actions.input import InputAction
from actions.click import ClickAction
from actions.wait import WaitAction
from actions.assert_exists import AssertExistsAction
from actions.assert_text import AssertTextAction
from actions.screenshot import ScreenshotAction
from actions.scroll_into_view import ScrollIntoViewAction

class ActionFactory:
    @staticmethod
    def create(site_id: str, step: dict):
        action = step.get("action")
        if action == "input":
            return InputAction(site_id, step) 
        elif action == "click":
            return ClickAction(site_id, step) 
        elif action == "wait":
            return WaitAction(site_id, step) 
        elif action == "assertExists":
            return AssertExistsAction(site_id, step) 
        elif action == "assertText":
            return AssertTextAction(site_id, step) 
        elif action == "screenshot":
            return ScreenshotAction(site_id, step)
        elif action == "scroll_into_view":
            return ScrollIntoViewAction(site_id, step)
        else:
            raise ValueError(f"Unknown action: {action}")
