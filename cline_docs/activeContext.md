# Active Context

## 現在のタスク
- (完了) APIリクエストに `site_id` パラメータを追加する。
- (完了) スクリーンショットの保存パスを `日付/ファイル名` から `site_id/日付/ファイル名` に変更する。

## 最近の変更
- `app.py`: `/run_tests` エンドポイントで `site_id` を受け取り、`run_test_flow` および `ActionFactory` に渡すように修正。
- `actions/factory.py`: `create` メソッドが `site_id` を受け取り、指定された引数順序でアクションコンストラクタに渡すように修正。
- `actions/base.py`: `__init__` メソッドが `site_id` を受け取り、指定された引数順序 (`self, site_id, step`) で初期化するように修正。
- `actions/screenshot.py`: `execute` メソッド内で `save_screenshot` に `self.site_id` を渡すように修正。
- `storage.py`: `save_screenshot` メソッドおよび内部メソッドが `site_id` を受け取り、保存パス形式を `site_id/日付/ファイル名` に変更。
- `tests/test_factory.py`: `ActionFactory.create` のシグネチャ変更に合わせて修正。

## 次のステップ
- (完了) 1. `app.py` を修正。
- (完了) 2. `actions/factory.py` と `actions/base.py` を修正。
- (完了) 3. `actions/screenshot.py` を修正。
- (完了) 4. `storage.py` を修正。
- (完了) 5. 関連するユニットテスト (`tests/test_factory.py`) を修正。(他のテストはユーザーが修正)
- (完了) 6. `activeContext.md` を更新。
- 全ての修正が完了しました。
