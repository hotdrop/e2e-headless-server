import pytest
from actions.assert_exists import AssertExistsAction
from playwright.sync_api import sync_playwright

def test_assert_exists_passes_when_element_exists():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content('<div id="target"></div>')

        step = {
            "action": "assert",
            "selector": "#target",
            "exists": True
        }

        action = AssertExistsAction(step)
        result = action.execute(page)

        assert result["status"] == "executed"
        browser.close()

def test_assert_exists_fails_when_element_missing():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content('')

        step = {
            "action": "assert",
            "selector": "#missing",
            "exists": True
        }

        action = AssertExistsAction(step)
        with pytest.raises(AssertionError):
            action.execute(page)
        browser.close()

def test_assert_not_exists_passes_when_element_missing():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content('')

        step = {
            "action": "assert",
            "selector": "#missing",
            "exists": False
        }

        action = AssertExistsAction(step)
        result = action.execute(page)

        assert result["status"] == "executed"
        browser.close()