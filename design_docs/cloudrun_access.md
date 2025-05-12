# 概要
`Cloud Run`でアプリを動作させるには、まずDockerイメージを`Artifact Registry`にアップロードしそのイメージを使って`Cloud Run`のデプロイコマンドを実行する必要があります。Dockerイメージのアップ方法は以下のいずれかとなります。本アプリではいちいちアップロードすると手間なので`Cloud Build`を使った手順をREADME.mdに記載しています。

- ローカルでDockerイメージを作成し`Artifact Registry`にアップロードしてデプロイコマンドを実行する
- `Cloud Build`を使用しイメージをGoogleCloud側で作成し`Artifact Registry`にアップロードされた後にデプロイコマンドを実行する

## Artifact Registry
`Cloud Run`上で動作させるDockerイメージをGoogleCloud上の`Artifact Registry`に保持する必要があります。コードを修正するたびに新しいDockerイメージをpushする必要があるのでご注意ください。

## サービスアカウント
Cloud Runにデプロイした後、何も設定を変更しない場合、デフォルトで広範囲の権限を持つサービスアカウントを使用して稼働する仕組みになっています。権限が無駄に付与されているとセキュリティ的に良くないので専用のサービスアカウントを設定しましょう。このサービスアカウントに設定する権限は以下のとおりです。
- Storage オブジェクト作成者者
- Cloud Datastore ユーザー