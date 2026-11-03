"""Things, constellations, characters, devices and character skills."""

import json

import pytest

from mywant import MyWantClient


@pytest.fixture
def client():
    c = MyWantClient(base_url="http://test")
    yield c
    c.close()


def test_things_crud(client, httpx_mock):
    httpx_mock.add_response(method="POST", url="http://test/api/v1/things", json={"id": "thg-1", "catalog": "stations", "value": "渋谷"})
    httpx_mock.add_response(method="GET", url="http://test/api/v1/things/thg-1", json={"id": "thg-1", "value": "渋谷"})
    httpx_mock.add_response(method="PATCH", url="http://test/api/v1/things/thg-1/labels", json={"id": "thg-1", "labels": {"a": "1"}})
    httpx_mock.add_response(method="DELETE", url="http://test/api/v1/things?ids=thg-1,thg-2", json={"deleted": ["thg-1"], "missing": ["thg-2"]})
    assert client.things.create("stations", "渋谷")["id"] == "thg-1"
    assert client.things.get("thg-1")["value"] == "渋谷"
    assert client.things.patch_labels("thg-1", {"a": "1"}, ["b"])["labels"] == {"a": "1"}
    sent = json.loads(httpx_mock.get_requests(method="PATCH")[0].content)
    assert sent == {"set": {"a": "1"}, "remove": ["b"]}
    assert client.things.delete_many(["thg-1", "thg-2"])["missing"] == ["thg-2"]


def test_things_export_import(client, httpx_mock):
    httpx_mock.add_response(method="POST", url="http://test/api/v1/things/export?ids=thg-1", text="- id: thg-1\n  catalog: notes\n  value: x\n")
    httpx_mock.add_response(method="POST", url="http://test/api/v1/things/import", json={"imported": ["thg-1"]})
    exported = client.things.export(["thg-1"])
    assert exported == [{"id": "thg-1", "catalog": "notes", "value": "x"}]
    assert client.things.import_(exported) == ["thg-1"]
    assert httpx_mock.get_requests(method="POST")[-1].headers["content-type"] == "application/yaml"


def test_constellations_by_name(client, httpx_mock):
    # A name with Japanese is one escaped path segment.
    httpx_mock.add_response(method="GET", url="http://test/api/v1/constellations/%E4%B8%AD%E5%A4%AE%E7%B7%9A", json={"name": "中央線", "members": ["thg-1"]})
    httpx_mock.add_response(method="PATCH", url="http://test/api/v1/constellations/%E4%B8%AD%E5%A4%AE%E7%B7%9A", json={"name": "中央線"})
    assert client.constellations.get("中央線")["members"] == ["thg-1"]
    client.constellations.update("中央線", color="#ff0000", capture="")
    assert json.loads(httpx_mock.get_requests(method="PATCH")[0].content) == {"color": "#ff0000", "capture": ""}


def test_devices_and_skills(client, httpx_mock):
    httpx_mock.add_response(method="GET", url="http://test/api/v1/devices", json={"devices": [{"id": "d1", "home": True}], "settings": {}})
    httpx_mock.add_response(method="PUT", url="http://test/api/v1/devices/settings", json={"homeBrowserDevice": ""})
    httpx_mock.add_response(method="GET", url="http://test/api/v1/character-skills", json={"skills": [{"metadata": {"name": "throw"}}]})
    assert client.devices.list()[0]["home"] is True
    client.devices.update_settings(home_browser_device="")
    assert json.loads(httpx_mock.get_requests(method="PUT")[0].content) == {"homeBrowserDevice": ""}
    assert client.character_skills.list()[0]["metadata"]["name"] == "throw"
