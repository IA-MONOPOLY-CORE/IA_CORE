"""Schema for the internal backend read model contract.

The schema is contract-only and read-only. It defines the shape a future
internal read model may expose without creating an implementation, store, API,
dashboard adapter, execution path or mutation surface.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any


SCHEMA_VERSION = "1.0"
CONTRACT_MODE = "internal_backend_read_model_contract_only"
ALLOWED_READ_MODEL_MODES = {
    "internal_backend_read_model_contract_only",
    "internal_backend_read_model_read_only",
    "internal_backend_snapshot",
}
ALLOWED_STATUSES = {"passed", "blocked", "failed"}
ALLOWED_VERDICTS = {
    "INTERNAL_BACKEND_READ_MODEL_CONTRACT_PASSED",
    "INTERNAL_BACKEND_READ_MODEL_CONTRACT_BLOCKED",
    "INTERNAL_BACKEND_READ_MODEL_CONTRACT_FAILED",
    "INTERNAL_BACKEND_READ_MODEL_SOURCE_MISSING",
    "INTERNAL_BACKEND_READ_MODEL_SOURCE_NOT_VERIFIED",
    "INTERNAL_BACKEND_READ_MODEL_BOUNDARY_LEAK",
    "INTERNAL_BACKEND_READ_MODEL_PAYLOAD_LEAK",
    "INTERNAL_BACKEND_READ_MODEL_MUTATION_LEAK",
}
REQUIRED_SNAPSHOT_FIELDS = {
    "snapshot_id",
    "schema_version",
    "read_model_mode",
    "generated_at",
    "target_type",
    "target_id",
    "target_ref",
    "domain_ref",
    "sandbox_summary",
    "promotion_summary",
    "active_summary",
    "runtime_contract_summary",
    "execution_contract_summary",
    "runtime_preparation_summary",
    "execution_runner_summary",
    "dry_run_summary",
    "dry_run_store_summary",
    "execution_attempt_store_summary",
    "execution_lifecycle_summary",
    "execution_history_summary",
    "audit_summary",
    "observability_summary",
    "capability_policy_summary",
    "readiness_summary",
    "blockers",
    "warnings",
    "evidence",
    "source_refs",
    "boundary_summary",
}


@dataclass(frozen=True)
class InternalBackendReadModelSourceRefs:
    domain_state_ref: dict[str, Any]
    artifact_state_ref: dict[str, Any]
    sandbox_summary_ref: dict[str, Any]
    promotion_summary_ref: dict[str, Any]
    active_summary_ref: dict[str, Any]
    runtime_contract_ref: dict[str, Any]
    execution_contract_ref: dict[str, Any]
    runtime_preparation_ref: dict[str, Any]
    execution_runner_contract_ref: dict[str, Any]
    dry_run_contract_ref: dict[str, Any]
    dry_run_ref: dict[str, Any]
    dry_run_store_ref: dict[str, Any]
    execution_attempt_store_ref: dict[str, Any]
    execution_lifecycle_ref: dict[str, Any]
    execution_history_view_ref: dict[str, Any]
    audit_refs: dict[str, Any]
    observability_refs: dict[str, Any]
    capability_policy_ref: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalBackendReadModelReadinessSummary:
    ready_for_read_model_implementation: bool
    blocked_by_missing_source: bool
    blocked_by_unverified_source: bool
    blocked_by_boundary_leak: bool
    blocked_by_payload_leak: bool
    blocked_by_contract_failure: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalBackendReadModelBoundarySummary:
    read_only: bool = True
    contract_only: bool = True
    implementation_enabled: bool = False
    store_enabled: bool = False
    api_enabled: bool = False
    dashboard_adapter_enabled: bool = False
    mutation_enabled: bool = False
    execution_enabled: bool = False
    scheduler_enabled: bool = False
    worker_enabled: bool = False
    model_invocation_enabled: bool = False
    tool_execution_enabled: bool = False
    memory_persistence_enabled: bool = False
    external_access_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalBackendReadModelEvidence:
    name: str
    passed: bool
    source: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalBackendReadModelSnapshotShape:
    snapshot_id: str
    read_model_mode: str
    target_type: str
    target_id: str
    target_ref: dict[str, Any]
    domain_ref: dict[str, Any]
    sandbox_summary: dict[str, Any]
    promotion_summary: dict[str, Any]
    active_summary: dict[str, Any]
    runtime_contract_summary: dict[str, Any]
    execution_contract_summary: dict[str, Any]
    runtime_preparation_summary: dict[str, Any]
    execution_runner_summary: dict[str, Any]
    dry_run_summary: dict[str, Any]
    dry_run_store_summary: dict[str, Any]
    execution_attempt_store_summary: dict[str, Any]
    execution_lifecycle_summary: dict[str, Any]
    execution_history_summary: dict[str, Any]
    audit_summary: dict[str, Any]
    observability_summary: dict[str, Any]
    capability_policy_summary: dict[str, Any]
    readiness_summary: dict[str, Any]
    blockers: list[Any]
    warnings: list[Any]
    evidence: list[Any]
    source_refs: dict[str, Any]
    boundary_summary: dict[str, Any]
    schema_version: str = SCHEMA_VERSION
    generated_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["generated_at"] = self.generated_at or datetime.now().isoformat()
        return payload


@dataclass(frozen=True)
class InternalBackendReadModelContractInput:
    read_model_mode: str
    target_type: str
    target_id: str
    target_ref: dict[str, Any]
    domain_ref: dict[str, Any]
    source_refs: dict[str, Any]
    source_verification: dict[str, Any]
    output_policy: dict[str, Any]
    boundary_policy: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalBackendReadModelContractResult:
    status: str
    verdict: str
    read_model_mode: str
    snapshot_shape: dict[str, Any]
    readiness_summary: dict[str, Any]
    boundary_summary: dict[str, Any]
    source_summary: dict[str, Any]
    output_summary: dict[str, Any]
    blockers: list[Any]
    warnings: list[Any]
    evidence: list[Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_internal_backend_read_model_snapshot_shape(snapshot: dict[str, Any]) -> bool:
    if not isinstance(snapshot, dict):
        return False
    if REQUIRED_SNAPSHOT_FIELDS - set(snapshot):
        return False
    if snapshot.get("schema_version") != SCHEMA_VERSION:
        return False
    if snapshot.get("read_model_mode") not in ALLOWED_READ_MODEL_MODES:
        return False
    for field in ["blockers", "warnings", "evidence"]:
        if not isinstance(snapshot.get(field), list):
            return False
    for field in REQUIRED_SNAPSHOT_FIELDS - {"blockers", "warnings", "evidence", "schema_version", "generated_at", "snapshot_id", "read_model_mode", "target_type", "target_id"}:
        if not isinstance(snapshot.get(field), dict):
            return False
    return True


def validate_internal_backend_read_model_contract_result(result: dict[str, Any]) -> bool:
    if not isinstance(result, dict):
        return False
    if result.get("status") not in ALLOWED_STATUSES:
        return False
    if result.get("verdict") not in ALLOWED_VERDICTS:
        return False
    if result.get("read_model_mode") not in ALLOWED_READ_MODEL_MODES:
        return False
    if not validate_internal_backend_read_model_snapshot_shape(result.get("snapshot_shape") or {}):
        return False
    for field in ["readiness_summary", "boundary_summary", "source_summary", "output_summary"]:
        if not isinstance(result.get(field), dict):
            return False
    for field in ["blockers", "warnings", "evidence"]:
        if not isinstance(result.get(field), list):
            return False
    return True
