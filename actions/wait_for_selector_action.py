from actions.base import BaseAction
from actions.mixins import LocatorResolverMixin

class WaitForSelectorAction(BaseAction, LocatorResolverMixin):
  def execute(self, page):
    selector_config = self.step.get("selector")
    # 表示されるまで待つ場合は省略かvisible、インジケータなどhiddenになるのを待つ場合はhiddenを指定
    state = self.step.get("state", "visible")
    timeout = self.step.get("timeout", 10000)

    if isinstance(selector_config, dict):
      locator = self._resolve_locator(page, selector_config)
      locator.wait_for(state=state, timeout=timeout)
    else:
      page.wait_for_selector(selector_config, state=state, timeout=timeout)

    return {"status": "executed"}