# TODOリスト
今できていないことを以下に列挙します。

## 1. APIKeyの取得先の変更
- ローカルのdockerで動かす場合: 従来通りAPIKeyを環境変数で設定できる。
- CloudRun上で動かす場合: APIKeyをGoogleCloudのSecretManagerから取得する。

## 2. 以下の新しいアクションを実装する
- screenshot
  - スクリーンショットを撮って特定のディレクトリに保存
- 仕様
  - ローカルのdockerで動かす場合: ローカルのscreenshotフォルダに保存する
  - CloudRun上で動かす場合: CloudStorage上に保存する
