from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union
import yaml

from ..models import ValidationResult, WantExecution, WantRuntimeState, WantStatus

if TYPE_CHECKING:
    from ..client import MyWantClient


class WantsResource:
    def __init__(self, client: "MyWantClient") -> None:
        self._c = client

    def create(self, config: Union[str, dict], name: Optional[str] = None) -> WantExecution:
        """Deploy a new want from YAML string or dict. Returns the created execution."""
        if isinstance(config, dict):
            yaml_str = yaml.dump(config, allow_unicode=True)
        else:
            yaml_str = config
        payload: dict[str, Any] = {"yaml": yaml_str}
        if name:
            payload["name"] = name
        return WantExecution.from_dict(self._c._post("/api/v1/wants", payload, expected=201))

    def list(self) -> list[WantExecution]:
        """List all want executions."""
        return [WantExecution.from_dict(d) for d in self._c._get("/api/v1/wants")]

    def delete_all(self) -> None:
        """Delete all want executions."""
        self._c._delete("/api/v1/wants", expected=204)

    def get(self, id: str) -> WantRuntimeState:
        """Get runtime state of a want execution."""
        return WantRuntimeState.from_dict(self._c._get(f"/api/v1/wants/{id}"))

    def update(self, id: str, config: Union[str, dict]) -> WantExecution:
        """Update an existing (non-running) want."""
        if isinstance(config, dict):
            yaml_str = yaml.dump(config, allow_unicode=True)
        else:
            yaml_str = config
        return WantExecution.from_dict(self._c._put(f"/api/v1/wants/{id}", {"yaml": yaml_str}))

    def delete(self, id: str) -> None:
        """Delete a want execution."""
        self._c._delete(f"/api/v1/wants/{id}", expected=204)

    def get_status(self, id: str) -> WantStatus:
        """Get execution status."""
        return WantStatus.from_dict(self._c._get(f"/api/v1/wants/{id}/status"))

    def get_results(self, id: str) -> dict:
        """Get execution results."""
        return self._c._get(f"/api/v1/wants/{id}/results")

    def suspend(self, id: str) -> None:
        self._c._post(f"/api/v1/wants/{id}/suspend", expected=202)

    def resume(self, id: str) -> None:
        self._c._post(f"/api/v1/wants/{id}/resume", expected=202)

    def stop(self, id: str) -> None:
        self._c._post(f"/api/v1/wants/{id}/stop", expected=202)

    def start(self, id: str) -> None:
        self._c._post(f"/api/v1/wants/{id}/start", expected=202)

    def suspend_many(self, ids: list[str]) -> None:
        self._c._post("/api/v1/wants/suspend", {"ids": ids}, expected=202)

    def resume_many(self, ids: list[str]) -> None:
        self._c._post("/api/v1/wants/resume", {"ids": ids}, expected=202)

    def stop_many(self, ids: list[str]) -> None:
        self._c._post("/api/v1/wants/stop", {"ids": ids}, expected=202)

    def start_many(self, ids: list[str]) -> None:
        self._c._post("/api/v1/wants/start", {"ids": ids}, expected=202)

    def add_label(self, id: str, key: str, value: str) -> None:
        self._c._post(f"/api/v1/wants/{id}/labels", {"key": key, "value": value}, expected=202)

    def remove_label(self, id: str, key: str) -> None:
        self._c._delete(f"/api/v1/wants/{id}/labels/{key}", expected=202)

    def update_order(self, id: str, new_order: int) -> None:
        self._c._put(f"/api/v1/wants/{id}/order", {"newOrder": new_order})

    def add_using(self, id: str, key: str, value: str) -> None:
        self._c._post(f"/api/v1/wants/{id}/using", {"key": key, "value": value}, expected=202)

    def remove_using(self, id: str, key: str) -> None:
        self._c._delete(f"/api/v1/wants/{id}/using/{key}", expected=202)

    def validate(self, config: Union[str, dict]) -> ValidationResult:
        """Validate a want configuration without deploying it."""
        if isinstance(config, dict):
            yaml_str = yaml.dump(config, allow_unicode=True)
        else:
            yaml_str = config
        return ValidationResult.from_dict(self._c._post("/api/v1/wants/validate", {"yaml": yaml_str}))

    def export(self) -> str:
        """Export all wants as a YAML string."""
        return self._c._get_raw("/api/v1/wants/export")

    def import_yaml(self, yaml_content: str) -> None:
        """Import wants from a YAML string."""
        self._c._post_yaml("/api/v1/wants/import", yaml_content, expected=201)
