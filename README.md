# 概要
このアプリはE2Eテストを支援するサーバーアプリです。
テスト対象のWebサイトURLとサイトID、テストケース(json)を受け取り、PlayWrightライブラリを使用してテストケースを実行し結果をレスポンスで返します。可能な限り簡単かつシンプルな構成を心がけて開発しています。

- ローカル: Dockerコンテナを起動し、curlコマンドでAPIをテストできる。特にクラウドサービスは使用しない
- リモート: `CloudRun`上にデプロイして稼働させる。`Cloud Storage`や`Firestore`など`Google Cloud`のサービスを使用する

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
      2. テスト対象サイトID
      3. テストケース(jsonオブジェクト)
   5. レスポンス:
      1. 実行結果（成功・失敗、ログ、失敗理由など）

# ディレクトリ構成
project_root/  
├── app.py  
├── actions/  
│　　　├── base.py  
│　　　├── click.py   
│　　　└── ...  
├── tests/  
│　　　├── test_input_action.py  
│　　　├── test_click_action.py  
│　　　└── ...  
├── requirements.txt  
└── dockerfile  

- `actions/`: ここにアクションを1ファイルずつ分けて入れる
- `base.py`: 実装するアクションは必ずbase.pyを継承する
- `tests/`: アクションを実装したら必ずテストも実装する

# テストケースのjson仕様
独自仕様のテストケースjsonを読み込み、パースしてそれぞれのactionを実行します。actionの仕様は以下の通りです。サンプルのjsonが必要な場合は同ディレクトリの`sample_test_case.json`を確認してください。

|     要素名    |     内容     |
| ------------ | ------------- |
| action       | 実行する操作。input, click, wait, assertExists, assertText, screenshot |
| selector     | CSSセレクタ |
| value        | 入力値。inputアクション時のみ使用 |
| secondswait  | アクション時に待機する秒数 |
| exists       | assert時に要素が存在すべきかどうか(true/false) |

# APIの認証について
CloudRun上にデプロイするとエンドポイントを知っていれば誰でも実行できます。しかし、第三者がこのAPIを実行しても特に盗用される情報はありません。
そこでガチガチにセキュリティを固めることはせず最低限のセキュリティを担保する設計としてAPI Keyを採用することにしました。
API Keyは環境変数で指定します。curlコマンドで"Authorization"を指定することで容易に検証が可能となります。

# スクリーンショットについて
スクリーンショットアクションを使うとスクリーンショットを取得し、`YYYYMMDDHHMMSS.png`というファイル名で保存します。保存先のディレクトリ仕様は以下のとおりです。

- ENVが"dev"の場合
  - Dockerコンテナ内の`/output/[siteId]/[日付]/[ファイル名]`に保存されます。
- ENVが"dev"でない場合
  - `Cloud Storage`に保存します。

## Cloud Storageの仕様
- バケット名の取得
  - 環境変数`CLOUD_STORAGE_BUCKET`から取得します。この環境変数が設定されていない場合のデフォルト値は"e2e-test-screenshots"です。(config.py)
- 保存先
  - バケット内のパス（オブジェクト名）は`CLOUD_STORAGE_BUCKET/[siteId]/日付/ファイル名`という形式になります。

# テスト
テストツールは`pytest`を使用しており、テストを書く対象（粒度）を分けて考えます。

|      テスト対象     | 内容 |
| ------------------ | ----- |
| 各アクションクラス | InputActionやClickActionなどのexecute関数の動作検証 |
| Factory         | 正しいクラスが返ってくるか（入力に応じて） |
| API(/run_tests) | curlで叩いたときに意図したレスポンスが返るか |

テストを実行する場合のコマンド
```sh
// 新たにライブラリを追加した場合
pip install -r requirements.txt

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