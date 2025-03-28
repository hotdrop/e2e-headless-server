import os

# 環境変数から実行環境を取得（デフォルトは本番環境）
ENV = os.environ.get("ENV", "prod")

# 環境に応じた設定
class Config:
    API_KEY = os.environ.get("API_KEY", "default-secret-key")
    
    if ENV == "dev":
        # 開発環境（ローカル）ではDockerコンテナ内の出力ディレクトリを指定
        SCREENSHOT_DIR = "/output"
    else:
        # 本番環境（Cloud Run）ではCloud Runの一時ディレクトリを指定
        SCREENSHOT_DIR = "/tmp"
        BUCKET_NAME = os.environ.get("CLOUD_STORAGE_BUCKET", "e2e-test-screenshots") 