# click アクション

## 概要
指定された要素を左クリックします。ボタン、リンク、チェックボックスなどのインタラクティブな要素の操作に使用されます。

## 詳細
- このアクションは、対象要素に対してPlaywrightの`locator.click()`メソッドを実行します。**Playwrightはクリックする前に要素がインタラクション可能になるまで自動的に待機します**（例：表示されている、有効であるなど）。
- `selector`が辞書型で`by: "role"`を指定し、かつ`type`を省略した場合、デフォルトで`type: "button"`として扱われます。これは `ClickAction`の実装で`default_role_type="button"`が指定されているためです。
- `by: "placeholder"`や`by: "label"`を使用する場合、特定される要素が直接クリック可能な要素であるか、またはPlaywrightが意図したクリック可能な要素を解決できるかを確認してください。これらのセレクタは主に入力フィールドやそのラベルを特定するために使用されます。

## パラメータ
このアクションで使用できるパラメータは以下の通りです。

| Key       | 型              | 必/任 | 説明        |
|-----------|-----------------|------|-------------|
| `action`  | string          | 必須 | "click"      |
| `selector`| string / object | 必須 | 操作対象の要素。セレクタ参照のこと |

## セレクタ
このアクションは、操作対象の要素を指定するために以下の形式のセレクタをサポートしています。

### 文字列セレクタ
- CSSセレクタまたはXPathを指定します。
- 例: "button#submit", "//a[@href='/login']"

### 辞書型セレクタ
Playwrightの`Locator API`に基づいた辞書形式でセレクタを指定します。
サポートしている `by` の種類と、それに応じたパラメータは以下の通りです。

#### `by: "role"`: ARIAロール
- `type`: (必須) ARIAロール名 (例: button, link, checkbox)。指定がない場合、このclickアクションではデフォルトで "button" として扱われます。
- name: (任意) アクセシブルネーム。要素を特定するための名前。
```json
"selector": {
  "by": "role",
  "type": "button",
  "name": "ログイン"
}
```

typeを省略した場合、デフォルトで"button"として探索します。

```json
"selector": {
  "by": "role",
  "name": "カートに追加" 
} 
```

#### `by: "text"`: 表示テキスト
- `text`: (必須) 検索するテキスト文字列。このテキストを持つ要素（通常はボタンやリンク）を探します。
```json
"selector": {
  "by": "text",
  "text": "続きを読む"
}
```

#### `by: "placeholder"`: プレースホルダーテキスト
- `text`: (必須) プレースホルダー属性のテキスト文字列。このプレースホルダーを持つ要素に関連付けられたクリック可能な要素を探す場合に利用できますが、通常は入力フィールド自体を指します。クリック対象がその要素自体であるか確認が必要です。
```json
"selector": {
  "by": "placeholder",
  "text": "検索キーワード"
}
```

#### `by: "label"`: ラベルテキスト
- `name`: (必須) ラベル要素のテキスト文字列。このラベルに関連付けられたクリック可能な要素（例: チェックボックス、ラジオボタン）を探します。
```json
"selector": {
  "by": "label",
  "name": "同意する"
}
```

## JSONサンプル
```json
{
  "action": "click",
  "selector": {
    "by": "role",
    "type": "button",
    "name": "検索"
  }
}
```

```json
{
  "action": "click",
  "selector": "a.nav-link[href='/profile']"
}
```

```json
{
  "action": "click",
  "selector": {
    "by": "text",
    "text": "利用規約に同意する"
  }
}
```

