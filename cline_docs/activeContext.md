# Active Context

## 現在のタスク
- APIリクエストに `site_id` パラメータを追加する。
- スクリーンショットの保存パスを `日付/ファイル名` から `site_id/日付/ファイル名` に変更する。

## 最近の変更
- (未実施)

## 次のステップ
1. `app.py` を修正し、`/run_tests` で `site_id` を受け取り、`run_test_flow` に渡す。
2. `actions/factory.py` と `actions/base.py` を修正し、アクションクラスが `site_id` を受け取れるようにする。
3. `actions/screenshot.py` を修正し、`save_screenshot` に `site_id` を渡す。
4. `storage.py` を修正し、`save_screenshot` が `site_id` を受け取り、新しいパス形式で保存するようにする。
5. 関連するユニットテストを修正する。
6. `activeContext.md` を更新する。（このステップは完了）
