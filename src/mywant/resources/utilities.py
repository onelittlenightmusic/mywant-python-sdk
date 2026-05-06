from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import MyWantClient


class UtilitiesResource:
    def __init__(self, client: "MyWantClient") -> None:
        self._c = client

    def query_llm(self, message: str, model: Optional[str] = None) -> dict:
        payload = {"message": message}
        if model:
            payload["model"] = model
        return self._c._post("/api/v1/llm/query", payload)

    def get_logs(self) -> str:
        return self._c._get_raw("/api/v1/logs")

    def clear_logs(self) -> None:
        self._c._delete("/api/v1/logs", expected=204)

    def list_errors(self) -> list:
        return self._c._get("/api/v1/errors")

    def get_error(self, id: str) -> dict:
        return self._c._get(f"/api/v1/errors/{id}")

    def update_error(self, id: str) -> dict:
        return self._c._put(f"/api/v1/errors/{id}", {})

    def delete_error(self, id: str) -> None:
        self._c._delete(f"/api/v1/errors/{id}", expected=204)


class WebhooksResource:
    def __init__(self, client: "MyWantClient") -> None:
        self._c = client

    def list(self) -> list:
        return self._c._get("/api/v1/webhooks")

    def send(self, id: str, payload: dict) -> None:
        """Deliver a webhook payload to a registered endpoint."""
        self._c._post(f"/api/v1/webhooks/{id}", payload)


class ReactionsResource:
    def __init__(self, client: "MyWantClient") -> None:
        self._c = client

    def list(self) -> list:
        return self._c._get("/api/v1/reactions/")

    def create(self) -> dict:
        return self._c._post("/api/v1/reactions/", expected=201)

    def get(self, id: str) -> dict:
        return self._c._get(f"/api/v1/reactions/{id}")

    def add(self, id: str) -> dict:
        return self._c._put(f"/api/v1/reactions/{id}", {})

    def delete(self, id: str) -> None:
        self._c._delete(f"/api/v1/reactions/{id}", expected=204)
