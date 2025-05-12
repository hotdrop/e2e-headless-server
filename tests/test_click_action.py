from actions.click import ClickAction
from playwright.sync_api import sync_playwright, Page
from typing import Generator
import pytest

DUMMY_SITE_ID = "test_site"

# ヘルパー関数：ページセットアップとクリーンアップを共通化
@pytest.fixture
def page() -> Generator[Page, None, None]: # <- 型ヒントを修正
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page_context = browser.new_page()
        yield page_context
        browser.close()

def test_click_action_executes_click_with_css_selector(page: Page):
    page.set_content('<button id="btn1" onclick="window.clickedCss=true">Click CSS</button><script>window.clickedCss = false;</script>')

    step = {
        "action": "click",
        "selector": "#btn1"
    }

    action = ClickAction(DUMMY_SITE_ID, step)
    result = action.execute(page)

    assert result["status"] == "executed"
    assert page.evaluate("window.clickedCss") is True

def test_click_action_executes_click_with_role_selector_default_type(page: Page):
    page.set_content('<button onclick="window.clickedRoleDefault=true">Click Role Default</button><script>window.clickedRoleDefault = false;</script>')

    step = {
        "action": "click",
        "selector": {
            "by": "role",
            "name": "Click Role Default"
            # type を指定しない場合、default_role_type="button" が使われることを期待
        }
    }

    action = ClickAction(DUMMY_SITE_ID, step)
    result = action.execute(page)

    assert result["status"] == "executed"
    assert page.evaluate("window.clickedRoleDefault") is True

def test_click_action_executes_click_with_role_selector_explicit_type(page: Page):
    page.set_content('<div role="button" aria-label="Click Me Role Div" onclick="window.clickedRoleExplicit=true">Click Role Explicit</div><script>window.clickedRoleExplicit = false;</script>')

    step = {
        "action": "click",
        "selector": {
            "by": "role",
            "type": "button", # 明示的に type を指定
            "name": "Click Me Role Div"
        }
    }

    action = ClickAction(DUMMY_SITE_ID, step)
    result = action.execute(page)

    assert result["status"] == "executed"
    assert page.evaluate("window.clickedRoleExplicit") is True


def test_click_action_executes_click_with_text_selector(page: Page):
    page.set_content('<button onclick="window.clickedText=true">Click By Text</button><script>window.clickedText = false;</script>')

    step = {
        "action": "click",
        "selector": {
            "by": "text",
            "text": "Click By Text"
        }
    }

    action = ClickAction(DUMMY_SITE_ID, step)
    result = action.execute(page)

    assert result["status"] == "executed"
    assert page.evaluate("window.clickedText") is True

# パラメータ化されたテストで複数のロールと名前の組み合わせをテスト
@pytest.mark.parametrize(
    "html_content, selector_config, js_flag",
    [
        # ケース1: role='button', name で指定
        (
            '<button onclick="window.clickedRoleBtnName=true">Submit Form</button><script>window.clickedRoleBtnName = false;</script>',
            {"by": "role", "type": "button", "name": "Submit Form"},
            "window.clickedRoleBtnName"
        ),
        # ケース2: role='link', name で指定
        (
            '<a href="#" role="link" onclick="window.clickedRoleLinkName=true">Read More</a><script>window.clickedRoleLinkName = false;</script>',
            {"by": "role", "type": "link", "name": "Read More"},
            "window.clickedRoleLinkName"
        ),
        # ケース3: role (type指定なし、デフォルト"button") nameで指定
        (
            '<button onclick="window.clickedRoleDefName=true">Default Button</button><script>window.clickedRoleDefName = false;</script>',
            {"by": "role", "name": "Default Button"}, # type を省略
            "window.clickedRoleDefName"
        ),
    ]
)
def test_click_action_with_various_role_selectors(page: Page, html_content: str, selector_config: dict, js_flag: str):
    page.set_content(html_content)

    step = {
        "action": "click",
        "selector": selector_config
    }

    action = ClickAction(DUMMY_SITE_ID, step)
    result = action.execute(page)

    assert result["status"] == "executed"
    assert page.evaluate(js_flag) is True


def test_click_action_with_unsupported_selector_by_value(page: Page):
    page.set_content('<button onclick="window.clicked=true">Test</button>')
    step = {
        "action": "click",
        "selector": {
            "by": "unsupported_method",
            "value": "some_value"
        }
    }
    action = ClickAction(DUMMY_SITE_ID, step)

    with pytest.raises(ValueError) as excinfo:
        action.execute(page)
    assert "Unsupported selector 'by' value: unsupported_method" in str(excinfo.value)