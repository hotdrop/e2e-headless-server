import os
from google.cloud import storage
from config import Config

class StorageHandler:
    def __init__(self):
        if Config.ENV != "dev":
            self.client = storage.Client()
            self.bucket = self.client.bucket(Config.BUCKET_NAME)
        else:
            self.client = None
            self.bucket = None

    def save_screenshot(self, temp_path: str, date_str: str, filename: str) -> str:
        # スクリーンショットを保存し、保存先のパスを返す
        if Config.ENV == "dev":
            return self._save_screenshot_local(temp_path, date_str, filename)
        else:
            return self._save_screenshot_cloud_storage(temp_path, date_str, filename)

    def _save_screenshot_local(self, temp_path: str, date_str: str, filename: str) -> str:
        # ローカルファイルシステムにスクリーンショットを保存
        date_dir = os.path.join(Config.SCREENSHOT_DIR, date_str)
        os.makedirs(date_dir, exist_ok=True)
        
        filepath = os.path.join(date_dir, filename)
        os.rename(temp_path, filepath)
        
        return filepath

    def _save_screenshot_cloud_storage(self, temp_path: str, date_str: str, filename: str) -> str:
        # Cloud Storageにスクリーンショットを保存
        blob_path = f"{date_str}/{filename}"
        blob = self.bucket.blob(blob_path)
        
        try:
            with open(temp_path, 'rb') as f:
                blob.upload_from_file(f, content_type='image/png')
        except Exception as e:
            raise RuntimeError(f"Cloud Storage upload failed: {e}")
        
        return f"gs://{Config.BUCKET_NAME}/{blob_path}" 