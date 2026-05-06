from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..models import HealthStatus

if TYPE_CHECKING:
    from ..client import MyWantClient


class SystemResource:
    def __init__(self, client: "MyWantClient") -> None:
        self._c = client

    def health(self) -> HealthStatus:
        d = self._c._get("/health")
        return HealthStatus(
            status=d["status"],
            wants=d["wants"],
            version=d["version"],
            server=d["server"],
        )

    def get_config(self) -> dict:
        return self._c._get("/api/v1/config")

    def update_config(self, config: dict) -> dict:
        return self._c._put("/api/v1/config", config)

    def stop(self) -> None:
        self._c._post("/api/v1/system/stop", expected=202)

    def restart(self) -> None:
        self._c._post("/api/v1/system/restart", expected=202)

    def get_global_state(self) -> dict[str, Any]:
        return self._c._get("/api/v1/global-state")

    def clear_global_state(self) -> None:
        self._c._delete("/api/v1/global-state", expected=204)

    def get_spec(self) -> str:
        """Return the OpenAPI spec as a YAML string."""
        return self._c._get_raw("/api/v1/spec")
