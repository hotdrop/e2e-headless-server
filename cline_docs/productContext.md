# Product Context

## プロジェクトの目的
このプロジェクトは、E2E（エンドツーエンド）テストを支援するためのサーバーアプリケーションを開発することを目的としています。

## 解決する問題
WebアプリケーションのE2Eテストを手動または複雑な設定で行う手間を削減します。特に、テストケースをJSON形式で定義し、APIリクエストを通じて簡単にテストを実行できる環境を提供することで、開発プロセスを効率化します。

## 主要技術スタック
- プログラミング言語: Python
- Webフレームワーク: Flask
- E2Eテストライブラリ: Playwright (Chromiumブラウザを使用)
- コンテナ化: Docker
- テストフレームワーク: pytest

# ディレクトリ構成
project_root/
├── app.py
├── config.py
├── actions/     # テストケースJSONのacionを実装する場合はここ
│　　　├── base.py
│　　　├── click.py
│　　　└── ...
├── tests/       # テストケースJSONのactionを実装した場合は必ずユニットテストも実装する
│　　　├── test_input_action.py
│　　　├── test_click_action.py
│　　　└── ...
├── services/    # 利用サービスの実装はここ
│　　　├── firestore_client.py
│　　　└── storage.py
├── cline_docs/  # MemoryBankで使用するdocs
│　　　└── ...
├── design_docs/ # アクションや利用サービスの実装仕様。アクションの実装を把握したい場合はここのドキュメントを参照のこと
│　　　├── action_design_xxxx.md
│　　　└── ...
├── requirements.txt
└── dockerfile

## アーキテクチャ概要
- FlaskベースのAPIサーバーとして構築されています。
- 2つのエンドポイントを持ちます。
  - `/run_tests`API仕様
    - メソッド: POST
    - APIリクエストのパラメータとしてJSONオブジェクトでテストケースを受け取ります
    - APIキー認証を採用します。過度に複雑なセキュリティは避けつつ、完全な公開状態を防ぐためです。API Keyは環境変数で設定します。
    - 実行結果をJSON形式でレスポンスします。
  - `/get_results/<site_id>`API仕様
    - メソッド: GET
    - APIリクエストのパラメータとしてsiteIdを受け取ります
    - APIキー認証を採用します。過度に複雑なセキュリティは避けつつ、完全な公開状態を防ぐためです。API Keyは環境変数で設定します。
    - 対象siteIdのテスト結果をリスト形式でレスポンスします。
- Playwrightライブラリを使用して、受け取ったテストケースに基づきブラウザ操作を実行します。
- Dockerコンテナとして実行されることを前提としています。なお、`playwright install --with-deps chromium` により依存関係を管理します。

## 設計パターン
- Actionクラス: 各テスト操作（クリック、入力など）は `actions/` ディレクトリ内に個別のPythonファイルとして実装されます。
- 継承: 全てのアクションクラスは `actions/base.py` のベースクラスを継承する必要があります。
- Factoryパターン: `actions/factory.py` が存在することから、テストケースJSONの `action` 要素の値に基づいて適切なアクションクラスのインスタンスを生成するFactoryパターンが使用されていると考えられます。
- テスト駆動開発: `tests/` ディレクトリが存在し、アクションごとにテストファイルが用意されていることから、テスト駆動開発またはそれに準じた開発スタイルが推奨されています。各アクションの実装と同時にテストも実装することが求められます。

## 期待される動作
- APIリクエストでテスト対象のWebサイトURLとテストケース（JSON形式）を受け取ります。
- 受け取ったテストケースに基づき、Playwrightライブラリを使用してヘッドレスブラウザで指定されたactionを実行します。
- テストの実行結果（成功/失敗、ログ、失敗理由など）をAPIレスポンスとして返します。
- ローカル環境（Docker）およびリモート環境（Google Cloud Run）での実行をサポートします。
- APIキーによる簡単な認証メカニズムを備えます。

## テストケースでサポートしているaction
テストケースでサポートしているactionは以下のとおりです。

|   action name   |  overview  |
| --------------- | ------------- |
| input           | 入力ボックスへの入力 |
| click           | クリック操作 |
| scrollIntoView  | 指定要素までスクロールする |
| wait            | 停止秒数の間、待機 |
| waitForSelector | 要素が指定の状態になるまで待機 |
| screenshot      | 表示されている画面のスクリーンショットを取得 |
| assertExists    | 指定の要素の存在確認 |
| assertText      | 指定の要素の文字列を確認 |

## 各仕様書
`design_docs/`ディレクトリに各アクションや利用サービスの詳細仕様書があります。必要に応じて読み込んでください。

- design_docs/action_design_xxx.md: xxxにはaction名が入ります。各アクションの詳細仕様を記載しています。
- design_docs/cloudrun_access.md: CloudRunのデプロイ方法等を記載しています。
- design_docs/firestore_access.md: テスト結果をFirestoreへ保存する処理と、テスト結果をFirestoreから取得する処理の仕様を記載しています。
