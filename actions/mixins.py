class LocatorResolverMixin:
    def _resolve_locator(self, page, selector: dict, default_role_type: str = None):
        # チェインされたセレクタの処理
        if "chain" in selector:
            locator = None
            for chain_selector in selector["chain"]:
                if locator is None:
                    locator = self._resolve_single_locator(page, chain_selector, default_role_type)
                else:
                    locator = locator.locator(self._resolve_single_locator(page, chain_selector, default_role_type))
            
            # インデックス指定の処理
            if "index" in selector:
                index = selector["index"]
                if not isinstance(index, int) or index < 0:
                    raise ValueError(f"Invalid index value: {index}")
                locator = locator.nth(index)
            else:
                # インデックスが指定されていない場合、最初の要素を選択
                locator = locator.first
            
            return locator
        
        # 従来の単一セレクタの処理
        return self._resolve_single_locator(page, selector, default_role_type)

    def _resolve_single_locator(self, page, selector: dict, default_role_type: str = None):
        by = selector.get("by")
        if by == "role":
            return page.get_by_role(selector.get("type", default_role_type), name=selector.get("name"))
        elif by == "text":
            return page.get_by_text(selector.get("text"))
        elif by == "placeholder":
            return page.get_by_placeholder(selector.get("text"))
        elif by == "label":
            return page.get_by_label(selector.get("name"))
        # 他のパターンも拡張可能
        raise ValueError(f"Unsupported selector 'by' value: {by} in {selector}")
