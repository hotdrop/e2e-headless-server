# TODOリスト
今できていないことを以下に列挙します。

## 1. ローカルで動かす場合とリモート(CloudRun)で動かす場合でモードを変更する
- ローカルのdockerで動かす場合: 従来通りAPIKeyを環境変数で設定できる。
- CloudRun上で動かす場合: APIKeyをGoogleCloudのSecretManagerから取得する。

## 2. 以下の新しいアクションを実装する
- assert_text
  - 特定の要素内に特定のテキストが含まれるか検証
- screenshot
  - スクリーンショットを撮って特定のディレクトリに保存

## 3. スクリーンショットについて以下を実現したい。
- ローカルのdockerで動かす場合: ローカルのscreenshotフォルダに保存する
- CloudRun上で動かす場合: CloudStorage上に保存する
