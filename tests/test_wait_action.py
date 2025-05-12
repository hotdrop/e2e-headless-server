import time
from actions.wait import WaitAction

DUMMY_SITE_ID = "test_site"

def test_wait_action_waits_correct_seconds(monkeypatch):
    called = []

    def fake_sleep(seconds):
        called.append(seconds)

    monkeypatch.setattr(time, "sleep", fake_sleep)

    step = {
        "action": "wait",
        "seconds": 2
    }

    action = WaitAction(DUMMY_SITE_ID, step)
    result = action.execute(None)

    assert result["status"] == "executed"
    assert called == [2]