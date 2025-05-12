import pytest
from actions.assert_exists import AssertExistsAction
from playwright.sync_api import Page, sync_playwright
from typing import Generator, Any, Dict

DUMMY_SITE_ID = "test_site"

# ヘルパー関数：ページセットアップとクリーンアップを共通化
@pytest.fixture
def page() -> Generator[Page, None, None]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page_context = browser.new_page()
        yield page_context
        browser.close()

def test_assert_exists_true_passes_when_element_exists_css(page: Page):
    page.set_content('<div id="target-css"></div>')
    step = {
        "action": "assert",
        "selector": "#target-css",
        "exists": True
    }
    action = AssertExistsAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "executed"

def test_assert_exists_true_fails_when_element_missing_css(page: Page):
    page.set_content('')
    selector_config = "#missing-css"
    step = {
        "action": "assert",
        "selector": selector_config,
        "exists": True
    }
    action = AssertExistsAction(DUMMY_SITE_ID, step)
    with pytest.raises(AssertionError, match=f"Assertion failed: Element {selector_config} not found."):
        action.execute(page)

def test_assert_exists_false_passes_when_element_missing_css(page: Page):
    page.set_content('')
    step = {
        "action": "assert",
        "selector": "#missing-css-false",
        "exists": False
    }
    action = AssertExistsAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "executed"

def test_assert_exists_false_fails_when_element_exists_css(page: Page):
    page.set_content('<div id="existing-css-false"></div>')
    selector_config = "#existing-css-false"
    step = {
        "action": "assert",
        "selector": selector_config,
        "exists": False
    }
    action = AssertExistsAction(DUMMY_SITE_ID, step)
    with pytest.raises(AssertionError, match=f"Assertion failed: Element {selector_config} exists but should not."):
        action.execute(page)

# --- selector が dict の場合のテスト ---

# Role Selector Tests
@pytest.mark.parametrize(
    "html_content, selector_dict, exists_param, should_raise, expected_message_part",
    [
        # Role: exists: True
        # ボタンのテキストをセレクタの name に合わせる
        ('<div><button>btn_role_exists_true</button></div>', {"by": "role", "type": "button", "name": "btn_role_exists_true"}, True, False, None),
        # 要素がないケース (HTMLを空にするか、該当nameの要素を含まないようにする)
        ('<div></div>', {"by": "role", "type": "button", "name": "btn_role_missing_true"}, True, True, "not found"),
        # Role: exists: False
        # 要素がないケース
        ('<div></div>', {"by": "role", "type": "button", "name": "btn_role_missing_false"}, False, False, None),
        # ボタンのテキストをセレクタの name に合わせる
        ('<div><button>btn_role_exists_false</button></div>', {"by": "role", "type": "button", "name": "btn_role_exists_false"}, False, True, "exists but should not"),
        # Role: exists: (default True)
        # ボタンのテキストをセレクタの name に合わせる
        ('<div><button>btn_role_exists_default</button></div>', {"by": "role", "type": "button", "name": "btn_role_exists_default"}, None, False, None),
        # 要素がないケース
        ('<div></div>', {"by": "role", "type": "button", "name": "btn_role_missing_default"}, None, True, "not found"),
    ]
)
def test_assert_exists_with_role_selector(page: Page, html_content: str, selector_dict: Dict[str, Any], exists_param: Any, should_raise: bool, expected_message_part: str):
    page.set_content(html_content)
    step: Dict[str, Any] = {
        "action": "assert",
        "selector": selector_dict,
    }
    if exists_param is not None:
        step["exists"] = exists_param

    action = AssertExistsAction(DUMMY_SITE_ID, step)

    if should_raise:
        with pytest.raises(AssertionError) as excinfo:
            action.execute(page)
        assert expected_message_part in str(excinfo.value)
        assert str(selector_dict) in str(excinfo.value)
    else:
        result = action.execute(page)
        assert result["status"] == "executed"

# Text Selector Tests
@pytest.mark.parametrize(
    "html_content, selector_dict, exists_param, should_raise, expected_message_part",
    [
        # Text: exists: True
        ('<div><span>Text Exists True</span></div>', {"by": "text", "text": "Text Exists True"}, True, False, None),
        ('<div></div>', {"by": "text", "text": "Text Missing True"}, True, True, "not found"),
        # Text: exists: False
        ('<div></div>', {"by": "text", "text": "Text Missing False"}, False, False, None),
        ('<div><span>Text Exists False</span></div>', {"by": "text", "text": "Text Exists False"}, False, True, "exists but should not"),
        # Text: exists: (default True)
        ('<div><span>Text Exists Default</span></div>', {"by": "text", "text": "Text Exists Default"}, None, False, None),
        ('<div></div>', {"by": "text", "text": "Text Missing Default"}, None, True, "not found"),
    ]
)
def test_assert_exists_with_text_selector(page: Page, html_content: str, selector_dict: Dict[str, Any], exists_param: Any, should_raise: bool, expected_message_part: str):
    page.set_content(html_content)
    step: Dict[str, Any] = {
        "action": "assert",
        "selector": selector_dict,
    }
    if exists_param is not None:
        step["exists"] = exists_param

    action = AssertExistsAction(DUMMY_SITE_ID, step)

    if should_raise:
        with pytest.raises(AssertionError) as excinfo:
            action.execute(page)
        assert expected_message_part in str(excinfo.value)
        assert str(selector_dict) in str(excinfo.value)
    else:
        result = action.execute(page)
        assert result["status"] == "executed"


# --- exists パラメータが省略された場合のテスト (CSSセレクタ) ---
def test_assert_exists_default_true_passes_when_element_exists_css(page: Page):
    page.set_content('<div id="target-default"></div>')
    step = {
        "action": "assert",
        "selector": "#target-default",
        # "exists" is omitted, defaults to True
    }
    action = AssertExistsAction(DUMMY_SITE_ID, step)
    result = action.execute(page)
    assert result["status"] == "executed"

def test_assert_exists_default_true_fails_when_element_missing_css(page: Page):
    page.set_content('')
    selector_config = "#missing-default"
    step = {
        "action": "assert",
        "selector": selector_config,
        # "exists" is omitted, defaults to True
    }
    action = AssertExistsAction(DUMMY_SITE_ID, step)
    with pytest.raises(AssertionError, match=f"Assertion failed: Element {selector_config} not found."):
        action.execute(page)


# --- 不正な selector by value のテスト ---
def test_assert_exists_with_unsupported_selector_by_value(page: Page):
    page.set_content('<button>Test</button>')
    selector_config = {"by": "invalid_method", "value": "some_value"}
    step = {
        "action": "assert",
        "selector": selector_config,
        "exists": True
    }
    action = AssertExistsAction(DUMMY_SITE_ID, step)

    with pytest.raises(ValueError) as excinfo:
        action.execute(page)
    # mixins.py で定義されたエラーメッセージに合致するか確認
    assert f"Unsupported selector 'by' value: {selector_config.get('by')} in {selector_config}" in str(excinfo.value)