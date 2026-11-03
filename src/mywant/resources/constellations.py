from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Optional, Union

import yaml

from ._common import csv, query, seg, yaml_text

if TYPE_CHECKING:
    from ..client import MyWantClient


class ConstellationsResource:
    """Constellations (星座) — things and wants named as one: /api/v1/constellations.

    An order is tied one after another; a hub (``capture``) is a capture into
    one tile. Schemas: want-spec's spec/constellation-spec.yaml.
    """

    def __init__(self, client: "MyWantClient") -> None:
        self._c = client

    def list(self, kind: Optional[str] = None) -> list[dict]:
        """All, or only "thing" / "want" ones."""
        path = "/api/v1/constellations" + (f"?kind={seg(kind)}" if kind else "")
        return self._c._get(path).get("groups", [])

    def get(self, name: str) -> dict:
        return self._c._get(f"/api/v1/constellations/{seg(name)}")

    def create(self, name: str, members: list[str], *, color: Optional[str] = None,
               capture: Optional[str] = None) -> dict:
        """Members are thing or want ids; ``capture`` (a member's id) makes it a hub."""
        body: dict = {"name": name, "members": members}
        if color:
            body["color"] = color
        if capture:
            body["capture"] = capture
        return self._c._post("/api/v1/constellations", body)

    def update(self, name: str, *, new_name: Optional[str] = None, members: Optional[list[str]] = None,
               color: Optional[str] = None, capture: Optional[str] = None) -> dict:
        """Change what is given; members are replaced; ``capture=""`` makes it an order."""
        body: dict = {}
        for k, v in (("name", new_name), ("members", members), ("color", color), ("capture", capture)):
            if v is not None:
                body[k] = v
        return self._c._patch(f"/api/v1/constellations/{seg(name)}", body)

    def delete(self, name: str) -> None:
        """Its members are kept."""
        self._c._delete(f"/api/v1/constellations/{seg(name)}")

    def delete_many(self, names: Iterable[str]) -> dict:
        return self._c._delete(f"/api/v1/constellations?names={csv(names)}")

    def export(self, names: Optional[Iterable[str]] = None) -> list[dict]:
        return yaml.safe_load(self._c._post_text(f"/api/v1/constellations/export{query('names', names)}")) or []

    def import_(self, data: Union[str, list]) -> list[str]:
        """Made or joined by name, with colour, art and hub. Their names."""
        return (self._c._post_yaml("/api/v1/constellations/import", yaml_text(data)) or {}).get("imported", [])
