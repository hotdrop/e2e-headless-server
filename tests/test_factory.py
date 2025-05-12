import pytest
from actions.factory import ActionFactory
from actions.input import InputAction
from actions.click import ClickAction
from actions.screenshot import ScreenshotAction
from actions.scroll_into_view import ScrollIntoViewAction
from actions.wait import WaitAction
from actions.wait_for_selector_action import WaitForSelectorAction
from actions.assert_exists import AssertExistsAction
from actions.assert_text import AssertTextAction

DUMMY_SITE_ID = "test_site"

def test_factory_creates_correct_action():
    assert isinstance(ActionFactory.create(DUMMY_SITE_ID, {"action": "input"}), InputAction)
    assert isinstance(ActionFactory.create(DUMMY_SITE_ID, {"action": "click"}), ClickAction)
    assert isinstance(ActionFactory.create(DUMMY_SITE_ID, {"action": "wait"}), WaitAction)
    assert isinstance(ActionFactory.create(DUMMY_SITE_ID, {"action": "waitForSelector"}), WaitForSelectorAction)
    assert isinstance(ActionFactory.create(DUMMY_SITE_ID, {"action": "assertExists"}), AssertExistsAction)
    assert isinstance(ActionFactory.create(DUMMY_SITE_ID, {"action": "assertText"}), AssertTextAction)
    assert isinstance(ActionFactory.create(DUMMY_SITE_ID, {"action": "screenshot"}), ScreenshotAction)
    assert isinstance(ActionFactory.create(DUMMY_SITE_ID, {"action": "scrollIntoView"}), ScrollIntoViewAction)

def test_factory_raises_for_unknown_action():
    with pytest.raises(ValueError):
        ActionFactory.create(DUMMY_SITE_ID, {"action": "unknown"})
