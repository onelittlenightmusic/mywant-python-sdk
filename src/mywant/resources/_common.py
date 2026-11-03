from __future__ import annotations

from typing import Iterable, Optional, Union
from urllib.parse import quote

import yaml


def seg(part: str) -> str:
    """One path segment, escaped (a name may hold spaces or Japanese)."""
    return quote(part, safe="")


def csv(items: Iterable[str]) -> str:
    """Items for a ?ids= / ?names= list, escaped."""
    return quote(",".join(items), safe=",")


def yaml_text(data: Union[str, list, dict]) -> str:
    """YAML to send: a string as it is, a list or dict dumped."""
    if isinstance(data, str):
        return data
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)


def query(name: str, items: Optional[Iterable[str]]) -> str:
    items = list(items or [])
    return f"?{name}={csv(items)}" if items else ""
