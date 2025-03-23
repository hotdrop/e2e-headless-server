from actions.base import BaseAction

class AssertExistsAction(BaseAction):
    def execute(self, page):
        selector = self.step.get("selector")
        expected = self.step.get("exists", True)
        elements = page.query_selector_all(selector)
        if expected and not elements:
            raise AssertionError(f"Assertion failed: Element {selector} not found.")
        elif not expected and elements:
            raise AssertionError(f"Assertion failed: Element {selector} exists but should not.")
        return {"status": "executed"}