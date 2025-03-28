from actions.base import BaseAction

class AssertTextAction(BaseAction):
    def execute(self, page):
        selector = self.step.get("selector")
        expected_text = self.step.get("text")
        
        if not expected_text:
            raise ValueError("Text to assert is required in the step definition")
            
        element = page.query_selector(selector)
        if not element:
            raise AssertionError(f"Element {selector} not found")
            
        actual_text = element.inner_text()
        if expected_text not in actual_text:
            raise AssertionError(
                f"Text assertion failed: Expected text '{expected_text}' not found in element {selector}. "
                f"Actual text: '{actual_text}'"
            )
            
        return {"status": "executed"} 