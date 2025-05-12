from actions.base import BaseAction
from actions.mixins import LocatorResolverMixin

class AssertExistsAction(BaseAction, LocatorResolverMixin):
    def execute(self, page):
        selector_config = self.step.get("selector")
        expected = self.step.get("exists", True)

        if isinstance(selector_config, dict):
            locator = self._resolve_locator(page, selector_config)
        else:
            locator = page.locator(selector_config)
        
        element_exists = locator.count() > 0

        if expected and not element_exists:
            raise AssertionError(f"Assertion failed: Element {selector_config} not found.")
        elif not expected and element_exists:
            raise AssertionError(f"Assertion failed: Element {selector_config} exists but should not.")
        return {"status": "executed"}
