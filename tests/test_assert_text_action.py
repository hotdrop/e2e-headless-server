import pytest
from actions.assert_text import AssertTextAction
from playwright.sync_api import sync_playwright

def test_assert_text_passes_when_text_exists():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content('<div id="target">Hello World</div>')

        step = {
            "action": "assertText",
            "selector": "#target",
            "text": "Hello"
        }

        action = AssertTextAction(step)
        result = action.execute(page)

        assert result["status"] == "executed"
        browser.close()

def test_assert_text_fails_when_text_missing():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content('<div id="target">Hello World</div>')

        step = {
            "action": "assertText",
            "selector": "#target",
            "text": "Goodbye"
        }

        action = AssertTextAction(step)
        with pytest.raises(AssertionError) as exc_info:
            action.execute(page)
        
        assert "Text assertion failed" in str(exc_info.value)
        assert "Expected text 'Goodbye'" in str(exc_info.value)
        assert "Actual text: 'Hello World'" in str(exc_info.value)
        browser.close()

def test_assert_text_fails_when_element_missing():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content('')

        step = {
            "action": "assertText",
            "selector": "#missing",
            "text": "Hello"
        }

        action = AssertTextAction(step)
        with pytest.raises(AssertionError) as exc_info:
            action.execute(page)
        
        assert "Element #missing not found" in str(exc_info.value)
        browser.close()

def test_assert_text_fails_when_text_not_specified():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content('<div id="target">Hello World</div>')

        step = {
            "action": "assertText",
            "selector": "#target"
        }

        action = AssertTextAction(step)
        with pytest.raises(ValueError) as exc_info:
            action.execute(page)
        
        assert "Text to assert is required" in str(exc_info.value)
        browser.close() 