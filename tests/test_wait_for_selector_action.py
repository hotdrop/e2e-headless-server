import pytest
from playwright.sync_api import Page, sync_playwright, TimeoutError as PlaywrightTimeoutError
from actions.wait_for_selector_action import WaitForSelectorAction
from typing import Generator

DUMMY_SITE_ID = "test_site_wait_for_selector"

# ヘルパー関数：ページセットアップとクリーンアップを共通化
@pytest.fixture
def page() -> Generator[Page, None, None]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page_context = browser.new_page()
        yield page_context
        browser.close()

def test_wait_for_string_selector_visible_default_timeout(page: Page):
    page.set_content('<div id="element-to-appear" style="display:none;">Target</div>')
    # 少し遅れて要素を表示するJavaScript
    page.evaluate('setTimeout(() => { document.getElementById("element-to-appear").style.display = "block"; }, 100)')
    step = {
        "action": "wait_for_selector",
        "selector": "#element-to-appear" 
    }
    action = WaitForSelectorAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "executed"
    assert page.query_selector("#element-to-appear").is_visible()

def test_wait_for_string_selector_hidden_default_timeout(page: Page):
    page.set_content('<div id="element-to-disappear">Target</div>')
    page.evaluate('setTimeout(() => { document.getElementById("element-to-disappear").style.display = "none"; }, 100)')
    step = {
        "action": "wait_for_selector",
        "selector": "#element-to-disappear",
        "state": "hidden"
    }
    action = WaitForSelectorAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "executed"
    assert not page.query_selector("#element-to-disappear").is_visible()

def test_wait_for_string_selector_custom_timeout_pass(page: Page):
    page.set_content('<div id="slow-element" style="display:none;">Slow Target</div>')
    page.evaluate('setTimeout(() => { document.getElementById("slow-element").style.display = "block"; }, 200)')
    step = {
        "action": "wait_for_selector",
        "selector": "#slow-element",
        "timeout": 500 # ms
    }
    action = WaitForSelectorAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "executed"

def test_wait_for_string_selector_times_out_visible(page: Page):
    page.set_content('<div id="never-appears" style="display:none;"></div>')
    step = {
        "action": "wait_for_selector",
        "selector": "#never-appears",
        "timeout": 100 # ms, very short timeout
    }
    action = WaitForSelectorAction(DUMMY_SITE_ID, step)
    with pytest.raises(PlaywrightTimeoutError):
        action.execute(page)

def test_wait_for_string_selector_times_out_hidden(page: Page):
    page.set_content('<div id="never-hides">Always Here</div>')
    step = {
        "action": "wait_for_selector",
        "selector": "#never-hides",
        "state": "hidden",
        "timeout": 100
    }
    action = WaitForSelectorAction(DUMMY_SITE_ID, step)
    with pytest.raises(PlaywrightTimeoutError):
        action.execute(page)

# --- selector が dict の場合のテスト ---

def test_wait_for_dict_selector_role_visible(page: Page):
    page.set_content('<button style="display:none;">Click Me</button>')
    page.evaluate('setTimeout(() => { document.querySelector("button").style.display = "block"; }, 100)')
    step = {
        "action": "wait_for_selector",
        "selector": {"by": "role", "type": "button", "name": "Click Me"}
    }
    action = WaitForSelectorAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "executed"

def test_wait_for_dict_selector_text_hidden(page: Page):
    page.set_content('<p>Loading Indicator</p>')
    page.evaluate('setTimeout(() => { document.querySelector("p").style.display = "none"; }, 100)')
    step = {
        "action": "wait_for_selector",
        "selector": {"by": "text", "text": "Loading Indicator"},
        "state": "hidden",
        "timeout": 500
    }
    action = WaitForSelectorAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "executed"

def test_wait_for_dict_selector_times_out_visible(page: Page):
    page.set_content('') # Element never appears
    step = {
        "action": "wait_for_selector",
        "selector": {"by": "role", "type": "dialog"},
        "timeout": 100
    }
    action = WaitForSelectorAction(DUMMY_SITE_ID, step)
    with pytest.raises(PlaywrightTimeoutError):
        action.execute(page)

# # --- エラーハンドリングのテスト ---

def test_execute_missing_selector_param(page: Page):
    step = {
        "action": "wait_for_selector"
        # "selector" is missing
    }
    action = WaitForSelectorAction(DUMMY_SITE_ID, step)
    with pytest.raises(TypeError, match="'selector'"):
        action.execute(page)

def test_execute_invalid_selector_type(page: Page):
    step = {
        "action": "wait_for_selector",
        "selector": ["invalid", "list", "type"] 
    }
    action = WaitForSelectorAction(DUMMY_SITE_ID, step)
    with pytest.raises(Exception):
        action.execute(page)

def test_execute_invalid_state_value(page: Page):
    page.set_content('<div id="test-div"></div>')
    step = {
        "action": "wait_for_selector",
        "selector": "#test-div",
        "state": "invalid_state_value" # [attached|detached|visible|hidden]のいずれかでなければエラー
    }
    action = WaitForSelectorAction(DUMMY_SITE_ID, step)
    with pytest.raises(Exception):
        action.execute(page)

def test_execute_dict_selector_unsupported_by_value(page: Page):
    step = {
        "action": "wait_for_selector",
        "selector": {"by": "unsupported_by", "type": "some_value"}
    }
    action = WaitForSelectorAction(DUMMY_SITE_ID, step)
    with pytest.raises(ValueError) as exc_info:
        action.execute(page)
    assert "Unsupported selector 'by' value: unsupported_by" in str(exc_info.value)
