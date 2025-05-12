import os
from datetime import datetime
from actions.base import BaseAction
from config import Config
from services.storage import StorageHandler

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
        # site_id を save_screenshot に渡す
        storage_handler.save_screenshot(temp_path, self.site_id, date_str, filename) 
        
        return { "status": "executed" }
