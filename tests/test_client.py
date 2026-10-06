"""Basic unit tests using pytest-httpx to mock HTTP calls."""

import pytest
import httpx

from mywant import MyWantClient
from mywant.exceptions import NotFoundError


@pytest.fixture
def client():
    c = MyWantClient(base_url="http://test")
    yield c
    c.close()


def test_health(client, httpx_mock):
    httpx_mock.add_response(
        url="http://test/health",
        json={"status": "healthy", "wants": 2, "version": "1.0.0", "server": "mywant"},
    )
    h = client.system.health()
    assert h.status == "healthy"
    assert h.wants == 2


def test_list_wants_empty(client, httpx_mock):
    httpx_mock.add_response(url="http://test/api/v1/wants", json=[])
    wants = client.wants.list()
    assert wants == []


def test_create_want(client, httpx_mock):
    httpx_mock.add_response(
        url="http://test/api/v1/wants",
        status_code=201,
        json={"id": "want-abc-1234", "status": "created", "want_ids": ["want-abc-1234"], "wants": 1},
    )
    result = client.wants.create("wants:\n  - metadata:\n      name: test\n      type: queue\n    spec:\n      params: {}\n")
    assert result["id"] == "want-abc-1234"
    assert result["status"] == "created"


def test_not_found_raises(client, httpx_mock):
    httpx_mock.add_response(
        url="http://test/api/v1/wants/missing",
        status_code=404,
        json={"error": "Want not found"},
    )
    with pytest.raises(NotFoundError) as exc_info:
        client.wants.get("missing")
    assert exc_info.value.status_code == 404


def test_validate_want(client, httpx_mock):
    httpx_mock.add_response(
        url="http://test/api/v1/wants/validate",
        json={"valid": True, "fatalErrors": [], "warnings": [], "wantCount": 1},
    )
    result = client.wants.validate("wants:\n  - metadata:\n      name: t\n      type: queue\n    spec:\n      params: {}\n")
    assert result.valid is True
    assert result.want_count == 1


def test_patch_want(client, httpx_mock):
    httpx_mock.add_response(
        url="http://test/api/v1/wants/want-1",
        method="PATCH",
        json={"metadata": {"id": "want-1", "labels": {}}},
    )
    client.wants.patch("want-1", labels={"mywant.io/archived": None}, params={"to": "銀座"})
    sent = httpx_mock.get_request()
    import json
    assert sent.method == "PATCH"
    assert json.loads(sent.content) == {
        "metadata": {"labels": {"mywant.io/archived": None}},
        "spec": {"params": {"to": "銀座"}},
    }
