from actions.base import BaseAction

class ClickAction(BaseAction):
    def execute(self, page):
        selector = self.step.get("selector")
        page.click(selector)
        return {"status": "executed"}