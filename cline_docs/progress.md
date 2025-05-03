# Progress

## 現在動作するもの (README.mdに基づく推測)
-   基本的なFlaskサーバー (`app.py`) が存在します。
-   APIエンドポイント `/run_tests` が定義されている可能性があります。
-   Playwrightを使用した基本的なブラウザ操作アクション (`actions/` ディレクトリ内のファイル: `click.py`, `input.py`, `wait.py`, `assert_exists.py`, `assert_text.py`, `screenshot.py`, `scroll_into_view`) が実装されています。
-   アクションクラスのベースクラス (`actions/base.py`) が存在します。
-   アクションクラスを生成するFactory (`actions/factory.py`) が存在します。
-   各アクションに対するユニットテスト (`tests/` ディレクトリ内) が存在します。
-   Dockerによるコンテナ化 (`dockerfile`) が可能です。
-   ローカル環境での実行と基本的なAPIテストが可能です。
-   基本的なテストケースJSON (`sample_test_case.json`) があります。

## 未実装・将来的な機能
- `Cloud Run`へのデプロイ: READMEには記載がありますが、具体的な実装手順や設定は不明です。
- 追加アクション:
  - `press_key` (エンターキー、タブなど)
- テスト結果をFirestoreへ保存: 現在はAPIのResponseでテスト結果を返すのみですが、Firebaseへ保存も将来的には実装予定です。

## 全体的な進捗状況
基本的なE2Eテスト実行サーバーとしてのコア機能は実装されているようです。ローカルでの動作確認および`Cloud Run`へのデプロイは確認済みですが、テスト結果の保存機能は未実装です。将来的な機能拡張のアイデアもいくつか挙げられています。
