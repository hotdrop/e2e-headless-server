import pytest
from actions.input import InputAction
from playwright.sync_api import sync_playwright

TEST_SITE = "test_site"

def test_input_action_executes_fill():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content('<input id="test" />')

        step = {
            "action": "input",
            "selector": "#test",
            "value": "hello"
        }

        action = InputAction(TEST_SITE, step)
        result = action.execute(page)

        assert result["status"] == "executed"
        assert page.input_value("#test") == "hello"
        browser.close()