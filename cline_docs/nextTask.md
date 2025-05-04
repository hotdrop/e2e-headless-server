# このファイルについて
この`nextTask.md`はタスクの仕様をユーザーが詳細に記載します。更新はしないでください。

# やりたいこと
複数のテスターがこのアプリを使ってテストを実行した場合も結果を共有できるよう`/run_tests`APIで実行したテスト結果をFirestoreに保存する処理を追加する。
テスト結果保存処理追加に伴い、これまでこのアプリは`/run_tests`API1つのみだったが、テスト結果を取得する"テスト結果取得API"を実装する。

# テスト結果の保存場所
テスト結果はFirestoreに保存する。ただし、ローカル環境で`/run_tests`APIを実行した場合（つまりENVがdevの場合）はFirestoreにはアクセスできないので既存通りテスト結果は保存せずResponseで返すのみとする。

# Firestoreのデータ構造
Firestoreはコレクションとドキュメントが交互になるため以下の通りとする。`siteId`はAPIで指定されるIDで可変文字列となる。`testCaseId`も同様。

- e2e-test(collection)
  - [siteId](document)
    - test-case(collection)
      - [testCaseId](document)
        - testRunAt: 前回実行日時を保持します。データ型は"timestamp"です
        - result: テスト結果を"succes"または"failed"という文字列で保持します。データ型は"string"です
        - detail: エラー詳細を保持します。データ型は"string"です。

# テスト結果保存処理
PlayWrightでテストケース実行後、APIのレスポンスを返却する前に`siteId`と`testCaseId`をもとにFirestoreにテスト結果を保存する。
testCaseIdは現在の仕様ではAPIで取得できていないので新たにAPIのRequestに追加する。
なお、`/run_tests`APIのResponseは既存通りテスト結果を返却する。

# テスト結果取得処理
新たにAPIを用意する。APIのRequestパラメータは`siteId`で、指定したサイトIDのテスト結果を全件取得する。つまり、リクエストの`siteId`をFirestoreに検索をかけ"/e2e-test/[siteId]/test-case"の配下にある全てのtestCaseIdのフィールドをResponseで返す。レスポンスはtestCaseIdとそのフィールドという構成にする。