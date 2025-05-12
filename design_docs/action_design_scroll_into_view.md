# ScrollIntoView アクション

## 概要
指定された要素がビューポート内に表示されるようにページをスクロールします。要素が既にビューポート内に表示されている場合は、スクロールは行われません。

## 詳細
- このアクションは、対象要素に対してPlaywrightの`locator.scroll_into_view_if_needed()`メソッドを実行します。
- 要素がビューポート内に完全に表示されるようにスクロールされます。要素が既に表示されている場合、スクロールは行われません。
- `selector`が辞書型で`by: "role"`を指定する場合、`type`パラメータは必須です。`input`アクションや`click`アクションとは異なり、このアクションでは`type`のデフォルト値は設定されません。
- 指定された`timeoutMillis`内に要素が見つからない、またはスクロールできない場合、エラーを発生させます。

## パラメータ
このアクションで使用できるパラメータは以下の通りです。

| Key             | 型              | 必/任 | 説明              |
|-----------------|-----------------|------|------------------|
| `action`        | string          | 必須  | "scrollIntoView" |
| `selector`      | string / object | 必須  | 操作対象の要素。セレクタ参照のこと |
| `timeoutMillis` | integer         | 任意  | 要素が表示されるのを待つ最大時間（ミリ秒）。デフォルトは 5000 (5秒) です。 |

## セレクタ
このアクションは、操作対象の要素を指定するために以下の形式のセレクタをサポートしています。

### 文字列セレクタ
- CSSセレクタまたはXPathを指定します。
- 例: "div#footer", "//button[@id='load-more']"

### 辞書型セレクタ
Playwrightの`Locator API`に基づいて辞書形式でセレクタを指定します。サポートしている`by`の種類と、それに応じたパラメータは以下の通りです。

#### `by: "role"`: ARIAロール
- `type`: (必須) ARIAロール名 (例: button, link, heading)。このアクションでは、ロールタイプを指定する必要があります。
- `name`: (任意) アクセシブルネーム。要素を特定するための名前。

```json
"selector": {
  "by": "role",
  "type": "article",
  "name": "最新の投稿"
}
```

#### `by: "text"`: 表示テキスト
- `text`: (必須) 検索するテキスト文字列。このテキストを含む要素を探します。
```json
"selector": {
  "by": "text",
  "text": "ユーザーID"
}
```

#### `by: "placeholder"`: プレースホルダーテキスト
- `text`: (必須) input要素などのプレースホルダー属性のテキスト文字列。
```json
"selector": {
  "by": "placeholder",
  "text": "コメントを入力"
}
```

#### `by: "label"`: ラベルテキスト
- `name`: (必須) input要素などに関連付けられたラベル要素のテキスト文字列。
```json
"selector": {
  "by": "label",
  "name": "利用規約"
}
```

## JSONサンプル
```json
{
  "action": "scrollIntoView",
  "selector": {
    "by": "role",
    "type": "contentinfo" 
  }
}
```

```json
{
  "action": "scrollIntoView",
  "selector": "button.load-more-button",
  "timeoutMillis": 10000
}
```

```json
{
  "action": "scrollIntoView",
  "selector": {
    "by": "text",
    "text": "ページ最下部の著作権表示"
  }
}
```
