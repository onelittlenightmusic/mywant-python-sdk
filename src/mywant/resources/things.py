from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Optional, Union

import yaml

from ._common import csv, query, seg, yaml_text

if TYPE_CHECKING:
    from ..client import MyWantClient


class ThingsResource:
    """Things — the values you have named (a station, a city…): /api/v1/things.

    A thing is addressed by its id (``thg-…``). Schemas: want-spec's
    spec/thing-spec.yaml.
    """

    def __init__(self, client: "MyWantClient") -> None:
        self._c = client

    def list(self) -> list[dict]:
        """Every thing, whole (labels, the wants naming it, …)."""
        return self._c._get("/api/v1/things").get("things", [])

    def get(self, id: str) -> dict:
        return self._c._get(f"/api/v1/things/{seg(id)}")

    def create(self, catalog: str, value: str) -> dict:
        """Remember a value under a kind ("stations", or the subtype "station")."""
        return self._c._post("/api/v1/things", {"catalog": catalog, "value": value})

    def update(self, id: str, *, catalog: Optional[str] = None, value: Optional[str] = None) -> dict:
        """Rename it, or file it under another kind — the same thing, kept."""
        body = {k: v for k, v in (("catalog", catalog), ("value", value)) if v}
        return self._c._patch(f"/api/v1/things/{seg(id)}", body)

    def delete(self, id: str) -> None:
        self._c._delete(f"/api/v1/things/{seg(id)}")

    def delete_many(self, ids: Iterable[str]) -> dict:
        """Several at once: {deleted: [...], missing: [...]}."""
        return self._c._delete(f"/api/v1/things?ids={csv(ids)}")

    def set_label(self, id: str, key: str, value: str) -> dict:
        return self._c._post(f"/api/v1/things/{seg(id)}/labels", {"key": key, "value": value})

    def remove_label(self, id: str, key: str) -> dict:
        return self._c._delete(f"/api/v1/things/{seg(id)}/labels/{seg(key)}")

    def patch_labels(self, id: str, set: Optional[dict] = None, remove: Optional[list] = None) -> dict:
        """Set and remove several labels in one request; the labels after: {id, labels}."""
        return self._c._patch(f"/api/v1/things/{seg(id)}/labels", {"set": set or {}, "remove": remove or []})

    def export(self, ids: Optional[Iterable[str]] = None) -> list[dict]:
        """Things as written out (id, catalog, value, createdAt, labels)."""
        return yaml.safe_load(self._c._post_text(f"/api/v1/things/export{query('ids', ids)}")) or []

    def import_(self, data: Union[str, list]) -> list[str]:
        """Read things in (YAML or the list export gives): matched by kind and
        value, their labels laid on. The ids they have here."""
        return (self._c._post_yaml("/api/v1/things/import", yaml_text(data)) or {}).get("imported", [])
