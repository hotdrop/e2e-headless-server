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
このアクションは、検証対象の要素を指定するために以下の形式のセレクタをサポートしています。

### 文字列セレクタ
- CSSセレクタまたはXPathを指定します。
- 例: "div#user-profile", "//header//img[@alt='Logo']"

### 辞書型セレクタ
Playwrightの`Locator API`に基づいて辞書形式でセレクタを指定します。サポートしている`by`の種類と、それに応じたパラメータは以下の通りです。

#### `by: "role"`: ARIAロール
- `type`: (必須) ARIAロール名 (例: button, dialog, listitem)。このアクションでは、ロールタイプを指定する必要があります。
- `name`: (任意) アクセシブルネーム。要素を特定するための名前。

```json
"selector": {
  "by": "role",
  "type": "navigation",
  "name": "メインメニュー"
}
```

#### `by: "text"`: 表示テキスト
- `text`: (必須) 検索するテキスト文字列。このテキストを含む要素を探します。
```json
"selector": {
  "by": "text",
  "text": "エラーメッセージが表示されました"
}
```

#### `by: "placeholder"`: プレースホルダーテキスト
- `text`: (必須) input要素などのプレースホルダー属性のテキスト文字列。
```json
"selector": {
  "by": "placeholder",
  "text": "必須項目"
}
```

#### `by: "label"`: ラベルテキスト
- `name`: (必須) input要素などに関連付けられたラベル要素のテキスト文字列。
```json
"selector": {
  "by": "label",
  "name": "利用規約の同意チェックボックス"
}
```

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