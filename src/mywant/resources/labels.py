from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import MyWantClient


class LabelsResource:
    def __init__(self, client: "MyWantClient") -> None:
        self._c = client

    def list(self) -> list:
        return self._c._get("/api/v1/labels")

    def add(self, key: str, value: str) -> None:
        self._c._post("/api/v1/labels", {"key": key, "value": value}, expected=201)
