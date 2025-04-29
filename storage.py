import os
from google.cloud import storage
from config import Config, ENV

class StorageHandler:
    def __init__(self):
        if ENV != "dev":
            self.client = storage.Client()
            self.bucket = self.client.bucket(Config.BUCKET_NAME)
        else:
            self.client = None
            self.bucket = None

    # site_id を引数に追加
    def save_screenshot(self, temp_path: str, site_id: str, date_str: str, filename: str) -> str:
        # スクリーンショットを保存し、保存先のパスを返す
        if ENV == "dev":
            # site_id を渡す
            return self._save_screenshot_local(temp_path, site_id, date_str, filename)
        else:
            # site_id を渡す
            return self._save_screenshot_cloud_storage(temp_path, site_id, date_str, filename)

    # site_id を引数に追加
    def _save_screenshot_local(self, temp_path: str, site_id: str, date_str: str, filename: str) -> str:
        # ローカルファイルシステムにスクリーンショットを保存
        # site_id をパスに追加
        target_dir = os.path.join(Config.SCREENSHOT_DIR, site_id, date_str)
        os.makedirs(target_dir, exist_ok=True)
        
        filepath = os.path.join(target_dir, filename)
        os.rename(temp_path, filepath)
        
        return filepath

    # site_id を引数に追加
    def _save_screenshot_cloud_storage(self, temp_path: str, site_id: str, date_str: str, filename: str) -> str:
        # Cloud Storageにスクリーンショットを保存
        # site_id をパスに追加
        blob_path = f"{site_id}/{date_str}/{filename}"
        blob = self.bucket.blob(blob_path)
        
        try:
            with open(temp_path, 'rb') as f:
                blob.upload_from_file(f, content_type='image/png')
        except Exception as e:
            raise RuntimeError(f"Cloud Storage upload failed: {e}")
        
        return f"gs://{Config.BUCKET_NAME}/{blob_path}"
