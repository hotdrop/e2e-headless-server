# Active Context

## 必ず守ること
- 現在のタスクに書かれた内容は必ず1つずつ「Plan/Act」を経てユーザーに確認しながら実装すること。Planで実装計画を立てた後、Actで実装に入った場合「現在のタスク」に列挙されたタスクを一度に全部こなしてはいけません。必ず1つずつPlan→Actを行い、1つ完了したらユーザーに確認し、Planで再び実装計画から行ってください。

## 現在のタスク
1. Firestoreにアクセスするための依存関係を追加するとともに、テスト結果保存処理とテスト結果取得処理を作る。
2. `/run_tests` APIのRequestに `testCaseId` を追加する。
3. `/run_tests` APIの処理で"ENV != dev"の場合のみテスト実行後にテスト結果保存処理を呼び出す。
4. `siteId` を指定してFirestoreからテスト結果を取得する新しいAPI (`/get_test_results`) を実装する。


## 最近の変更
- (以前のタスク完了) `site_id` パラメータの追加とスクリーンショット保存パスの変更。

## 次のステップ
1. `requirements.txt` に `google-cloud-firestore` を追加。
2. Firestore操作用のヘルパーモジュール (`firestore_client.py` など) を作成。
3. `app.py` を修正し、`/run_tests` にFirestore保存ロジックと `testCaseId` の処理を追加。環境変数 `ENV` をチェックし、`dev` 以外の場合のみ保存を実行する。
4. `app.py` に新しいAPIエンドポイント `/get_test_results` を追加し、Firestoreからのデータ取得ロジックを実装。
5. Firestore関連処理のユニットテストを作成・更新 (`.clinerules` に従う)。
6. `activeContext.md` を更新。
