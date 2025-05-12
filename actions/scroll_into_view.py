from actions.base import BaseAction
from actions.mixins import LocatorResolverMixin

class ScrollIntoViewAction(BaseAction, LocatorResolverMixin):
    def execute(self, page):
        selector_config = self.step.get("selector")
        timeout = self.step.get('timeoutMillis', 5000)

        if isinstance(selector_config, dict):
            locator = self._resolve_locator(page, selector_config)
        else:
            locator = page.locator(selector_config)
        
        try:
            locator.scroll_into_view_if_needed(timeout=timeout)
            return { "status": "success", "message": f"Scrolled to element '{selector_config}'" }
        except Exception as e:
            raise RuntimeError(f"Failed to scroll to element '{selector_config}': {e}") from e
