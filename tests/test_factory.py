import pytest
from actions.factory import ActionFactory
from actions.input import InputAction
from actions.click import ClickAction
from actions.screenshot import ScreenshotAction
from actions.wait import WaitAction
from actions.assert_exists import AssertExistsAction
from actions.assert_text import AssertTextAction

def test_factory_creates_correct_action():
    assert isinstance(ActionFactory.create({"action": "input"}), InputAction)
    assert isinstance(ActionFactory.create({"action": "click"}), ClickAction)
    assert isinstance(ActionFactory.create({"action": "wait"}), WaitAction)
    assert isinstance(ActionFactory.create({"action": "assertExists"}), AssertExistsAction)
    assert isinstance(ActionFactory.create({"action": "assertText"}), AssertTextAction)
    assert isinstance(ActionFactory.create({"action": "screenshot"}), ScreenshotAction)

def test_factory_raises_for_unknown_action():
    with pytest.raises(ValueError):
        ActionFactory.create({"action": "unknown"})