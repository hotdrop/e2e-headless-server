import os
from datetime import datetime
from actions.base import BaseAction
from config import Config
from storage import StorageHandler

class ScreenshotAction(BaseAction):
    def execute(self, page):
        now = datetime.now()
        date_str = now.strftime("%Y%m%d")
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.png"
        
        # スクリーンショットを一時的に保存
        temp_path = os.path.join(Config.SCREENSHOT_DIR, filename)
        page.screenshot(path=temp_path)
        
        # ストレージハンドラーを使用して保存
        storage_handler = StorageHandler()
        storage_path = storage_handler.save_screenshot(temp_path, date_str, filename)
        
        # 一時ファイルを削除
        os.remove(temp_path)
        
        return {
            "status": "executed",
            "screenshot_path": storage_path
        } 