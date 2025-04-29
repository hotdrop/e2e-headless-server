import pytest
from actions.factory import ActionFactory
from actions.input import InputAction
from actions.click import ClickAction
from actions.screenshot import ScreenshotAction
from actions.wait import WaitAction
from actions.assert_exists import AssertExistsAction
from actions.assert_text import AssertTextAction

TEST_SITE = "test_site"

def test_factory_creates_correct_action():
    assert isinstance(ActionFactory.create(TEST_SITE, {"action": "input"}), InputAction)
    assert isinstance(ActionFactory.create(TEST_SITE, {"action": "click"}), ClickAction)
    assert isinstance(ActionFactory.create(TEST_SITE, {"action": "wait"}), WaitAction)
    assert isinstance(ActionFactory.create(TEST_SITE, {"action": "assertExists"}), AssertExistsAction)
    assert isinstance(ActionFactory.create(TEST_SITE, {"action": "assertText"}), AssertTextAction)
    assert isinstance(ActionFactory.create(TEST_SITE, {"action": "screenshot"}), ScreenshotAction)

def test_factory_raises_for_unknown_action():
    with pytest.raises(ValueError):
        ActionFactory.create(TEST_SITE, {"action": "unknown"})
