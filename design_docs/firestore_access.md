# 概要
複数のテスターがこのアプリを使ってテストを実行した場合も結果を共有できるよう`/run_tests`APIで実行したテスト結果はFirestoreに保存します。

# ローカル環境での保存処理
ローカル環境（ENVが`dev`の場合）はFirestoreにはアクセスできないので、テスト結果は保存しません。

# Firestoreのデータ構造
Firestoreはコレクションとドキュメントが交互になるため以下の通りとします。`siteId`および`testCaseId`はAPIで指定されるIDで可変文字列となります。

- e2e-test(collection)
  - [siteId](document)
    - test-case(collection)
      - [testCaseId](document)
        - testRunAt: 前回実行日時を保持します。データ型は"timestamp"です
        - result: テスト結果を"success"または"failed"という文字列で保持します。データ型は"string"です

# テスト結果保存処理
PlayWrightでテストケース実行後、`siteId`と`testCaseId`をもとにFirestoreにテスト結果を保存します。

# テスト結果取得処理
指定した`siteId`のテスト結果を全件取得します。具体的には指定した`siteId`でFirestoreに検索をかけ"/e2e-test/[siteId]/test-case"の配下にある全てのtestCaseIdのフィールドを取得します。

# Firestoreのルール
このアプリは`Cloud Run`上で実行するのでFirestoreセキュリティルールは`read`, `write`とも許可しないデフォルト設定のままとします。

