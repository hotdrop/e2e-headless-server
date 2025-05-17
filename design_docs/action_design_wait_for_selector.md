# WaitForSelector アクション

## 概要
指定されたセレクタに一致する要素が、特定の状態になるまで待機します。非同期で表示が変わる要素の出現や非表示を待つために使用されます。

## 詳細
- このアクションは、セレクタの形式に応じてPlaywrightの以下のいずれかを実行します。
  - `page.wait_for_selector()`: 文字列セレクタの場合
  - `locator.wait_for()`: 辞書型セレクタの場合
- `selector`が辞書型で`by: "role"`を指定する場合、`type`パラメータは必須です。このアクションでは`type`のデフォルト値は設定されません。
- 指定された`timeout`内に要素が期待する`state`にならない場合、テストはエラーで失敗します。
- `state`に指定可能なパラメータは以下のとおりです。
  - attached: 要素がDOMにアタッチされている状態。
  - detached: 要素がDOMからデタッチされている状態。
  - visible: 要素が表示されている状態。state省略時のデフォルトパラメータ。サイズがあり、`visibility:visible`、`opacity > 0`
  - hidden: 要素が非表示の状態 (サイズがない、または `visibility:hidden`、`display:none`)
- `state`パラメータを理解し、テストケースの意図に合わせて適切に設定することが重要です。

## パラメータ
このアクションで使用できるパラメータは以下の通りです。

| Key        | 型              | 必/任 | 説明              |
|------------|-----------------|------|------------------|
| `action`   | string          | 必須  | "waitForSelector" |
| `selector` | string / object | 必須  | 操作対象の要素。セレクタ参照のこと |
| `state`    | string          | 任意  | "attached", "detached", "visible"(デフォルト), "hidden"いずれかの値を指定 |
| `timeout`  | integer         | 任意  | 待機する最大時間（ミリ秒）。この時間内に指定された状態にならない場合、エラーが発生します。デフォルトは 10000 (10秒) です。 |

## セレクタ
`./selector_design.md`を参照のこと

## JSONサンプル
ローディングスピナーが非表示になるまで待つ
```json
{
  "action": "waitForSelector",
  "selector": "#loading-spinner",
  "state": "hidden",
  "timeout": 15000
}
```

特定のテキストが表示されるまで待つ (辞書型セレクタ)
```json
{
  "action": "waitForSelector",
  "selector": {
    "by": "text",
    "text": "ようこそ、ユーザー名さん"
  },
  "state": "visible"
}
```

ダイアログが表示されるまで待つ (文字列セレクタ)  
(この場合、state はデフォルトの"visible"が使用されます)
```json
{
  "action": "waitForSelector",
  "selector": "div.modal-dialog[role='dialog']"
}
```
