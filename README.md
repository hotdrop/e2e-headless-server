# 概要
このアプリはE2Eテストを支援するサーバーアプリです。APIは一つで、リクエストでテスト対象のWebサイトURLとテストケース(json)を与えられると、PlayWrightライブラリを使用してヘッドレスで指定されたアクションを実行して結果をレスポンスで返します。可能な限り簡単に実行できるよう実行環境は以下が実現できるようにします。
- ローカル
  - Dockerコンテナを起動し、curlコマンドでAPIをテストできる。特にクラウドサービスは使用しない
- リモート
  - 社内のテスターが使用するためCloudRun上にアップする。GoogleCloudのサービスを使う

# 構成要素の整理
1. 環境・技術スタック
   1. 言語: python
   2. HTTPサーバー: Flask
   3. E2Eテストライブラリ: Playwright
   4. 実行環境: Docker
2. API仕様
   1. エンドポイント: `/run_tests`
   2. メソッド: POST
   3. ヘッダー: APIKeyで認証
   4. リクエストのパラメータ:
      1. テスト対象URL
      2. テストケース(jsonオブジェクト)
   5. レスポンス:
      1. 実行結果（成功・失敗、ログ、失敗理由など）

# ディレクトリ構成
project_root/
├── app.py
├── actions/     // ここにアクションを1ファイルずつ分けて入れる
│   ├── base.py  // 実装するアクションは必ずbase.pyを継承する
│   ├── click.py
│   └── ...
├── tests/       // アクションを実装したら必ずテストも実装する
│   ├── test_input_action.py
│   ├── test_click_action.py
│   └── ...
├── requirements.txt
└── dockerfile

# 開発ルール
- PEP 8に準拠
- actionクラスは必ずbase.pyを継承すること
- 新規action追加時は必ずテストも実装すること

# テストケースのjson仕様
独自仕様のテストケースjsonを読み込み、パースしてそれぞれのactionを実行します。actionの仕様は以下の通りです。サンプルのjsonが必要な場合は同ディレクトリの`sample_test_case.json`を確認してください。

|     要素名    |     内容     |
| ------------ | ------------- |
| action       | 実行する操作。input, click, wait, assertExists |
| selector     | CSSセレクタ |
| value        | 入力値。inputアクション時のみ使用 |
| secondswait  | アクション時に待機する秒数 |
| exists       | assert時に要素が存在すべきかどうか(true/false) |

# APIの認証について
CloudRun上にデプロイするとURLを知っていれば誰でもAPIを実行できてしまうためセキュリティ的に良くないです。かといって第三者がこのAPIを実行しても特に盗用される情報はありません。そこでガチガチにセキュリティを固めることはせず、でもフル開放状態にはしない設計としてAPI Keyを採用することにしました。
API Keyは以下の仕様とします。
- ローカルで実行する場合
  - docker run時に環境変数でAPIKeyを指定します、curlコマンドで"Authorization"を指定することで容易に検証が可能となります。
- CloudRun上で実行する場合
  - APIKeyが漏れた場合に容易に変更管理できるようGoogleCloudのSecretManagerを使う予定です（未実装）

# テスト
テストツールは`pytest`を使用しており、テストを書く対象（粒度）を分けて考えます。

|      テスト対象     | 内容 |
| ------------------ | ----- |
| 各アクションクラス | InputActionやClickActionなどのexecute関数の動作検証 |
| Factory         | 正しいクラスが返ってくるか（入力に応じて） |
| API(/run_tests) | curlで叩いたときに意図したレスポンスが返るか |

テストを実行する場合のコマンド
```sh
// ventで仮想環境を作っている場合
source .venv/bin/activate

// テスト実行
pytest tests/
```

# 動作確認手順
```
// イメージ作成
docker build -t e2e-server .

// サーバー実行
docker run -p 8080:8080 -v $(pwd)/output:/output -e ENV=dev -e API_KEY=KEY12345 e2e-server

// サンプルのテストケース実行
curl -X POST http://localhost:8080/run_tests -H "Authorization: Bearer KEY12345" -H "Content-Type: application/json" -d @sample_test_case.json
```


# 将来的に追加しても良いアクション
|      action名    |     内容     |
| ---------------- | ------------- |
| press_key        | エンターキーやタブなどのキー操作 |
| hover            | 要素にマウスをホバーする |
| scroll_into_view | 特定要素までスクロール |

# 過去の検討事項まとめ
## SeleniumとPlaywrightどちらを採用すべきか？
Playwrightの方が良い。WebDriverが不要だったり非同期処理に長けている。Microsoftが開発元なのも強い。
## FlaskかFastAPIか
すぐにシンプルな構成で始めたい場合はFlask、長期的に保守・拡張を視野に入れて非同期処理を前提にしたい場合はFastAPiが良いとのこと。
## テストケースのjsonはAPIで渡すべきか？ファイルにするべきか？
「開発スピード」と「疎結合な構成」を両立させたいなら、まずAで構築してBへの移行余地を残す設計（パラメータにjson or json_uri）が良いです。Playwrightコード側も、受け取るJSONの構造が一定ならファイルからでもインラインでも同じパース処理で使えるようにしておくのが望ましい。
したがって、あらかじめJSONを作っておいてRequestのパラメータで指定する。もしjsonが大きくなってきたらファイルパスを送ってE2Eテストサーバー側でファイルを見に行ってjsonをパースする方式にする可能性もある
## dockerfile
`playwright install --with-deps chromium`によって必要なブラウザと依存ライブラリがまとめてインストールされるので別途Chromeなどは不要。slimベースを使い不要なパッケージを避けている。（軽量化意識）Playwrightは自動的にヘッドレスモードで動作する（もちろん非ヘッドレスにも切り替え可）。あとでgunicornに差し替える余地を残しているが、今はFlaskの内蔵サーバーでOK。