# 第一弾
## 目標
ローカルでDockerコンテナを起動し、curlコマンドでAPIを実行し、PlaywrightによるE2Eテストが実行され、結果が返ってくること
## 構成要素の整理
1. 環境・技術スタック
   1. python、Flask使用
   2. E2Eテストライブラリ: Playwright
   3. 実行環境: Docker
2. API設計（エンドポイント）
   1. POSTリクエストでパラメータは以下の通り
      1. テスト対象URL
      2. テストケース(jsonオブジェクト)
   2. レスポンス: 実行結果（成功・失敗、ログ、失敗理由など）
## ディレクトリ構成
project_root/
├── app.py
├── actions/
├── tests/
│   ├── test_input_action.py
│   ├── test_click_action.py
│   └── ...
├── requirements.txt
└── dockerfile

## サーバーアプリ
Flaskでサーバーを立てている。POSTでエンドポイントは`/run_tests`となる。Play Wrightで実装しているため独自仕様のテストケースjsonを読み込み、パースしてそれぞれのactionを実行する。actionの仕様はテストケースの欄に記載。
### テスト
テストツールは`pytest`とする。テストを書く対象（粒度）を分けて考える。

|      テスト対象     | 内容 |
| ------------------ | ----- |
| 🔹 各アクションクラス | InputActionやClickActionなどのexecute関数の動作検証 |
| 🔹 Factory         | 正しいクラスが返ってくるか（入力に応じて） |
| 🔸 API(/run_tests) | curlで叩いたときに意図したレスポンスが返るか |

## テストケースjsonの仕様
|     要素名    |     内容     |
| ------------ | ------------- |
| action       | 実行する操作。input, click, wait, assertExists |
| selector     | CSSセレクタ |
| value        | 入力値。inputアクション時のみ使用 |
| secondswait  | アクション時に待機する秒数 |
| exists       | assert時に要素が存在すべきかどうか(true/false) |
## 今後あっても良いアクション
|      action名    |     内容     |
| ---------------- | ------------- |
| assert_text      | 特定の要素内に特定のテキストが含まれるか検証 |
| screenshot       | スクリーンショットを撮って特定のディレクトリに保存 |
| press_key        | エンターキーやタブなどのキー操作 |
| hover            | 要素にマウスをホバーする |
| scroll_into_view | 特定要素までスクロール |

## 動作確認手順
1. イメージ作成
   1. docker build -t e2e-server .
2. サーバー実行
   1. docker run -p 8080:8080 e2e-server
3. テスト実行
   1. curl -X POST http://localhost:8080/run_tests -H "Content-Type: application/json" -d @sample_test_case.json



# 検討事項まとめ
## SeleniumとPlaywrightどちらを採用すべきか？
Playwrightの方が良い。WebDriverが不要だったり非同期処理に長けている。Microsoftが開発元なのも強い。
## FlaskかFastAPIか
すぐにシンプルな構成で始めたい場合はFlask、長期的に保守・拡張を視野に入れて非同期処理を前提にしたい場合はFastAPiが良いとのこと。
## テストケースのjsonはAPIで渡すべきか？ファイルにするべきか？
「開発スピード」と「疎結合な構成」を両立させたいなら、まずAで構築してBへの移行余地を残す設計（パラメータにjson or json_uri）が良いです。Playwrightコード側も、受け取るJSONの構造が一定ならファイルからでもインラインでも同じパース処理で使えるようにしておくのが望ましい。
したがって、あらかじめJSONを作っておいてRequestのパラメータで指定する。もしjsonが大きくなってきたらファイルパスを送ってE2Eテストサーバー側でファイルを見に行ってjsonをパースする方式にする可能性もある
## dockerfile
`playwright install --with-deps chromium`によって必要なブラウザと依存ライブラリがまとめてインストールされるので別途Chromeなどは不要。slimベースを使い不要なパッケージを避けている。（軽量化意識）Playwrightは自動的にヘッドレスモードで動作する（もちろん非ヘッドレスにも切り替え可）。あとでgunicornに差し替える余地を残しているが、今はFlaskの内蔵サーバーでOK。
