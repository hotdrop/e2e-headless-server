import pytest
from actions.input import InputAction
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

def test_input_action_executes_fill(page: Page):
    page.set_content('<input id="test" />')
    step = {
        "action": "input",
        "selector": "#test",
        "value": "hello"
    }
    action = InputAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "executed"
    assert page.input_value("#test") == "hello"

def test_input_action_by_role(page: Page):
    page.set_content('<input type="text" aria-label="Username" />')
    step = {
        "action": "input",
        "selector": {"by": "role", "type": "textbox", "name": "Username"},
        "value": "testuser1"
    }
    action = InputAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "executed"
    assert page.get_by_label("Username").input_value() == "testuser1"

def test_input_action_by_role_with_type_omitted(page: Page):
    page.set_content('<input type="text" aria-label="Password" />')
    step = {
        "action": "input",
        "selector": {"by": "role", "name": "Password"},
        "value": "testpass123"
    }
    action = InputAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "executed"
    assert page.get_by_label("Password").input_value() == "testpass123"

def test_input_action_by_text_contenteditable(page: Page):
    page.set_content('<div contenteditable="true" aria-label="Description">Initial description</div>')
    step = {
        "action": "input",
        "selector": {"by": "text", "text": "Initial description"},
        "value": "Updated description"
    }
    action = InputAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "executed"
    # contenteditable divの場合、値はinner_textとなる
    assert page.get_by_label("Description").inner_text() == "Updated description"

def test_input_action_unsupported_by_value(page: Page):
    page.set_content('<input id="test" />')
    step = {
        "action": "input",
        "selector": {"by": "invalid_by_type", "value": "some_value"},
        "value": "hello"
    }
    action = InputAction(DUMMY_SITE_ID, step)
    with pytest.raises(ValueError) as excinfo:
        action.execute(page)
    assert "Unsupported selector 'by' value: invalid_by_type" in str(excinfo.value)
