class LocatorResolverMixin:
    def _resolve_locator(self, page, selector: dict, default_role_type: str = None):
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
