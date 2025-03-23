import pytest
from actions.click import ClickAction
from playwright.sync_api import sync_playwright

def test_click_action_executes_click():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content('<button id="btn" onclick="window.clicked=true">Click</button><script>window.clicked = false;</script>')

        step = {
            "action": "click",
            "selector": "#btn"
        }

        action = ClickAction(step)
        result = action.execute(page)

        assert result["status"] == "executed"
        assert page.evaluate("window.clicked") is True
        browser.close()