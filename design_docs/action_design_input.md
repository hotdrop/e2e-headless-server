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
`./selector_design.md`を参照のこと

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
