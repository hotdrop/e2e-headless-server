# 1. Pythonベースイメージ（スリムで安定）
FROM python:3.10-slim

# 2. 環境変数（無害なデフォルト）
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. 必要なOSパッケージをインストール（Playwrightが必要とするライブラリ群）
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    ca-certificates \
    libnss3 \
    libatk-bridge2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libgtk-3-0 \
    libasound2 \
    libxshmfence1 \
    libx11-xcb1 \
    libxext6 \
    libxfixes3 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# 4. 作業ディレクトリを作成
WORKDIR /app

# 5. Python依存関係ファイルをコピーしてインストール
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 6. Playwrightのブラウザをインストール（chromiumのみ）
RUN playwright install --with-deps chromium

# 7. アプリケーションのコードをコピーする
COPY . .

# 8. Flaskアプリの起動（ホスト側からは8080番を使う前提）
EXPOSE 8080

# 9. 実行コマンド
CMD ["python", "app.py"]