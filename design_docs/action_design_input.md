# input アクション

## 概要
指定された要素に対して、指定された値を入力（フィルイン）します。主にテキストボックスやテキストエリアへの文字入力に使用されます。

## 詳細
- このアクションは、対象要素に対してPlaywrightの`locator.fill()`メソッドを実行します。これは入力フィールドの既存のテキストをクリアしてから新しい値を入力する動作をします。
- `selector`が辞書型で`by: "role"`を指定し、かつ`type`を省略した場合、デフォルトで`type: "textbox"`として扱われます。これは`InputAction`の実装で`default_role_type="textbox"`が指定されているためです。

## パラメータ
このアクションで使用できるパラメータは以下の通りです。

| Key      | 型              | 必/任 | 説明                                            |
|----------|-----------------|------|------------------------------------------------|
| `action`   | string          | 必須  | "input"                                       |
| `selector` | string / object | 必須  | 操作対象の要素。セレクタ参照のこと |
| `value`    | string          | 任意  | 入力する文字列。省略した場合は空文字列が入力されます    |

## セレクタ
このアクションは、操作対象の要素を指定するために以下の形式のセレクタをサポートしています。

### 文字列セレクタ
- CSSセレクタまたはXPathを指定します。
- 例: "input#username", "//textarea[@name='description']"

### 辞書型セレクタ
Playwrightの`Locator API`に基づいて辞書形式でセレクタを指定します。サポートしている`by`の種類と、それに応じたパラメータは以下の通りです。

#### `by: "role"`: ARIAロール
- `type`: (必須) ARIAロール名 (例: textbox, searchbox)。指定がない場合、このinputアクションではデフォルトで "textbox" として扱われます。
- `name`: (任意) アクセシブルネーム。要素を特定するための名前。

```json
"selector": {
  "by": "role",
  "type": "textbox",
  "name": "メールアドレス"
}
```

typeを省略した場合、デフォルトで"textbox"として探索します。

```json
"selector": {
  "by": "role",
  "name": "検索キーワード" 
} 
```

#### `by: "text"`: 表示テキスト
- `text`: (必須) 検索するテキスト文字列。このテキストを持つ要素に関連付けられた入力フィールドを探します。
```json
"selector": {
  "by": "text",
  "text": "ユーザーID"
}
```

#### `by: "placeholder"`: プレースホルダーテキスト
- `text`: (必須) input要素のプレースホルダー属性のテキスト文字列。
```json
"selector": {
  "by": "placeholder",
  "text": "メールアドレスを入力してください"
}
```

#### `by: "label"`: ラベルテキスト
- `name`: (必須) input要素に関連付けられたラベル要素のテキスト文字列。
```json
"selector": {
  "by": "label",
  "name": "パスワード"
}
```

## JSONサンプル
```json
{
  "action": "input",
  "selector": {
    "by": "role",
    "type": "textbox",
    "name": "メールアドレス"
  },
  "value": "user1@test.com"
}
```

```json
{
  "action": "input",
  "selector": "input[name='q']",
  "value": "Playwright test"
}
```

```json
{
  "action": "input",
  "selector": {
    "by": "placeholder",
    "text": "ここに検索語を入力"
  },
  "value": "自動テスト"
}
```
