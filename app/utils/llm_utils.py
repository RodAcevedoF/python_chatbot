from typing import Any
import json


def normalize_response(response_or_content: Any) -> str:
    content = getattr(response_or_content, "content", response_or_content)

    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(item.get("content") or item.get("text") or item.get("message") or json.dumps(item, ensure_ascii=False))
            else:
                parts.append(str(item))
        return "\n".join(parts)

    if isinstance(content, dict):
        return content.get("content") or content.get("text") or content.get("message") or json.dumps(content, ensure_ascii=False)

    return str(content)
