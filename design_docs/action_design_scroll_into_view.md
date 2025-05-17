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
`./selector_design.md`を参照のこと

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
