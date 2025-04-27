# Tech Context

## 主要技術スタック
- プログラミング言語: Python
- Webフレームワーク: Flask
- E2Eテストライブラリ: Playwright (Chromiumブラウザを使用)
- コンテナ化: Docker
- テストフレームワーク: pytest

## 開発セットアップ
1.  依存関係のインストール:
    ```bash
    pip install -r requirements.txt
    ```
    (仮想環境を使用している場合は、`source .venv/bin/activate` などで有効化する)
2.  Dockerイメージのビルド:
    ```bash
    docker build -t e2e-server .
    ```
3.  Dockerコンテナの実行 (ローカル):
    ```bash
    docker run -p 8080:8080 -v $(pwd)/output:/output -e ENV=dev -e API_KEY=KEY12345 e2e-server
    ```
    -   `-p 8080:8080`: ホストの8080番ポートをコンテナの8080番ポートにマッピング
    -   `-v $(pwd)/output:/output`: ホストのカレントディレクトリ下の `output` をコンテナの `/output` にマウント (スクリーンショット等の出力用)
    -   `-e ENV=dev`: 環境変数を設定 (開発環境)
    -   `-e API_KEY=KEY12345`: APIキーを設定
4.  APIテスト (ローカル):
    ```bash
    curl -X POST http://localhost:8080/run_tests -H "Authorization: Bearer KEY12345" -H "Content-Type: application/json" -d @sample_test_case.json
    ```
5.  ユニットテストの実行:
    ```bash
    pytest tests/
    ```

## 技術的制約・考慮事項
- 実行環境: 主にDockerコンテナ内での実行を想定。ローカル開発およびCloud Runへのデプロイを視野に入れる。
- Playwrightの依存関係: `dockerfile` 内で `playwright install --with-deps chromium` を実行し、必要なブラウザとライブラリをインストールする。別途Chrome等のインストールは不要。
- Webサーバー: Flaskの組み込みサーバーを使用
- テストケースJSON: 現在はリクエストボディで直接受け取るが、将来的にファイルパス指定による読み込みに変更する可能性あり。
