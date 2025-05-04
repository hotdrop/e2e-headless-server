# Active Context

## 必ず守ること
- 現在のタスクに書かれた内容は必ず1つずつ「Plan/Act」を経てユーザーに確認しながら実装すること。Planで実装計画を立てた後、Actで実装に入った場合「現在のタスク」に列挙されたタスクを一度に全部こなしてはいけません。必ず1つずつPlan→Actを行い、1つ完了したらユーザーに確認し、Planで再び実装計画から行ってください。

## 現在のタスク
1. ~~Firestoreにアクセスするための依存関係を追加するとともに、テスト結果保存処理とテスト結果取得処理を作る。~~ **完了**
2. `/run_tests` APIのRequestに `testCaseId` を追加する。 **← 次のタスク**
3. `/run_tests` APIの処理でテスト実行後にテスト結果保存処理を呼び出す。
4. `siteId` を指定してFirestoreからテスト結果を取得する新しいAPI (`/get_test_results`) を実装する。


## 最近の変更
- Firestore依存関係 (`google-cloud-firestore`) を `requirements.txt` に追加。
- Firestore操作用モジュール `firestore_client.py` を作成 (`save_test_result`, `get_test_results_by_site` 関数を含む)。
- 依存関係をインストール (`pip install -r requirements.txt`)。
- (以前のタスク完了) `site_id` パラメータの追加とスクリーンショット保存パスの変更。

## 次のステップ
1. `app.py` を修正し、`/run_tests` APIのRequestパラメータに `testCaseId` を追加する。
2. `app.py` を修正し、 `firestore_client.save_test_result` を呼び出すようにする。
3. `app.py` に新しいAPIエンドポイント `/get_test_results` を追加し、`firestore_client.get_test_results_by_site` を呼び出して結果を返すように実装する。
4. Firestore関連処理のユニットテストを作成・更新 (`.clinerules` に従う)。
5. `activeContext.md` を更新。
