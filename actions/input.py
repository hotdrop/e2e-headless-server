from actions.base import BaseAction

class InputAction(BaseAction):
    def execute(self, page):
        selector = self.step.get("selector")
        value = self.step.get("value", "")
        page.fill(selector, value)
        return {"status": "executed"}