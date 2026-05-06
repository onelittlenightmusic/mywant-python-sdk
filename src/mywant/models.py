"""Lightweight dataclass models mirroring the OpenAPI schemas."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class HealthStatus:
    status: str
    wants: int
    version: str
    server: str


@dataclass
class OwnerReference:
    api_version: str
    kind: str
    name: str
    id: Optional[str] = None
    controller: bool = False
    block_owner_deletion: bool = False

    @classmethod
    def from_dict(cls, d: dict) -> "OwnerReference":
        return cls(
            api_version=d.get("apiVersion", ""),
            kind=d.get("kind", ""),
            name=d.get("name", ""),
            id=d.get("id"),
            controller=d.get("controller", False),
            block_owner_deletion=d.get("blockOwnerDeletion", False),
        )


@dataclass
class Metadata:
    name: str
    type: str
    labels: dict[str, str] = field(default_factory=dict)
    owner_references: list[OwnerReference] = field(default_factory=list)
    is_system_want: bool = False

    @classmethod
    def from_dict(cls, d: dict) -> "Metadata":
        return cls(
            name=d["name"],
            type=d["type"],
            labels=d.get("labels") or {},
            owner_references=[OwnerReference.from_dict(r) for r in (d.get("ownerReferences") or [])],
            is_system_want=d.get("isSystemWant", False),
        )


@dataclass
class WantSpec:
    params: dict[str, Any] = field(default_factory=dict)
    using: list[dict[str, str]] = field(default_factory=list)
    state_subscriptions: list[dict] = field(default_factory=list)
    notification_filters: list[dict] = field(default_factory=list)
    when: list[dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> "WantSpec":
        return cls(
            params=d.get("params") or {},
            using=d.get("using") or [],
            state_subscriptions=d.get("stateSubscriptions") or [],
            notification_filters=d.get("notificationFilters") or [],
            when=d.get("when") or [],
        )


@dataclass
class AgentExecution:
    agent_name: str
    agent_type: str
    start_time: str
    status: str
    end_time: Optional[str] = None
    error: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "AgentExecution":
        return cls(
            agent_name=d["agent_name"],
            agent_type=d["agent_type"],
            start_time=d["start_time"],
            status=d["status"],
            end_time=d.get("end_time"),
            error=d.get("error"),
        )


@dataclass
class Want:
    metadata: Metadata
    spec: WantSpec
    status: Optional[str] = None
    state: dict[str, Any] = field(default_factory=dict)
    history: dict[str, Any] = field(default_factory=dict)
    current_agent: Optional[str] = None
    running_agents: list[str] = field(default_factory=list)
    agent_history: list[AgentExecution] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> "Want":
        return cls(
            metadata=Metadata.from_dict(d["metadata"]),
            spec=WantSpec.from_dict(d.get("spec") or {}),
            status=d.get("status"),
            state=d.get("state") or {},
            history=d.get("history") or {},
            current_agent=d.get("current_agent"),
            running_agents=d.get("running_agents") or [],
            agent_history=[AgentExecution.from_dict(a) for a in (d.get("agent_history") or [])],
        )


@dataclass
class WantExecution:
    id: str
    status: str
    config: dict[str, Any]
    results: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> "WantExecution":
        return cls(
            id=d["id"],
            status=d["status"],
            config=d.get("config") or {},
            results=d.get("results") or {},
        )


@dataclass
class WantRuntimeState:
    id: str
    execution_status: str
    wants: dict[str, Want]
    results: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> "WantRuntimeState":
        return cls(
            id=d["id"],
            execution_status=d["execution_status"],
            wants={k: Want.from_dict(v) for k, v in (d.get("wants") or {}).items()},
            results=d.get("results") or {},
        )


@dataclass
class WantStatus:
    id: str
    status: str

    @classmethod
    def from_dict(cls, d: dict) -> "WantStatus":
        return cls(id=d["id"], status=d["status"])


@dataclass
class ValidationResult:
    valid: bool
    fatal_errors: list[dict] = field(default_factory=list)
    warnings: list[dict] = field(default_factory=list)
    want_count: int = 0
    validated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "ValidationResult":
        return cls(
            valid=d.get("valid", False),
            fatal_errors=d.get("fatalErrors") or [],
            warnings=d.get("warnings") or [],
            want_count=d.get("wantCount", 0),
            validated_at=d.get("validatedAt"),
        )


@dataclass
class Agent:
    name: str
    type: str
    capabilities: list[str]

    @classmethod
    def from_dict(cls, d: dict) -> "Agent":
        return cls(name=d["name"], type=d["type"], capabilities=d.get("capabilities") or [])


@dataclass
class Capability:
    name: str
    gives: list[str]

    @classmethod
    def from_dict(cls, d: dict) -> "Capability":
        return cls(name=d["name"], gives=d.get("gives") or [])
