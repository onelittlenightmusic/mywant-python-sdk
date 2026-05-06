from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import MyWantClient


class PluginsResource:
    def __init__(self, client: "MyWantClient") -> None:
        self._c = client

    def list(self) -> list[str]:
        """Return list of plugin script URLs."""
        return self._c._get("/api/v1/plugins")

    def get(self, filename: str) -> str:
        """Fetch a compiled ESM plugin script by filename (e.g. 'rpg-observe.js')."""
        return self._c._get_raw(f"/api/v1/plugins/{filename}")
