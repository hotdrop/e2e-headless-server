import os
from unittest.mock import patch, MagicMock
from datetime import datetime
from actions.screenshot import ScreenshotAction
from config import Config

# テスト用の固定日時
FIXED_DATETIME = datetime(2024, 1, 1, 12, 0, 0)
DUMMY_SITE_ID = "test_site_screenshot"
DUMMY_STEP = {"action": "screenshot"}
EXPECTED_DATE_STR = FIXED_DATETIME.strftime("%Y%m%d") # "20240101"
EXPECTED_TIMESTAMP = FIXED_DATETIME.strftime("%Y%m%d_%H%M%S") # "20240101_120000"
EXPECTED_FILENAME = f"{EXPECTED_TIMESTAMP}.png"
EXPECTED_TEMP_PATH = os.path.join(Config.SCREENSHOT_DIR, EXPECTED_FILENAME)

@patch('actions.screenshot.datetime')
@patch('actions.screenshot.StorageHandler')
def test_screenshot_action_execute(MockStorageHandler, mock_datetime):
    # Mockの設定
    mock_datetime.now.return_value = FIXED_DATETIME
    mock_page = MagicMock()
    mock_storage_instance = MockStorageHandler.return_value

    # アクションのインスタンス化と実行
    action = ScreenshotAction(DUMMY_SITE_ID, DUMMY_STEP)
    result = action.execute(mock_page)

    # アサーション
    # 1. page.screenshot が正しい一時パスで呼ばれたか
    mock_page.screenshot.assert_called_once_with(path=EXPECTED_TEMP_PATH)

    # 2. StorageHandler がインスタンス化されたか
    MockStorageHandler.assert_called_once()

    # 3. storage_handler.save_screenshot が正しい引数で呼ばれたか
    mock_storage_instance.save_screenshot.assert_called_once_with(
        EXPECTED_TEMP_PATH,
        DUMMY_SITE_ID,
        EXPECTED_DATE_STR,
        EXPECTED_FILENAME
    )

    # 4. 戻り値が正しいか
    assert result == {"status": "executed"}
