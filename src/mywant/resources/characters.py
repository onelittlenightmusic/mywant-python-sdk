from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Optional, Union

import yaml

from ._common import csv, query, seg, yaml_text

if TYPE_CHECKING:
    from ..client import MyWantClient


class CharactersResource:
    """Characters — who moves on the board: /api/v1/characters."""

    def __init__(self, client: "MyWantClient") -> None:
        self._c = client

    def list(self) -> list[dict]:
        resp = self._c._get("/api/v1/characters")
        return resp.get("characters", resp) if isinstance(resp, dict) else resp

    def get(self, id: str) -> dict:
        return self._c._get(f"/api/v1/characters/{seg(id)}")

    def create(self, name: str, *, avatar: str = "", color: str = "", shape: str = "") -> dict:
        body = {"name": name, "avatar": avatar, "color": color}
        if shape:
            body["shape"] = shape
        return self._c._post("/api/v1/characters", body)

    def update(self, id: str, **fields) -> dict:
        """Who they are: name, avatar, color, shape (their display and labels have their own calls)."""
        return self._c._put(f"/api/v1/characters/{seg(id)}", fields)

    def delete(self, id: str) -> None:
        self._c._delete(f"/api/v1/characters/{seg(id)}")

    def delete_many(self, ids: Iterable[str]) -> dict:
        return self._c._delete(f"/api/v1/characters?ids={csv(ids)}")

    def set_label(self, id: str, key: str, value: str) -> dict:
        return self._c._post(f"/api/v1/characters/{seg(id)}/labels", {"key": key, "value": value})

    def remove_label(self, id: str, key: str) -> dict:
        return self._c._delete(f"/api/v1/characters/{seg(id)}/labels/{seg(key)}")

    def export(self, ids: Optional[Iterable[str]] = None) -> list[dict]:
        return yaml.safe_load(self._c._post_text(f"/api/v1/characters/export{query('ids', ids)}")) or []

    def import_(self, data: Union[str, list]) -> list[str]:
        """One of an id already here is updated; any other is added. Their ids."""
        return (self._c._post_yaml("/api/v1/characters/import", yaml_text(data)) or {}).get("imported", [])
