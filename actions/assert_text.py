from actions.base import BaseAction
from actions.mixins import LocatorResolverMixin

class AssertTextAction(BaseAction, LocatorResolverMixin):
    def execute(self, page):
        selector_config = self.step.get("selector")
        expected_text = self.step.get("text")
        
        if not expected_text:
            raise ValueError("Text to assert is required in the step definition")
        
        if isinstance(selector_config, dict):
            locator = self._resolve_locator(page, selector_config)
        else:
            locator = page.locator(selector_config)

        if locator.count() == 0:
            raise AssertionError(f"Element {selector_config} not found")
            
        actual_text = locator.inner_text()
        if expected_text not in actual_text:
            raise AssertionError(
                f"Text assertion failed: Expected text '{expected_text}' not found in element {selector_config}. "
                f"Actual text: '{actual_text}'"
            )
            
        return {"status": "executed"}
