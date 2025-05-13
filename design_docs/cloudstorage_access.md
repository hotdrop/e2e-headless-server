# スクリーンショットの保存場所
スクリーンショットアクションを使うとスクリーンショットを取得し、`YYYYMMDDHHMMSS.png`というファイル名で保存します。保存先のディレクトリ仕様は以下のとおりです。

- ENVが"dev"の場合
  - Dockerコンテナ内の`/output/[siteId]/[日付]/[ファイル名]`に保存します。
- ENVが"dev"でない場合
  - `Cloud Storage`に保存します。

## Cloud Storageの仕様
- バケット名の取得
  - 環境変数`CLOUD_STORAGE_BUCKET`から取得します。この環境変数が設定されていない場合のデフォルト値は"e2e-test-screenshots"です。(config.py)
- 保存先
  - バケット内のパス（オブジェクト名）は`CLOUD_STORAGE_BUCKET/[siteId]/日付/ファイル名`という形式になります。