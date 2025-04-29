import pytest
from actions.click import ClickAction
from playwright.sync_api import sync_playwright

TEST_SITE = "test_site"

def test_click_action_executes_click():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content('<button id="btn" onclick="window.clicked=true">Click</button><script>window.clicked = false;</script>')

        step = {
            "action": "click",
            "selector": "#btn"
        }

        action = ClickAction(TEST_SITE, step)
        result = action.execute(page)

        assert result["status"] == "executed"
        assert page.evaluate("window.clicked") is True
        browser.close()