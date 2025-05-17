# AssertExists アクション

## 概要
指定されたセレクタに一致する要素がページ上に存在するかどうか、または存在しないかどうかを検証（アサート）します。

## 詳細
- このアクションは、Playwrightの`locator.count()`メソッドを使用して、セレクタに一致する要素の数を取得し、その数が0より大きいかどうかで存在を判断します。
- `exists`パラメータが true (デフォルト) の場合、要素が存在しないと`AssertionError`を発生させます。
- `exists`パラメータが false の場合、要素が存在すると`AssertionError`を発生させます。
- `selector`が辞書型で`by: "role"`を指定する場合、`type`パラメータは必須です。このアクションでは`type`のデフォルト値は設定されません。

## パラメータ
このアクションで使用できるパラメータは以下の通りです。

| Key        | 型              | 必/任 | 説明              |
|------------|-----------------|------|------------------|
| `action`   | string          | 必須  | "assertExists" |
| `selector` | string / object | 必須  | 操作対象の要素。セレクタ参照のこと |
| `exists`   | boolean         | 任意  | 要素が存在することを期待する場合は true、存在しないことを期待する場合は false を指定します。デフォルトは true です。 |

## セレクタ
`./selector_design.md`を参照のこと

## JSONサンプル
特定の要素が存在することを検証する (デフォルトの exists: true)
```json
{
  "action": "assertExists",
  "selector": "#user-avatar"
}
```

特定のロールを持つ要素が存在することを検証する (辞書型セレクタ)
```json
{
  "action": "assertExists",
  "selector": {
    "by": "role",
    "type": "button",
    "name": "送信"
  }
}
```

特定の要素が存在しないことを検証する (exists: false)
```json
{
  "action": "assertExists",
  "selector": ".temp-loading-indicator",
  "exists": false
}
```

特定のテキストを持つ要素が存在しないことを検証する (辞書型セレクタ、exists: false)
```json
{
  "action": "assertExists",
  "selector": {
    "by": "text",
    "text": "古い通知メッセージ"
  },
  "exists": false
}
```