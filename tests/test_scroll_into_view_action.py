import pytest
from unittest.mock import MagicMock
from actions.scroll_into_view import ScrollIntoViewAction

TEST_SITE = "test_site"

def test_scroll_into_view_action_execute():
    mock_page = MagicMock()
    mock_locator = MagicMock()
    mock_page.locator.return_value = mock_locator

    step = {
        "action": "scroll_into_view",
        "selector": "#myElement",
        "timeoutMillis": 2000
    }

    action = ScrollIntoViewAction(TEST_SITE, step)
    action.execute(mock_page)

    mock_page.locator.assert_called_once_with("#myElement")
    mock_locator.scroll_into_view_if_needed.assert_called_once_with(timeout=2000)

def test_scroll_into_view_action_execute_default_timeout():
    mock_page = MagicMock()
    mock_locator = MagicMock()
    mock_page.locator.return_value = mock_locator

    step = {
        "action": "scroll_into_view",
        "selector": "#myElement",
    }

    action = ScrollIntoViewAction(TEST_SITE, step)
    action.execute(mock_page)

    mock_page.locator.assert_called_once_with("#myElement")
    mock_locator.scroll_into_view_if_needed.assert_called_once_with(timeout=5000)

def test_scroll_into_view_action_execute_exception():
    mock_page = MagicMock()
    mock_locator = MagicMock()
    mock_page.locator.return_value = mock_locator
    mock_locator.scroll_into_view_if_needed.side_effect = Exception("Scroll failed")

    step = {
        "action": "scroll_into_view",
        "selector": "#myElement",
    }

    action = ScrollIntoViewAction(TEST_SITE, step)

    with pytest.raises(Exception, match="Scroll failed"):
        action.execute(mock_page)
