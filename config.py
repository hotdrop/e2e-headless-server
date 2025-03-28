import os

# 環境変数から実行環境を取得（デフォルトは本番環境）
ENV = os.environ.get("ENV", "prod")

# 環境に応じた設定
class Config:
    # 共通設定
    API_KEY = os.environ.get("API_KEY", "default-secret-key")
    
    # 環境固有の設定
    if ENV == "dev":
        # 開発環境（ローカル）
        SCREENSHOT_DIR = "/output"  # Dockerコンテナ内の出力ディレクトリ
        STORAGE_TYPE = "local"
    else:
        # 本番環境（Cloud Run）
        SCREENSHOT_DIR = "/tmp"  # Cloud Runの一時ディレクトリ
        STORAGE_TYPE = "cloud_storage"
        # Cloud Storageの設定
        BUCKET_NAME = os.environ.get("CLOUD_STORAGE_BUCKET", "e2e-test-screenshots") 