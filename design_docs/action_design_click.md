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
`./selector_design.md`を参照のこと

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

