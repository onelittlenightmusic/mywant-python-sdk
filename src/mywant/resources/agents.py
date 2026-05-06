from __future__ import annotations

from typing import TYPE_CHECKING

from ..models import Agent

if TYPE_CHECKING:
    from ..client import MyWantClient


class AgentsResource:
    def __init__(self, client: "MyWantClient") -> None:
        self._c = client

    def list(self) -> list:
        return self._c._get("/api/v1/agents")

    def create(self, name: str, type: str, capabilities: list[str]) -> dict:
        return self._c._post("/api/v1/agents", {"name": name, "type": type, "capabilities": capabilities}, expected=201)

    def get(self, name: str) -> Agent:
        return Agent.from_dict(self._c._get(f"/api/v1/agents/{name}"))

    def delete(self, name: str) -> None:
        self._c._delete(f"/api/v1/agents/{name}", expected=204)

    def register_yaml(self, yaml_content: str) -> dict:
        """Hot-reload an agent from its YAML definition without a server restart."""
        return self._c._post_raw("/api/v1/agents/register-yaml", yaml_content, content_type="application/x-yaml")
