from actions.base import BaseAction
from actions.mixins import LocatorResolverMixin

class ClickAction(BaseAction, LocatorResolverMixin):
    def execute(self, page):
        selector_config = self.step.get("selector")

        if isinstance(selector_config, dict):
            locator = self._resolve_locator(page, selector_config, default_role_type="button")
        else:
            locator = page.locator(selector_config)

        locator.click()
        return {"status": "executed"}
