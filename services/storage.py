import os
from google.cloud import storage
from config import Config, ENV

class StorageHandler:
    def __init__(self):
        if ENV.lower() != "dev":
            self.client = storage.Client()
            self.bucket = self.client.bucket(Config.BUCKET_NAME)
        else:
            self.client = None
            self.bucket = None

    def save_screenshot(self, temp_path: str, site_id: str, date_str: str, filename: str) -> str:
        if ENV.lower() == "dev":
            return self._save_screenshot_local(temp_path, site_id, date_str, filename)
        else:
            return self._save_screenshot_cloud_storage(temp_path, site_id, date_str, filename)

    # ローカルファイルシステムにスクリーンショットを保存
    def _save_screenshot_local(self, temp_path: str, site_id: str, date_str: str, filename: str) -> str:
        target_dir = os.path.join(Config.SCREENSHOT_DIR, site_id, date_str)
        os.makedirs(target_dir, exist_ok=True)
        
        filepath = os.path.join(target_dir, filename)
        os.rename(temp_path, filepath)
        
        return filepath

    # Cloud Storageにスクリーンショットを保存
    def _save_screenshot_cloud_storage(self, temp_path: str, site_id: str, date_str: str, filename: str) -> str:
        blob_path = f"{site_id}/{date_str}/{filename}"
        blob = self.bucket.blob(blob_path)
        
        try:
            with open(temp_path, 'rb') as f:
                blob.upload_from_file(f, content_type='image/png')
        except Exception as e:
            raise RuntimeError(f"Cloud Storageへの画像アップロード処理でエラーが発生しました。", e)
        
        return f"gs://{Config.BUCKET_NAME}/{blob_path}"
