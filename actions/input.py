from actions.base import BaseAction
from actions.mixins import LocatorResolverMixin

class InputAction(BaseAction, LocatorResolverMixin):
    def execute(self, page):
        selector_config = self.step.get("selector")
        value = self.step.get("value", "")

        if isinstance(selector_config, dict):
            locator = self._resolve_locator(page, selector_config, default_role_type="textbox")
        else:
            locator = page.locator(selector_config)
        
        locator.fill(value)
        return {"status": "executed"}
