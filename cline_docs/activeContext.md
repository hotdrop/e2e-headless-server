# Active Context

## 必ず守ること(編集禁止)
現在のタスクに書かれた内容は必ず1つずつ「Plan/Act」を経てユーザーに確認しながら実装すること。Planで実装計画を立てた後、Actで実装に入った場合「現在のタスク」に列挙されたタスクを一度に全部こなしてはいけません。必ず1つずつPlan→Actを行い、1つ完了したらユーザーに確認し、Planで再び実装計画から行ってください。

## Current Task: Playwright Locator API対応とMixin化

現在、e2eテストサーバーのアクション (`assert_exists.py`, `assert_text.py`, `scroll_into_view.py`) を修正し、PlaywrightのLocator API構文（辞書形式のセレクタ）に対応させる作業を行っています。また、各アクションファイルに点在する `_resolve_locator` メソッドを共通のMixinクラスとして切り出し、コードの共通化とメンテナンス性向上を目指します。

## Recent Changes

- 実装計画の策定とユーザーによる承認。
- `actions/mixins.py` を作成し、`LocatorResolverMixin` を実装。`_resolve_locator` メソッドに `default_role_type` パラメータを追加。
- `actions/assert_exists.py`, `actions/assert_text.py`, `actions/scroll_into_view.py` を修正し、`LocatorResolverMixin` を使用するように変更。セレクタが文字列または辞書の場合に対応。
- `actions/input.py`, `actions/click.py` をリファクタリングし、`LocatorResolverMixin` を使用するように変更。ローカルの `_resolve_locator` メソッドを削除し、Mixinのメソッド呼び出し時に適切な `default_role_type` を指定。
- `tests/test_assert_text_action.py` および `tests/test_scroll_into_view_action.py` に、辞書形式セレクタ（`by:role`, `by:text`）および不正なセレクタ形式に対応するユニットテストケースを追加・修正。

## Next Steps
ユニットテストの追加・更新: 以下のアクションについて、文字列セレクタおよび辞書形式セレクタ（`role`, `text`）での動作を検証するテストケースを追加・更新する。また、不正なセレクタ形式の場合のテストも追加する必要がある。

- [x] input **完了**
- [x] click **完了**
- [x] assert_exists **完了**
- [x] assert_text **完了**
- [x] scroll_into_view **完了**
