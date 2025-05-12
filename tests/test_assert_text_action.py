import pytest
from actions.assert_text import AssertTextAction
from playwright.sync_api import Page, sync_playwright
from typing import Generator

DUMMY_SITE_ID = "test_site"

# ヘルパー関数：ページセットアップとクリーンアップを共通化
@pytest.fixture
def page() -> Generator[Page, None, None]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page_context = browser.new_page()
        yield page_context
        browser.close()

def test_assert_text_passes_when_text_exists(page: Page):
    page.set_content('<div id="target">Hello World</div>')
    step = {
        "action": "assertText",
        "selector": "#target",
        "text": "Hello"
    }
    action = AssertTextAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "executed"

def test_assert_text_fails_when_text_missing(page: Page):
    page.set_content('<div id="target">Hello World</div>')
    step = {
        "action": "assertText",
        "selector": "#target",
        "text": "Goodbye"
    }
    action = AssertTextAction(DUMMY_SITE_ID, step)
    with pytest.raises(AssertionError) as exc_info:
        action.execute(page)
    assert "Text assertion failed" in str(exc_info.value)
    assert "Expected text 'Goodbye'" in str(exc_info.value)
    assert "Actual text: 'Hello World'" in str(exc_info.value)

def test_assert_text_fails_when_element_missing(page: Page):
    page.set_content('')
    step = {
        "action": "assertText",
        "selector": "#missing",
        "text": "Hello"
    }
    action = AssertTextAction(DUMMY_SITE_ID, step)
    with pytest.raises(AssertionError) as exc_info:
        action.execute(page)
    assert "Element #missing not found" in str(exc_info.value)

def test_assert_text_fails_when_text_not_specified(page: Page):
    page.set_content('<div id="target">Hello World</div>')
    step = {
        "action": "assertText",
        "selector": "#target"
    }
    action = AssertTextAction(DUMMY_SITE_ID, step)
    with pytest.raises(ValueError) as exc_info:
        action.execute(page)
    assert "Text to assert is required" in str(exc_info.value)

# --- selector が dict の場合のテスト ---

def test_assert_text_by_role_passes(page: Page):
    page.set_content('<div role="status" aria-label="Message">Operation successful</div>')
    step = {
        "action": "assertText",
        "selector": {"by": "role", "type": "status", "name": "Message"},
        "text": "successful"
    }
    action = AssertTextAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "executed"

def test_assert_text_by_role_fails_wrong_text(page: Page):
    page.set_content('<div role="status" aria-label="Message">Operation successful</div>')
    step = {
        "action": "assertText",
        "selector": {"by": "role", "type": "status", "name": "Message"},
        "text": "failed"
    }
    action = AssertTextAction(DUMMY_SITE_ID, step)
    with pytest.raises(AssertionError) as exc_info:
        action.execute(page)
    assert "Text assertion failed" in str(exc_info.value)

def test_assert_text_by_role_fails_element_missing(page: Page):
    page.set_content('<div></div>')
    step = {
        "action": "assertText",
        "selector": {"by": "role", "type": "status", "name": "NonExistentMessage"},
        "text": "any"
    }
    action = AssertTextAction(DUMMY_SITE_ID, step)
    with pytest.raises(AssertionError) as exc_info:
        action.execute(page)
    assert "Element {'by': 'role', 'type': 'status', 'name': 'NonExistentMessage'} not found" in str(exc_info.value)

def test_assert_text_by_text_passes(page: Page):
    page.set_content('<p>This is the target paragraph.</p>')
    step = {
        "action": "assertText",
        "selector": {"by": "text", "text": "target paragraph"},
        "text": "paragraph"
    }
    action = AssertTextAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "executed"

def test_assert_text_by_text_fails_wrong_text(page: Page):
    page.set_content('<p>This is the target paragraph.</p>')
    step = {
        "action": "assertText",
        "selector": {"by": "text", "text": "target paragraph"},
        "text": "non_existent_text"
    }
    action = AssertTextAction(DUMMY_SITE_ID, step)
    with pytest.raises(AssertionError) as exc_info:
        action.execute(page)
    assert "Text assertion failed" in str(exc_info.value)

def test_assert_text_unsupported_by_value(page: Page):
    page.set_content('<div id="target">Hello World</div>')
    step = {
        "action": "assertText",
        "selector": {"by": "invalid_by_type", "value": "some_value"},
        "text": "Hello"
    }
    action = AssertTextAction(DUMMY_SITE_ID, step)
    with pytest.raises(ValueError) as exc_info:
        action.execute(page)
    assert "Unsupported selector 'by' value: invalid_by_type" in str(exc_info.value)
