"""MyWant Python SDK — synchronous HTTP client."""

from __future__ import annotations

import os
from typing import Any, Optional

import httpx

from .exceptions import APIError, ConflictError, NotFoundError, ValidationError
from .resources.agents import AgentsResource
from .resources.capabilities import CapabilitiesResource
from .resources.labels import LabelsResource
from .resources.plugins import PluginsResource
from .resources.recipes import RecipesResource
from .resources.system import SystemResource
from .resources.utilities import ReactionsResource, UtilitiesResource, WebhooksResource
from .resources.want_types import WantTypesResource
from .resources.wants import WantsResource


class MyWantClient:
    """Synchronous client for the MyWant API.

    Args:
        base_url: Server base URL. Defaults to ``MYWANT_URL`` env var or ``http://localhost:8080``.
        timeout: Request timeout in seconds (default 30).
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        self.base_url = (base_url or os.environ.get("MYWANT_URL") or "http://localhost:8080").rstrip("/")
        self._http = httpx.Client(timeout=timeout)

        self.wants = WantsResource(self)
        self.recipes = RecipesResource(self)
        self.agents = AgentsResource(self)
        self.capabilities = CapabilitiesResource(self)
        self.want_types = WantTypesResource(self)
        self.labels = LabelsResource(self)
        self.plugins = PluginsResource(self)
        self.system = SystemResource(self)
        self.utilities = UtilitiesResource(self)
        self.webhooks = WebhooksResource(self)
        self.reactions = ReactionsResource(self)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "MyWantClient":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    # ── internal helpers ──────────────────────────────────────────────────────

    def _raise_for(self, resp: httpx.Response) -> None:
        if resp.status_code < 400:
            return
        try:
            msg = resp.json().get("error", resp.text)
        except Exception:
            msg = resp.text
        cls = {404: NotFoundError, 409: ConflictError, 400: ValidationError}.get(resp.status_code, APIError)
        raise cls(resp.status_code, msg)

    def _get(self, path: str) -> Any:
        resp = self._http.get(self.base_url + path)
        self._raise_for(resp)
        return resp.json()

    def _get_raw(self, path: str) -> str:
        resp = self._http.get(self.base_url + path)
        self._raise_for(resp)
        return resp.text

    def _post(self, path: str, payload: Any = None, *, expected: int = 200) -> Any:
        resp = self._http.post(self.base_url + path, json=payload)
        self._raise_for(resp)
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    def _post_yaml(self, path: str, yaml_content: str, *, expected: int = 200) -> Any:
        resp = self._http.post(
            self.base_url + path,
            content=yaml_content.encode(),
            headers={"Content-Type": "application/yaml"},
        )
        self._raise_for(resp)
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    def _post_raw(self, path: str, content: str, *, content_type: str = "text/plain") -> Any:
        resp = self._http.post(
            self.base_url + path,
            content=content.encode(),
            headers={"Content-Type": content_type},
        )
        self._raise_for(resp)
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    def _put(self, path: str, payload: Any) -> Any:
        resp = self._http.put(self.base_url + path, json=payload)
        self._raise_for(resp)
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    def _put_yaml(self, path: str, yaml_content: str) -> Any:
        resp = self._http.put(
            self.base_url + path,
            content=yaml_content.encode(),
            headers={"Content-Type": "application/yaml"},
        )
        self._raise_for(resp)
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    def _delete(self, path: str, *, expected: int = 200) -> Any:
        resp = self._http.delete(self.base_url + path)
        self._raise_for(resp)
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()
