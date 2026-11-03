from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ._common import seg

if TYPE_CHECKING:
    from ..client import MyWantClient


class DevicesResource:
    """Devices — the browsers and apps connected: /api/v1/devices.

    A device appears by connecting (it announces itself every thirty
    seconds), so there is no create; its settings — which one browser work is
    pinned to, which sends its location — are kept on this machine.
    """

    def __init__(self, client: "MyWantClient") -> None:
        self._c = client

    def list(self) -> list[dict]:
        """Each with whether it is home, sends its location, and its characters."""
        return self._c._get("/api/v1/devices").get("devices", [])

    def get(self, id: str) -> dict:
        return self._c._get(f"/api/v1/devices/{seg(id)}")

    def forget(self, id: str) -> None:
        """Off the list, off every character, unpinned where it was pinned."""
        self._c._delete(f"/api/v1/devices/{seg(id)}")

    def settings(self) -> dict:
        return self._c._get("/api/v1/devices/settings")

    def update_settings(self, *, home_browser_device: Optional[str] = None,
                        active_location_device: Optional[str] = None,
                        location_want_id: Optional[str] = None) -> dict:
        """Any of them; "" unsets."""
        body = {}
        for k, v in (("homeBrowserDevice", home_browser_device),
                     ("activeLocationDevice", active_location_device),
                     ("locationWantId", location_want_id)):
            if v is not None:
                body[k] = v
        return self._c._put("/api/v1/devices/settings", body)
