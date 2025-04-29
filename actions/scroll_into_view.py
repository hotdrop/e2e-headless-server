from actions.base import BaseAction

class ScrollIntoViewAction(BaseAction):
    def __init__(self, site_id, step):
        super().__init__(site_id, step)
        self.selector = step['selector']
        self.timeout = step.get('timeoutMillis', 5000)

    def execute(self, page):
        try:
            page.locator(self.selector).scroll_into_view_if_needed(timeout=self.timeout)
            return { "status": "success", "message": f"Scrolled to element '{self.selector}'" }
        except Exception as e:
            raise e
