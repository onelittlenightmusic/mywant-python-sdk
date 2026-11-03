# mywant-python-sdk

> **Moved.** This SDK now lives in the MyWant repository, as
> [`client-py`](https://github.com/onelittlenightmusic/MyWant/tree/master/client-py)
> (its code in `engine/core/pysdk/mywant`). It is the same `mywant` package,
> resource style (`Client().wants.list()`, `.things.create(...)`), standard
> library only. `MyWantClient` is now `Client`. This repository is archived.

Python SDK for the [MyWant](https://github.com/hrk-osaki/mywant) API.

## Installation

```bash
pip install mywant
```

Or from source:

```bash
git clone https://github.com/hrk-osaki/mywant-python-sdk
cd mywant-python-sdk
pip install -e .
```

## Quick start

```python
from mywant import MyWantClient

# defaults to http://localhost:8080 or $MYWANT_URL
with MyWantClient() as client:
    # health check
    h = client.system.health()
    print(h.status)          # "healthy"

    # deploy a want from a YAML string
    ex = client.wants.create("""
wants:
  - metadata:
      name: my-queue
      type: queue
    spec:
      params:
        service_time: 0.1
""")
    print(ex.id, ex.status)  # want-abc-1234  created

    # check runtime state
    state = client.wants.get(ex.id)
    print(state.execution_status)

    # stop & delete
    client.wants.stop(ex.id)
    client.wants.delete(ex.id)
```

## Resources

| Attribute | Covers |
|---|---|
| `client.wants` | CRUD + lifecycle (start/stop/suspend/resume) |
| `client.recipes` | Recipe template management |
| `client.agents` | Agent registration |
| `client.capabilities` | Capability registry |
| `client.want_types` | Want type definitions |
| `client.labels` | Label management |
| `client.plugins` | JIT-compiled card plugins |
| `client.system` | Health, config, global state, stop/restart |
| `client.utilities` | LLM query, logs, error history |
| `client.webhooks` | Webhook delivery |
| `client.reactions` | Reaction queues |

## Configuration

| Env var | Default | Description |
|---|---|---|
| `MYWANT_URL` | `http://localhost:8080` | Server base URL |

You can also pass `base_url` directly:

```python
client = MyWantClient(base_url="https://my-server:8080", timeout=60.0)
```

## Error handling

```python
from mywant.exceptions import NotFoundError, ConflictError, ValidationError

try:
    client.wants.get("nonexistent")
except NotFoundError as e:
    print(e.status_code, e.message)
```

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
