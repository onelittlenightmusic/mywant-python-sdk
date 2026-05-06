from __future__ import annotations

from typing import TYPE_CHECKING

from ..models import Capability

if TYPE_CHECKING:
    from ..client import MyWantClient


class CapabilitiesResource:
    def __init__(self, client: "MyWantClient") -> None:
        self._c = client

    def list(self) -> list:
        return self._c._get("/api/v1/capabilities")

    def create(self, name: str, gives: list[str]) -> dict:
        return self._c._post("/api/v1/capabilities", {"name": name, "gives": gives}, expected=201)

    def get(self, name: str) -> Capability:
        return Capability.from_dict(self._c._get(f"/api/v1/capabilities/{name}"))

    def delete(self, name: str) -> None:
        self._c._delete(f"/api/v1/capabilities/{name}", expected=204)

    def find_agents(self, name: str) -> list:
        """Find all agents that provide a given capability."""
        return self._c._get(f"/api/v1/capabilities/{name}/agents")
