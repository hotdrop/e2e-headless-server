# セレクタ仕様
各アクションでサポートするセレクタ形式の仕様を記載します。

## 文字列セレクタ
- CSSセレクタまたはXPathを指定します。
- 例: "div#user-profile", "//header//img[@alt='Logo']"

## 辞書型セレクタ
Playwrightの`Locator API`に基づいて辞書形式でセレクタを指定します。サポートしている`by`の種類と、それに応じたパラメータは以下の通りです。

### `by: "role"`: ARIAロール
- `type`: (必須) ARIAロール名 (例: button, dialog, listitem)。一部のアクションでは、指定を省略した場合、デフォルト値が起用されます。
  - デフォルト値を持つアクションとその値
    - click アクション: "button"
    - input アクション: "textbox"
- `name`: (任意) アクセシブルネーム。要素を特定するための名前。

```json
"selector": {
  "by": "role",
  "type": "navigation",
  "name": "メインメニュー"
}
```

### `by: "text"`: 表示テキスト
- `text`: (必須) 検索するテキスト文字列。このテキストを含む要素を探します。
  - 注意: assertアクションの場合でも必要です。この text パラメータはセレクタ用であり、アサーション対象のテキストとは別に指定する必要があります。
```json
"selector": {
  "by": "text",
  "text": "エラーメッセージが表示されました"
}
```

### `by: "placeholder"`: プレースホルダーテキスト
- `text`: (必須) input要素などのプレースホルダー属性のテキスト文字列。
  - 注意: click アクションの場合、このプレースホルダーを持つ要素に関連付けられたクリック可能な要素を探す場合に利用できますが、通常は入力フィールド自体を指します。クリック対象がその要素自体であるか確認が必要です。
```json
"selector": {
  "by": "placeholder",
  "text": "必須項目"
}
```

### `by: "label"`: ラベルテキスト
- `name`: (必須) input要素などに関連付けられたラベル要素のテキスト文字列。
```json
"selector": {
  "by": "label",
  "name": "利用規約の同意チェックボックス"
}
```

## チェインされたセレクタ
複数のセレクタを連結して、より複雑な要素の特定が可能です。`chain`配列に複数のセレクタを指定し、順番に適用していきます。

```json
"selector": {
  "chain": [
    {
      "by": "role",
      "type": "row",
      "name": "sample@test.co.jp"
    },
    {
      "by": "role",
      "type": "button"
    }
  ]
}
```

### インデックス指定
セレクタで特定された複数の要素から、特定のインデックスの要素を選択できます。`index`パラメータで0から始まるインデックスを指定します。

```json
"selector": {
  "chain": [
    {
      "by": "role",
      "type": "row",
      "name": "sample@test.co.jp"
    },
    {
      "by": "role",
      "type": "button"
    }
  ],
  "index": 1
}
```
