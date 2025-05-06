# Cline Rules for E2E Test Server Project
このファイルは、Clineがこのプロジェクトで開発を行う際に従うべきルールを定義します。

## 1. 全体のルール
- 回答は必ず日本語でしてください。
- ソフトウェア開発の基本原則を遵守しましょう。DRY原則、YAGNI、SOLID原則などです。ただし、SOLID原則はOOPの原則なので、pythonには必ずしも有効ではありません。原則よりもpythonの基本的な原則やベストプラクティスを優先して問題ありません。

## 2. Actionの実装ルール
- 新規Action: 新しいAction（例: `scroll_into_view`, `press_key`）を実装する場合`actions/`ディレクトリ内に`[Action名].py`というファイル名で作成します。
- Baseクラスの継承: 全てのActionクラスは`actions/base.py`内で定義されているBaseActionクラスを必ず継承してください。
- ファイル分割: 1つのActionにつき1つのPythonファイルを作成します。
- 実装の注意点: 新しいActionを実装する際は必ず既存のActionの作りにあわせてください。

## 3. テストの実装ルール
- テスト必須: 新しいActionクラスを実装した場合、または既存のActionクラスを修正した場合、`screenshot`以外のActionは必ず対応するユニットテストを`tests/`ディレクトリに追加または更新してください。`screenshot`Actionはテストを作成する必要はありません。
- テストファイル命名規則: テストファイル名は test_Action名.py`の形式に従ってください（例: `test_input_action.py`）
- テストフレームワーク: テストの記述と実行には`pytest`を使用します。

## 4. コーディング規約
- 既存コードへの準拠: 新しいコードを追加・修正する際は、既存のコードのスタイル、命名規則、構造に合わせてください。
- Pythonベストプラクティス: PEP 8などのPythonコミュニティで一般的に受け入れられているコーディング規約に従ってください。
- コメントとドキュメンテーション: 必要に応じてコードにコメントを追加し、複雑なロジックや意図を明確にしてください。主要な関数やクラスにはdocstringを追加することを推奨します。

## 5. 依存関係管理
- `requirements.txt`の更新: 新しい外部ライブラリを追加した場合は、必ず`requirements.txt`に追加してください。
- インストール: `requirements.txt`を更新した後は、`pip install -r requirements.txt`を実行して依存関係をインストールしてください（必要であれば仮想環境を有効化した後）。

## 6. 実行環境と設定
- Docker優先: 開発、テスト、実行は主にDockerコンテナ内で行うことを前提とします。`dockerfile`を使用して環境を構築・維持してください。
- APIキー: 環境変数`API_KEY`を使用してAPIキーを設定します。Cloud Run環境上でも同様です。

## 7. Memory Bankの利用
- 開発開始時: タスクを開始する前に`cline_docs/`ディレクトリ内のすべてのMemory Bankファイル（`productContext.md`, `nextTask.md`, `activeContext.md`）を読み込み、現在のプロジェクト状況とコンテキストを完全に理解してください。
- ドキュメント更新: 大規模な変更や重要な決定を行った場合は、関連するMemory Bankファイルを更新してください。特に`activeContext.md`は現在の作業状況を反映するように維持してください。
