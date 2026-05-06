from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import MyWantClient


class WantTypesResource:
    def __init__(self, client: "MyWantClient") -> None:
        self._c = client

    def list(self) -> list:
        return self._c._get("/api/v1/want-types")

    def get(self, name: str) -> dict:
        return self._c._get(f"/api/v1/want-types/{name}")

    def get_examples(self, name: str) -> dict:
        return self._c._get(f"/api/v1/want-types/{name}/examples")
