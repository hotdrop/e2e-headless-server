import pytest
from actions.factory import ActionFactory
from actions.input import InputAction
from actions.click import ClickAction
from actions.wait import WaitAction
from actions.assert_exists import AssertExistsAction

def test_factory_creates_correct_action():
    assert isinstance(ActionFactory.create({"action": "input"}), InputAction)
    assert isinstance(ActionFactory.create({"action": "click"}), ClickAction)
    assert isinstance(ActionFactory.create({"action": "wait"}), WaitAction)
    assert isinstance(ActionFactory.create({"action": "assertExists"}), AssertExistsAction)

def test_factory_raises_for_unknown_action():
    with pytest.raises(ValueError):
        ActionFactory.create({"action": "unknown"})