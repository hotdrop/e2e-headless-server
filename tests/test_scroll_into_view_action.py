import pytest
from playwright.sync_api import Page, sync_playwright, TimeoutError as PlaywrightTimeoutError
from actions.scroll_into_view import ScrollIntoViewAction
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

# 一番下の要素を持つページを設定するためのヘルパー関数
def setup_page_for_scroll(page, element_id="bottomElement", role=None, label=None, text_content=None):
    content = '<div style="height: 1500px;">Spacer</div>' # スクロールが必要であることを確認する
    if role and label:
        content += f'<div style="margin-top: 50px;" id="{element_id}" role="{role}" aria-label="{label}">{label} Content</div>'
    elif text_content:
        content += f'<p style="margin-top: 50px;" id="{element_id}">{text_content}</p>'
    else:
        content += f'<div style="margin-top: 50px;" id="{element_id}">Target Element</div>'
    page.set_content(content)
    page.set_viewport_size({"width": 600, "height": 600}) # 要素が画面外にあることを確認する

def test_scroll_into_view_string_selector(page: Page):
    setup_page_for_scroll(page, element_id="target1")
    step = {
        "action": "scrollIntoView",
        "selector": "#target1",
        "timeoutMillis": 2000
    }
    action = ScrollIntoViewAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "success"

def test_scroll_into_view_string_selector_default_timeout(page: Page):
    setup_page_for_scroll(page, element_id="target2")
    step = {
        "action": "scrollIntoView",
        "selector": "#target2" 
    } # Default timeout 5000ms
    action = ScrollIntoViewAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "success"

def test_scroll_into_view_element_not_found_string_selector(page: Page):
    page.set_content('')
    step = {
        "action": "scrollIntoView",
        "selector": "#nonExistentElement"
    }
    action = ScrollIntoViewAction(DUMMY_SITE_ID, step)
    with pytest.raises(RuntimeError) as exc_info:
        action.execute(page)
    assert "Failed to scroll to element '#nonExistentElement'" in str(exc_info.value)

def test_scroll_into_view_by_role(page: Page):
    setup_page_for_scroll(page, element_id="role_target", role="region", label="FarRegion")
    step = {
        "action": "scrollIntoView",
        "selector": {"by": "role", "type": "region", "name": "FarRegion"}
    }
    action = ScrollIntoViewAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "success"

def test_scroll_into_view_by_text(page: Page):
    setup_page_for_scroll(page, element_id="text_target", text_content="Scroll to this specific text")
    step = {
        "action": "scrollIntoView",
        "selector": {"by": "text", "text": "Scroll to this specific text"}
    }
    action = ScrollIntoViewAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "success"

def test_scroll_into_view_element_not_found_dict_selector(page: Page):
    page.set_content('')
    selector_config = {"by": "role", "type": "region", "name": "NonExistentRegion"}
    step = {
        "action": "scrollIntoView",
        "selector": selector_config
    }
    action = ScrollIntoViewAction(DUMMY_SITE_ID, step)
    with pytest.raises(RuntimeError) as exc_info:
        action.execute(page)
    assert f"Failed to scroll to element '{selector_config}'" in str(exc_info.value)

def test_scroll_into_view_unsupported_by_value(page: Page):
    # 未定義のセレクタがあった場合はPlaywrightとのやり取りの前に失敗するはずなのでコンテンツは適当
    page.set_content('<div id="any"></div>') 
    step = {
        "action": "scrollIntoView",
        "selector": {"by": "invalid_by_type", "value": "some_value"}
    }
    action = ScrollIntoViewAction(DUMMY_SITE_ID, step)
    with pytest.raises(ValueError) as exc_info:
        action.execute(page)
    assert "Unsupported selector 'by' value: invalid_by_type" in str(exc_info.value)
