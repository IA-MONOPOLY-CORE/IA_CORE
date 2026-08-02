"""Contract-only Runtime Execution Preparation Projection.

This module derives safe, filtered, JSON-serializable projection shapes from
the Runtime Execution Preparation Read Model and Package contracts. It is
read-only and non-operational: it never stores, writes, executes, invokes
tools/models, opens external capabilities, exposes APIs/UI, or replaces the
permission and Security Layer contracts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
import json
from typing import Any, Mapping

from core import runtime_execution_preparation_contract as parent_contract
from core import runtime_execution_preparation_package as package_contract
from core import runtime_execution_preparation_read_model as read_model_contract


RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTRACT_READY = True
RUNTIME_EXECUTION_PREPARATION_PROJECTION_OPERATIONAL = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_RUNTIME_ACTIVE = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_EXECUTION_ACTIVE = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_DRY_RUN_ACTIVE = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_TOOLS_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_MODELS_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTEXT_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_OUTPUT_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_WRITES_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_STORES_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_MEMORY_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_NETWORK_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_BROWSER_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_FILESYSTEM_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_ENV_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_SECRETS_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_API_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_UI_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_UI_DEVICE_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PROJECTION_INTEGRATIONS_ENABLED = False

CONTRACT_STATUS = "RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTRACT_READY"
CONTRACT_VERDICT = "RUNTIME_EXECUTION_PREPARATION_PROJECTION_NO_OPERATIONAL_CONFIRMED"
CONTRACT_READINESS = "ready_for_runtime_execution_preparation_projection_contract_e2e"
CONTRACT_NEXT_STEP = "PROMPT 4.7.1 - Checkpoint E2E Runtime Execution Preparation Projection Contract"
PARENT_READ_MODEL_CONTRACT_REF = "core.runtime_execution_preparation_read_model"
PARENT_PACKAGE_CONTRACT_REF = "core.runtime_execution_preparation_package"
PARENT_PREPARATION_CONTRACT_REF = "core.runtime_execution_preparation_contract"
EXCLUDED_EXTERNAL_CONCEPTS = frozenset({"OBLITERATUS"})
OBLITERATUS_EXCLUSION_STATEMENTS = (
    "OBLITERATUS is excluded from Runtime Execution Preparation Projection.",
    "OBLITERATUS is not an integration.",
    "OBLITERATUS is not a dependency.",
    "OBLITERATUS is not an adapter.",
    "OBLITERATUS is not a provider.",
    "OBLITERATUS is not a capability.",
    "OBLITERATUS is not a runtime.",
    "OBLITERATUS is not an execution source.",
    "OBLITERATUS is not a package source.",
    "OBLITERATUS is not a read model source.",
    "OBLITERATUS is not a projection source.",
    "OBLITERATUS is not a projection metadata source.",
    "OBLITERATUS is not a projection view source.",
    "OBLITERATUS is not an audit source.",
)


class RuntimeExecutionPreparationProjectionStatus(str, Enum):
    PROJECTION_UNINITIALIZED = "projection_uninitialized"
    PROJECTION_DRAFT = "projection_draft"
    PROJECTION_SOURCE_REQUIRED = "projection_source_required"
    PROJECTION_READ_MODEL_REQUIRED = "projection_read_model_required"
    PROJECTION_PACKAGE_REQUIRED = "projection_package_required"
    PROJECTION_VISIBILITY_REQUIRED = "projection_visibility_required"
    PROJECTION_FILTERING_REQUIRED = "projection_filtering_required"
    PROJECTION_READY_SIMULATED = "projection_ready_simulated"
    PROJECTION_BLOCKED = "projection_blocked"
    PROJECTION_INVALID = "projection_invalid"
    PROJECTION_ARCHIVED_SIMULATED = "projection_archived_simulated"


class RuntimeExecutionPreparationProjectionReadiness(str, Enum):
    READY_FOR_RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTRACT = (
        "ready_for_runtime_execution_preparation_projection_contract"
    )
    READY_FOR_RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTRACT_E2E = (
        "ready_for_runtime_execution_preparation_projection_contract_e2e"
    )


class RuntimeExecutionPreparationProjectionKind(str, Enum):
    MASTER_PANEL_PROJECTION = "master_panel_projection"
    USER_PANEL_PROJECTION = "user_panel_projection"
    INTERNAL_AUDIT_PROJECTION = "internal_audit_projection"
    SUMMARY_PROJECTION = "summary_projection"
    STATUS_ONLY_PROJECTION = "status_only_projection"
    BLOCKED_PROJECTION = "blocked_projection"


class RuntimeExecutionPreparationProjectionVisibility(str, Enum):
    MASTER_PANEL = "master_panel"
    USER_PANEL = "user_panel"
    INTERNAL_AUDIT = "internal_audit"
    SUMMARY_ONLY = "summary_only"
    STATUS_ONLY = "status_only"
    INTERNAL_ONLY = "internal_only"
    BLOCKED = "blocked"


class RuntimeExecutionPreparationProjectionDecision(str, Enum):
    ALLOW_READ_ONLY_PROJECTION = "allow_read_only_projection"
    BLOCK_PROJECTION = "block_projection"
    REQUIRE_SOURCE_REFS = "require_source_refs"
    REQUIRE_READ_MODEL_FILTER = "require_read_model_filter"
    REQUIRE_METADATA_SANITIZATION = "require_metadata_sanitization"
    REQUIRE_POLICY_DEFAULT_DENY = "require_policy_default_deny"
    REQUIRE_VISIBILITY_FILTERING = "require_visibility_filtering"
    INVALID = "invalid"


class RuntimeExecutionPreparationProjectionCapability(str, Enum):
    RUNTIME_EXECUTION = "runtime_execution"
    RUNTIME_ACTIVATION = "runtime_activation"
    DRY_RUN_EXECUTION = "dry_run_execution"
    RUNNER = "runner"
    SCHEDULER = "scheduler"
    WORKER = "worker"
    QUEUE = "queue"
    EXECUTOR = "executor"
    ORCHESTRATOR = "orchestrator"
    DISPATCHER = "dispatcher"
    EVENT_BUS = "event_bus"
    TOOL_EXECUTION = "tool_execution"
    MODEL_INVOCATION = "model_invocation"
    CONTEXT_INJECTION = "context_injection"
    OUTPUT_DELIVERY = "output_delivery"
    WRITES = "writes"
    STORES = "stores"
    MEMORY = "memory"
    NETWORK = "network"
    API = "api"
    BROWSER = "browser"
    FILESYSTEM = "filesystem"
    ENV = "env"
    SECRETS = "secrets"
    UI = "ui"
    UI_CONTROL = "ui_control"
    DEVICE_CONTROL = "device_control"
    INTEGRATIONS = "integrations"
    MARKET_CATALOG_RUNTIME = "market_catalog_runtime"
    BUSINESS_COMPOSITION_RUNTIME = "business_composition_runtime"
    OBLITERATUS_INTEGRATION = "obliteratus_integration"
    MASTER_PANEL_INTERNAL_CAPABILITY_EXPOSURE = "master_panel_internal_capability_exposure"
    USER_PANEL_RAW_INTERNAL_EXPOSURE = "user_panel_raw_internal_exposure"
    PERMISSION_BYPASS = "permission_bypass"
    RAW_PACKAGE_TO_USER_PROJECTION = "raw_package_to_user_projection"


class RuntimeExecutionPreparationProjectionRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


ALLOWED_STATUSES = tuple(status.value for status in RuntimeExecutionPreparationProjectionStatus)
FORBIDDEN_STATUSES = (
    "projection_active",
    "projection_running",
    "projection_executing",
    "projection_live",
    "projection_enabled",
    "projection_operational",
    "projection_runtime_started",
    "projection_execution_started",
    "projection_dry_run_started",
    "projection_tool_executing",
    "projection_model_invoking",
    "projection_context_injecting",
    "projection_output_delivering",
    "projection_writing",
    "projection_store_mutating",
    "projection_network_active",
    "projection_browser_active",
    "projection_filesystem_active",
    "projection_env_active",
    "projection_secret_active",
    "projection_integration_active",
    "projection_api_active",
    "projection_ui_control_active",
)
ALLOWED_READINESS = tuple(readiness.value for readiness in RuntimeExecutionPreparationProjectionReadiness)
FORBIDDEN_READINESS = (
    "ready_for_runtime",
    "ready_for_runtime_activation",
    "ready_for_execution",
    "ready_for_dry_run_execution",
    "ready_for_tool_execution",
    "ready_for_model_invocation",
    "ready_for_context_injection",
    "ready_for_output_delivery",
    "ready_for_writes",
    "ready_for_stores",
    "ready_for_api",
    "ready_for_ui",
    "runtime_open",
    "runtime_active",
    "runtime_enabled",
    "execution_enabled",
    "operations_enabled",
    "projection_operational",
    "projection_store_enabled",
    "projection_writer_enabled",
    "projection_api_enabled",
    "projection_ui_enabled",
)
PROJECTION_KINDS = tuple(kind.value for kind in RuntimeExecutionPreparationProjectionKind)
BLOCKED_CAPABILITIES = tuple(capability.value for capability in RuntimeExecutionPreparationProjectionCapability)
SAFE_METADATA_KEYS = (
    "projection_reason",
    "projection_scope",
    "projection_kind",
    "created_by",
    "source",
    "tags",
    "notes",
    "read_model_ref",
    "package_ref",
    "contract_ref",
    "visibility",
)
FORBIDDEN_METADATA_KEYS = tuple(
    dict.fromkeys(
        (
            *read_model_contract.FORBIDDEN_METADATA_KEYS,
            "raw_master_panel_view",
            "raw_user_panel_view",
            "raw_internal_audit_view",
        )
    )
)
REQUIRED_SOURCE_REF_FIELDS = (
    "projection_id",
    "read_model_id",
    "package_id",
    "preparation_id",
    "intent_ref",
    "source_read_model_ref",
    "source_package_ref",
    "parent_read_model_contract_ref",
    "parent_package_contract_ref",
    "parent_preparation_contract_ref",
)
FORBIDDEN_PROJECTION_FRAGMENTS = (
    "raw_payload",
    "raw_prompt",
    "raw_output",
    "model_response",
    "tool_response",
    "api_key",
    "admin_secret",
    "authorization",
    "bearer",
    "token",
    "cookie",
    "personal_data_unsanitized",
    "raw_package_contract",
    "raw_read_model_contract",
)
USER_PROJECTION_FORBIDDEN_FRAGMENTS = (
    *FORBIDDEN_PROJECTION_FRAGMENTS,
    "technical_refs",
    "technical_ref",
    "metadata",
    "master_panel",
    "admin",
    "security_internal",
    "permission_internal",
    "intent_internal",
    "attempt_internal",
    "raw_package",
    "raw_read_model",
)


@dataclass(frozen=True)
class RuntimeExecutionPreparationProjectionPolicy:
    contract_ready: bool = True
    read_only_enabled: bool = True
    projection_operational_enabled: bool = False
    runtime_activation_enabled: bool = False
    runtime_execution_enabled: bool = False
    dry_run_execution_enabled: bool = False
    tool_execution_enabled: bool = False
    model_invocation_enabled: bool = False
    context_injection_enabled: bool = False
    output_delivery_enabled: bool = False
    writes_enabled: bool = False
    stores_enabled: bool = False
    memory_enabled: bool = False
    network_enabled: bool = False
    browser_enabled: bool = False
    filesystem_enabled: bool = False
    env_enabled: bool = False
    secrets_enabled: bool = False
    api_enabled: bool = False
    ui_enabled: bool = False
    ui_device_enabled: bool = False
    integrations_enabled: bool = False
    master_panel_internal_exposure_enabled: bool = False
    user_panel_raw_internal_exposure_enabled: bool = False
    permission_bypass_enabled: bool = False
    raw_package_to_user_projection_enabled: bool = False


@dataclass(frozen=True)
class RuntimeExecutionPreparationProjectionMetadata:
    projection_reason: str = ""
    projection_scope: str = ""
    projection_kind: str = ""
    created_by: str = ""
    source: str = ""
    tags: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    read_model_ref: str = ""
    package_ref: str = ""
    contract_ref: str = ""
    visibility: str = ""
    blocked_keys: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuntimeExecutionPreparationProjectionSourceRef:
    projection_id: str
    read_model_id: str
    package_id: str
    preparation_id: str
    intent_ref: str
    attempt_ref: str | None
    source_read_model_ref: str
    source_package_ref: str
    source_contract_refs: tuple[str, ...]
    parent_read_model_contract_ref: str
    parent_package_contract_ref: str
    parent_preparation_contract_ref: str
    serialization_version: str

    def missing_critical_source_refs(self) -> tuple[str, ...]:
        return tuple(
            field for field in REQUIRED_SOURCE_REF_FIELDS if not str(getattr(self, field, "") or "").strip()
        )


@dataclass(frozen=True)
class RuntimeExecutionPreparationProjectionCore:
    projection_id: str
    read_model_id: str
    package_id: str
    preparation_id: str
    intent_ref: str
    attempt_ref: str | None
    projection_kind: RuntimeExecutionPreparationProjectionKind | str
    projection_status: RuntimeExecutionPreparationProjectionStatus | str
    projection_readiness: RuntimeExecutionPreparationProjectionReadiness | str
    visibility: RuntimeExecutionPreparationProjectionVisibility | str
    risk_level: RuntimeExecutionPreparationProjectionRiskLevel | str
    execution_scope: str
    execution_mode: str
    decision: RuntimeExecutionPreparationProjectionDecision | str
    validation_status: str
    dependency_summary: str
    boundary_summary: str
    blocked_capabilities_summary: str
    warning_summary: str
    error_summary: str
    safe_summary: str
    source_read_model_ref: str
    source_package_ref: str
    source_contract_refs: tuple[str, ...]
    parent_read_model_contract_ref: str
    parent_package_contract_ref: str
    parent_preparation_contract_ref: str
    serialization_version: str
    metadata: RuntimeExecutionPreparationProjectionMetadata


@dataclass(frozen=True)
class RuntimeExecutionPreparationMasterPanelProjection:
    projection_id: str
    read_model_id: str
    package_id: str
    preparation_id: str
    intent_ref: str
    attempt_ref: str | None
    status: str
    readiness: str
    risk_level: str
    execution_scope: str
    execution_mode: str
    decision: str
    validation_status: str
    dependency_summary: str
    boundary_summary: str
    blocked_capabilities_summary: str
    warning_summary: str
    error_summary: str
    safe_summary: str
    technical_refs: tuple[str, ...]
    visibility: RuntimeExecutionPreparationProjectionVisibility


@dataclass(frozen=True)
class RuntimeExecutionPreparationUserPanelProjection:
    projection_id: str
    package_id: str
    status: str
    readiness: str
    risk_level: str
    safe_summary: str
    dependency_summary: str
    blocked_capabilities_summary: str
    warning_summary: str
    visibility: RuntimeExecutionPreparationProjectionVisibility


@dataclass(frozen=True)
class RuntimeExecutionPreparationInternalAuditProjection:
    projection_id: str
    read_model_id: str
    package_id: str
    preparation_id: str
    intent_ref: str
    attempt_ref: str | None
    status: str
    readiness: str
    risk_level: str
    decision: str
    validation_status: str
    sanitized_refs: tuple[str, ...]
    blocked_keys: tuple[str, ...]
    blocked_capabilities_summary: str
    warning_summary: str
    error_summary: str
    visibility: RuntimeExecutionPreparationProjectionVisibility


@dataclass(frozen=True)
class RuntimeExecutionPreparationSummaryProjection:
    projection_id: str
    package_id: str
    status: str
    readiness: str
    risk_level: str
    safe_summary: str
    visibility: RuntimeExecutionPreparationProjectionVisibility


@dataclass(frozen=True)
class RuntimeExecutionPreparationStatusOnlyProjection:
    projection_id: str
    package_id: str
    status: str
    readiness: str
    risk_level: str
    visibility: RuntimeExecutionPreparationProjectionVisibility


@dataclass(frozen=True)
class RuntimeExecutionPreparationBlockedProjection:
    projection_id: str
    package_id: str
    status: str
    readiness: str
    risk_level: str
    safe_summary: str
    blocked_reason: str
    visibility: RuntimeExecutionPreparationProjectionVisibility


@dataclass(frozen=True)
class RuntimeExecutionPreparationProjectionValidationResult:
    is_valid: bool
    status: RuntimeExecutionPreparationProjectionStatus
    readiness: RuntimeExecutionPreparationProjectionReadiness | str
    missing_source_refs: tuple[str, ...]
    forbidden_readiness_detected: tuple[str, ...]
    forbidden_status_detected: tuple[str, ...]
    metadata_blocked_keys: tuple[str, ...]
    policy_violations: tuple[str, ...]
    visibility_violations: tuple[str, ...]
    projection_violations: tuple[str, ...]
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeExecutionPreparationProjectionDecisionRecord:
    decision: RuntimeExecutionPreparationProjectionDecision
    allowed: bool
    read_only_projection_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    dry_run_execution_allowed: bool
    tool_execution_allowed: bool
    model_invocation_allowed: bool
    context_injection_allowed: bool
    output_delivery_allowed: bool
    writes_allowed: bool
    stores_allowed: bool
    memory_allowed: bool
    network_allowed: bool
    browser_allowed: bool
    filesystem_allowed: bool
    env_allowed: bool
    secrets_allowed: bool
    api_allowed: bool
    ui_allowed: bool
    permission_bypass_allowed: bool
    raw_package_to_user_projection_allowed: bool
    reason: str
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeExecutionPreparationProjectionSnapshot:
    projection: RuntimeExecutionPreparationProjectionCore
    master_panel_projection: RuntimeExecutionPreparationMasterPanelProjection
    user_panel_projection: RuntimeExecutionPreparationUserPanelProjection
    internal_audit_projection: RuntimeExecutionPreparationInternalAuditProjection
    summary_projection: RuntimeExecutionPreparationSummaryProjection
    status_only_projection: RuntimeExecutionPreparationStatusOnlyProjection
    blocked_projection: RuntimeExecutionPreparationBlockedProjection
    validation: RuntimeExecutionPreparationProjectionValidationResult
    decision: RuntimeExecutionPreparationProjectionDecisionRecord
    source_refs: RuntimeExecutionPreparationProjectionSourceRef
    policy: RuntimeExecutionPreparationProjectionPolicy


@dataclass(frozen=True)
class RuntimeExecutionPreparationProjectionContractSnapshot:
    contract_status: str
    policy: RuntimeExecutionPreparationProjectionPolicy
    allowed_statuses: tuple[str, ...]
    forbidden_statuses: tuple[str, ...]
    allowed_readiness: tuple[str, ...]
    forbidden_readiness: tuple[str, ...]
    projection_kinds: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    forbidden_metadata_keys: tuple[str, ...]
    projection: RuntimeExecutionPreparationProjectionCore | None
    master_panel_projection: RuntimeExecutionPreparationMasterPanelProjection | None
    user_panel_projection: RuntimeExecutionPreparationUserPanelProjection | None
    internal_audit_projection: RuntimeExecutionPreparationInternalAuditProjection | None
    summary_projection: RuntimeExecutionPreparationSummaryProjection | None
    status_only_projection: RuntimeExecutionPreparationStatusOnlyProjection | None
    blocked_projection: RuntimeExecutionPreparationBlockedProjection | None
    validation: RuntimeExecutionPreparationProjectionValidationResult | None
    decision: RuntimeExecutionPreparationProjectionDecisionRecord | None
    source_refs: RuntimeExecutionPreparationProjectionSourceRef | None
    parent_read_model_contract_ref: str
    parent_package_contract_ref: str
    parent_preparation_contract_ref: str


def build_runtime_execution_preparation_projection_policy() -> RuntimeExecutionPreparationProjectionPolicy:
    return RuntimeExecutionPreparationProjectionPolicy()


def sanitize_runtime_execution_preparation_projection_metadata(
    raw_metadata: Mapping[str, Any] | None,
) -> RuntimeExecutionPreparationProjectionMetadata:
    metadata = raw_metadata or {}
    sanitized: dict[str, Any] = {}
    blocked: list[str] = []
    for key, value in metadata.items():
        key_text = str(key)
        normalized = key_text.lower()
        if _is_forbidden_metadata_key(normalized):
            blocked.append(key_text)
            continue
        if key_text in SAFE_METADATA_KEYS:
            sanitized[key_text] = _to_json_safe(value)
    return RuntimeExecutionPreparationProjectionMetadata(
        projection_reason=str(sanitized.get("projection_reason", "")),
        projection_scope=str(sanitized.get("projection_scope", "")),
        projection_kind=str(sanitized.get("projection_kind", "")),
        created_by=str(sanitized.get("created_by", "")),
        source=str(sanitized.get("source", "")),
        tags=_to_tuple_of_strings(sanitized.get("tags", ())),
        notes=_to_tuple_of_strings(sanitized.get("notes", ())),
        read_model_ref=str(sanitized.get("read_model_ref", "")),
        package_ref=str(sanitized.get("package_ref", "")),
        contract_ref=str(sanitized.get("contract_ref", "")),
        visibility=str(sanitized.get("visibility", "")),
        blocked_keys=tuple(blocked),
    )


def build_runtime_execution_preparation_projection_source_ref(
    *,
    projection_id: str,
    read_model_id: str,
    package_id: str,
    preparation_id: str,
    intent_ref: str,
    source_read_model_ref: str,
    source_package_ref: str,
    source_contract_refs: tuple[str, ...] | list[str] | None = None,
    attempt_ref: str | None = None,
    parent_read_model_contract_ref: str = PARENT_READ_MODEL_CONTRACT_REF,
    parent_package_contract_ref: str = PARENT_PACKAGE_CONTRACT_REF,
    parent_preparation_contract_ref: str = PARENT_PREPARATION_CONTRACT_REF,
    serialization_version: str = "runtime_execution_preparation_projection_source_ref.v1",
) -> RuntimeExecutionPreparationProjectionSourceRef:
    return RuntimeExecutionPreparationProjectionSourceRef(
        projection_id=_clean_ref(projection_id),
        read_model_id=_clean_ref(read_model_id),
        package_id=_clean_ref(package_id),
        preparation_id=_clean_ref(preparation_id),
        intent_ref=_clean_ref(intent_ref),
        attempt_ref=_clean_optional_ref(attempt_ref),
        source_read_model_ref=_clean_ref(source_read_model_ref),
        source_package_ref=_clean_ref(source_package_ref),
        source_contract_refs=_sanitize_ref_list(source_contract_refs or ()),
        parent_read_model_contract_ref=_clean_ref(parent_read_model_contract_ref),
        parent_package_contract_ref=_clean_ref(parent_package_contract_ref),
        parent_preparation_contract_ref=_clean_ref(parent_preparation_contract_ref),
        serialization_version=_clean_ref(serialization_version),
    )


def build_runtime_execution_preparation_projection(
    *,
    source_ref: RuntimeExecutionPreparationProjectionSourceRef,
    projection_kind: RuntimeExecutionPreparationProjectionKind | str = (
        RuntimeExecutionPreparationProjectionKind.SUMMARY_PROJECTION
    ),
    projection_status: RuntimeExecutionPreparationProjectionStatus | str = (
        RuntimeExecutionPreparationProjectionStatus.PROJECTION_READY_SIMULATED
    ),
    projection_readiness: RuntimeExecutionPreparationProjectionReadiness | str = (
        RuntimeExecutionPreparationProjectionReadiness.READY_FOR_RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTRACT
    ),
    visibility: RuntimeExecutionPreparationProjectionVisibility | str = (
        RuntimeExecutionPreparationProjectionVisibility.INTERNAL_ONLY
    ),
    risk_level: RuntimeExecutionPreparationProjectionRiskLevel | str = RuntimeExecutionPreparationProjectionRiskLevel.LOW,
    execution_scope: str = "future_safe_projection",
    execution_mode: str = "contract_only",
    decision: RuntimeExecutionPreparationProjectionDecision | str = (
        RuntimeExecutionPreparationProjectionDecision.ALLOW_READ_ONLY_PROJECTION
    ),
    validation_status: str = "projection_validation_pending",
    dependency_summary: str = "dependencies:0",
    boundary_summary: str = "boundaries:0",
    blocked_capabilities_summary: str = "",
    warning_summary: str = "warnings:0",
    error_summary: str = "errors:0",
    safe_summary: str = "Runtime Execution Preparation Projection is read-only and non-operational.",
    metadata: RuntimeExecutionPreparationProjectionMetadata | Mapping[str, Any] | None = None,
    serialization_version: str = "runtime_execution_preparation_projection.v1",
) -> RuntimeExecutionPreparationProjectionCore:
    clean_metadata = (
        metadata
        if isinstance(metadata, RuntimeExecutionPreparationProjectionMetadata)
        else sanitize_runtime_execution_preparation_projection_metadata(metadata)
    )
    return RuntimeExecutionPreparationProjectionCore(
        projection_id=source_ref.projection_id,
        read_model_id=source_ref.read_model_id,
        package_id=source_ref.package_id,
        preparation_id=source_ref.preparation_id,
        intent_ref=source_ref.intent_ref,
        attempt_ref=source_ref.attempt_ref,
        projection_kind=_coerce_kind(projection_kind),
        projection_status=_coerce_status(projection_status),
        projection_readiness=projection_readiness,
        visibility=_coerce_visibility(visibility),
        risk_level=_coerce_risk_level(risk_level),
        execution_scope=_clean_ref(execution_scope),
        execution_mode=_clean_ref(execution_mode),
        decision=_coerce_decision(decision),
        validation_status=_clean_ref(validation_status),
        dependency_summary=_clean_summary(dependency_summary),
        boundary_summary=_clean_summary(boundary_summary),
        blocked_capabilities_summary=_clean_summary(
            blocked_capabilities_summary or f"blocked_capabilities:{len(BLOCKED_CAPABILITIES)}"
        ),
        warning_summary=_clean_summary(warning_summary),
        error_summary=_clean_summary(error_summary),
        safe_summary=_clean_summary(safe_summary),
        source_read_model_ref=source_ref.source_read_model_ref,
        source_package_ref=source_ref.source_package_ref,
        source_contract_refs=source_ref.source_contract_refs,
        parent_read_model_contract_ref=source_ref.parent_read_model_contract_ref,
        parent_package_contract_ref=source_ref.parent_package_contract_ref,
        parent_preparation_contract_ref=source_ref.parent_preparation_contract_ref,
        serialization_version=_clean_ref(serialization_version),
        metadata=clean_metadata,
    )


def build_runtime_execution_preparation_master_panel_projection(
    projection: RuntimeExecutionPreparationProjectionCore,
    technical_refs: tuple[str, ...] | list[str] | None = None,
) -> RuntimeExecutionPreparationMasterPanelProjection:
    return RuntimeExecutionPreparationMasterPanelProjection(
        projection_id=projection.projection_id,
        read_model_id=projection.read_model_id,
        package_id=projection.package_id,
        preparation_id=projection.preparation_id,
        intent_ref=projection.intent_ref,
        attempt_ref=projection.attempt_ref,
        status=_enum_or_string(projection.projection_status),
        readiness=_enum_or_string(projection.projection_readiness),
        risk_level=_enum_or_string(projection.risk_level),
        execution_scope=projection.execution_scope,
        execution_mode=projection.execution_mode,
        decision=_enum_or_string(projection.decision),
        validation_status=projection.validation_status,
        dependency_summary=projection.dependency_summary,
        boundary_summary=projection.boundary_summary,
        blocked_capabilities_summary=projection.blocked_capabilities_summary,
        warning_summary=projection.warning_summary,
        error_summary=projection.error_summary,
        safe_summary=projection.safe_summary,
        technical_refs=_sanitize_ref_list(technical_refs or projection.source_contract_refs),
        visibility=RuntimeExecutionPreparationProjectionVisibility.MASTER_PANEL,
    )


def build_runtime_execution_preparation_user_panel_projection(
    projection: RuntimeExecutionPreparationProjectionCore,
) -> RuntimeExecutionPreparationUserPanelProjection:
    return RuntimeExecutionPreparationUserPanelProjection(
        projection_id=projection.projection_id,
        package_id=projection.package_id,
        status=_enum_or_string(projection.projection_status),
        readiness=_enum_or_string(projection.projection_readiness),
        risk_level=_enum_or_string(projection.risk_level),
        safe_summary=projection.safe_summary,
        dependency_summary=projection.dependency_summary,
        blocked_capabilities_summary=projection.blocked_capabilities_summary,
        warning_summary=projection.warning_summary,
        visibility=RuntimeExecutionPreparationProjectionVisibility.USER_PANEL,
    )


def build_runtime_execution_preparation_internal_audit_projection(
    projection: RuntimeExecutionPreparationProjectionCore,
    sanitized_refs: tuple[str, ...] | list[str] | None = None,
) -> RuntimeExecutionPreparationInternalAuditProjection:
    return RuntimeExecutionPreparationInternalAuditProjection(
        projection_id=projection.projection_id,
        read_model_id=projection.read_model_id,
        package_id=projection.package_id,
        preparation_id=projection.preparation_id,
        intent_ref=projection.intent_ref,
        attempt_ref=projection.attempt_ref,
        status=_enum_or_string(projection.projection_status),
        readiness=_enum_or_string(projection.projection_readiness),
        risk_level=_enum_or_string(projection.risk_level),
        decision=_enum_or_string(projection.decision),
        validation_status=projection.validation_status,
        sanitized_refs=_sanitize_ref_list(sanitized_refs or projection.source_contract_refs),
        blocked_keys=projection.metadata.blocked_keys,
        blocked_capabilities_summary=projection.blocked_capabilities_summary,
        warning_summary=projection.warning_summary,
        error_summary=projection.error_summary,
        visibility=RuntimeExecutionPreparationProjectionVisibility.INTERNAL_AUDIT,
    )


def build_runtime_execution_preparation_summary_projection(
    projection: RuntimeExecutionPreparationProjectionCore,
) -> RuntimeExecutionPreparationSummaryProjection:
    return RuntimeExecutionPreparationSummaryProjection(
        projection_id=projection.projection_id,
        package_id=projection.package_id,
        status=_enum_or_string(projection.projection_status),
        readiness=_enum_or_string(projection.projection_readiness),
        risk_level=_enum_or_string(projection.risk_level),
        safe_summary=projection.safe_summary,
        visibility=RuntimeExecutionPreparationProjectionVisibility.SUMMARY_ONLY,
    )


def build_runtime_execution_preparation_status_only_projection(
    projection: RuntimeExecutionPreparationProjectionCore,
) -> RuntimeExecutionPreparationStatusOnlyProjection:
    return RuntimeExecutionPreparationStatusOnlyProjection(
        projection_id=projection.projection_id,
        package_id=projection.package_id,
        status=_enum_or_string(projection.projection_status),
        readiness=_enum_or_string(projection.projection_readiness),
        risk_level=_enum_or_string(projection.risk_level),
        visibility=RuntimeExecutionPreparationProjectionVisibility.STATUS_ONLY,
    )


def build_runtime_execution_preparation_blocked_projection(
    projection: RuntimeExecutionPreparationProjectionCore,
    blocked_reason: str = "blocked",
) -> RuntimeExecutionPreparationBlockedProjection:
    return RuntimeExecutionPreparationBlockedProjection(
        projection_id=projection.projection_id,
        package_id=projection.package_id,
        status=RuntimeExecutionPreparationProjectionStatus.PROJECTION_BLOCKED.value,
        readiness=_enum_or_string(projection.projection_readiness),
        risk_level=_enum_or_string(projection.risk_level),
        safe_summary=projection.safe_summary,
        blocked_reason=_clean_summary(blocked_reason),
        visibility=RuntimeExecutionPreparationProjectionVisibility.BLOCKED,
    )


def validate_runtime_execution_preparation_projection(
    projection: RuntimeExecutionPreparationProjectionCore,
    policy: RuntimeExecutionPreparationProjectionPolicy | None = None,
    master_projection: RuntimeExecutionPreparationMasterPanelProjection | None = None,
    user_projection: RuntimeExecutionPreparationUserPanelProjection | None = None,
    internal_audit_projection: RuntimeExecutionPreparationInternalAuditProjection | None = None,
    summary_projection: RuntimeExecutionPreparationSummaryProjection | None = None,
    status_only_projection: RuntimeExecutionPreparationStatusOnlyProjection | None = None,
    blocked_projection: RuntimeExecutionPreparationBlockedProjection | None = None,
) -> RuntimeExecutionPreparationProjectionValidationResult:
    resolved_policy = policy or build_runtime_execution_preparation_projection_policy()
    errors: list[str] = []
    warnings: list[str] = []
    policy_violations: list[str] = []
    visibility_violations: list[str] = []
    projection_violations: list[str] = []
    missing_refs = list(
        build_runtime_execution_preparation_projection_source_ref(
            projection_id=projection.projection_id,
            read_model_id=projection.read_model_id,
            package_id=projection.package_id,
            preparation_id=projection.preparation_id,
            intent_ref=projection.intent_ref,
            attempt_ref=projection.attempt_ref,
            source_read_model_ref=projection.source_read_model_ref,
            source_package_ref=projection.source_package_ref,
            source_contract_refs=projection.source_contract_refs,
            parent_read_model_contract_ref=projection.parent_read_model_contract_ref,
            parent_package_contract_ref=projection.parent_package_contract_ref,
            parent_preparation_contract_ref=projection.parent_preparation_contract_ref,
        ).missing_critical_source_refs()
    )
    for missing in missing_refs:
        errors.append(f"missing_source_ref:{missing}")
    forbidden_readiness_detected = _forbidden_readiness_detected(projection.projection_readiness)
    for readiness in forbidden_readiness_detected:
        errors.append(f"forbidden_readiness:{readiness}")
    status_value = _enum_or_string(projection.projection_status)
    forbidden_status_detected = (status_value,) if status_value in FORBIDDEN_STATUSES else ()
    for status in forbidden_status_detected:
        errors.append(f"forbidden_status:{status}")
    if not forbidden_status_detected and status_value not in ALLOWED_STATUSES:
        errors.append(f"status_not_allowed:{status_value}")
    if projection.metadata.blocked_keys:
        errors.append("dangerous_metadata_detected")
    if not resolved_policy.contract_ready:
        policy_violations.append("policy_contract_ready_false")
    if not resolved_policy.read_only_enabled:
        policy_violations.append("policy_read_only_enabled_false")
    for field_name, value in asdict(resolved_policy).items():
        if field_name not in {"contract_ready", "read_only_enabled"} and value is True:
            policy_violations.append(f"operational_policy_flag_enabled:{field_name}")
    errors.extend(policy_violations)
    for projection_name, projection_view in (
        ("master_panel_projection", master_projection),
        ("user_panel_projection", user_projection),
        ("internal_audit_projection", internal_audit_projection),
        ("summary_projection", summary_projection),
        ("status_only_projection", status_only_projection),
        ("blocked_projection", blocked_projection),
    ):
        if projection_view is not None:
            projection_violations.extend(_unsafe_projection_fragments(projection_name, projection_view))
    if user_projection is not None:
        projection_violations.extend(_unsafe_user_projection_fragments(user_projection))
    if any(
        item is None
        for item in (
            master_projection,
            user_projection,
            internal_audit_projection,
            summary_projection,
            status_only_projection,
            blocked_projection,
        )
    ):
        visibility_violations.append("safe_projections_required")
    if visibility_violations:
        errors.extend(visibility_violations)
    if projection_violations:
        errors.extend(projection_violations)
    try:
        json.dumps(runtime_execution_preparation_projection_to_dict(projection), sort_keys=True)
    except (TypeError, ValueError):
        errors.append("projection_not_json_safe")
    status = (
        RuntimeExecutionPreparationProjectionStatus.PROJECTION_READY_SIMULATED
        if not errors and not missing_refs
        else RuntimeExecutionPreparationProjectionStatus.PROJECTION_INVALID
    )
    return RuntimeExecutionPreparationProjectionValidationResult(
        is_valid=not errors and not missing_refs,
        status=status,
        readiness=projection.projection_readiness,
        missing_source_refs=tuple(dict.fromkeys(missing_refs)),
        forbidden_readiness_detected=forbidden_readiness_detected,
        forbidden_status_detected=forbidden_status_detected,
        metadata_blocked_keys=projection.metadata.blocked_keys,
        policy_violations=tuple(dict.fromkeys(policy_violations)),
        visibility_violations=tuple(dict.fromkeys(visibility_violations)),
        projection_violations=tuple(dict.fromkeys(projection_violations)),
        errors=tuple(dict.fromkeys(errors)),
        warnings=tuple(dict.fromkeys(warnings)),
    )


def decide_runtime_execution_preparation_projection(
    validation_result: RuntimeExecutionPreparationProjectionValidationResult,
    policy: RuntimeExecutionPreparationProjectionPolicy | None = None,
) -> RuntimeExecutionPreparationProjectionDecisionRecord:
    resolved_policy = policy or build_runtime_execution_preparation_projection_policy()
    if any(
        value is True
        for key, value in asdict(resolved_policy).items()
        if key not in {"contract_ready", "read_only_enabled"}
    ):
        decision = RuntimeExecutionPreparationProjectionDecision.REQUIRE_POLICY_DEFAULT_DENY
        allowed = False
        reason = "policy_not_default_deny"
    elif validation_result.policy_violations:
        decision = RuntimeExecutionPreparationProjectionDecision.REQUIRE_POLICY_DEFAULT_DENY
        allowed = False
        reason = "policy_violations"
    elif validation_result.metadata_blocked_keys:
        decision = RuntimeExecutionPreparationProjectionDecision.REQUIRE_METADATA_SANITIZATION
        allowed = False
        reason = "metadata_blocked"
    elif validation_result.projection_violations:
        decision = RuntimeExecutionPreparationProjectionDecision.REQUIRE_VISIBILITY_FILTERING
        allowed = False
        reason = "projection_violations"
    elif validation_result.visibility_violations:
        decision = RuntimeExecutionPreparationProjectionDecision.REQUIRE_READ_MODEL_FILTER
        allowed = False
        reason = "safe_projection_required"
    elif validation_result.missing_source_refs:
        decision = RuntimeExecutionPreparationProjectionDecision.REQUIRE_SOURCE_REFS
        allowed = False
        reason = "missing_source_refs"
    elif validation_result.errors:
        decision = RuntimeExecutionPreparationProjectionDecision.INVALID
        allowed = False
        reason = "validation_errors"
    elif validation_result.is_valid:
        decision = RuntimeExecutionPreparationProjectionDecision.ALLOW_READ_ONLY_PROJECTION
        allowed = True
        reason = "read_only_projection_only"
    else:
        decision = RuntimeExecutionPreparationProjectionDecision.BLOCK_PROJECTION
        allowed = False
        reason = "blocked"
    return RuntimeExecutionPreparationProjectionDecisionRecord(
        decision=decision,
        allowed=allowed,
        read_only_projection_allowed=allowed
        and decision == RuntimeExecutionPreparationProjectionDecision.ALLOW_READ_ONLY_PROJECTION,
        runtime_execution_allowed=False,
        runtime_activation_allowed=False,
        dry_run_execution_allowed=False,
        tool_execution_allowed=False,
        model_invocation_allowed=False,
        context_injection_allowed=False,
        output_delivery_allowed=False,
        writes_allowed=False,
        stores_allowed=False,
        memory_allowed=False,
        network_allowed=False,
        browser_allowed=False,
        filesystem_allowed=False,
        env_allowed=False,
        secrets_allowed=False,
        api_allowed=False,
        ui_allowed=False,
        permission_bypass_allowed=False,
        raw_package_to_user_projection_allowed=False,
        reason=reason,
        errors=validation_result.errors,
        warnings=validation_result.warnings,
    )


def runtime_execution_preparation_projection_to_dict(value: Any) -> Any:
    return _to_json_safe(value)


def build_runtime_execution_preparation_projection_snapshot(
    *,
    projection: RuntimeExecutionPreparationProjectionCore,
    master_panel_projection: RuntimeExecutionPreparationMasterPanelProjection,
    user_panel_projection: RuntimeExecutionPreparationUserPanelProjection,
    internal_audit_projection: RuntimeExecutionPreparationInternalAuditProjection,
    summary_projection: RuntimeExecutionPreparationSummaryProjection,
    status_only_projection: RuntimeExecutionPreparationStatusOnlyProjection,
    blocked_projection: RuntimeExecutionPreparationBlockedProjection,
    validation: RuntimeExecutionPreparationProjectionValidationResult,
    decision: RuntimeExecutionPreparationProjectionDecisionRecord,
    source_refs: RuntimeExecutionPreparationProjectionSourceRef,
    policy: RuntimeExecutionPreparationProjectionPolicy | None = None,
) -> RuntimeExecutionPreparationProjectionSnapshot:
    return RuntimeExecutionPreparationProjectionSnapshot(
        projection=projection,
        master_panel_projection=master_panel_projection,
        user_panel_projection=user_panel_projection,
        internal_audit_projection=internal_audit_projection,
        summary_projection=summary_projection,
        status_only_projection=status_only_projection,
        blocked_projection=blocked_projection,
        validation=validation,
        decision=decision,
        source_refs=source_refs,
        policy=policy or build_runtime_execution_preparation_projection_policy(),
    )


def build_runtime_execution_preparation_projection_contract_snapshot(
    *,
    projection: RuntimeExecutionPreparationProjectionCore | None = None,
    master_panel_projection: RuntimeExecutionPreparationMasterPanelProjection | None = None,
    user_panel_projection: RuntimeExecutionPreparationUserPanelProjection | None = None,
    internal_audit_projection: RuntimeExecutionPreparationInternalAuditProjection | None = None,
    summary_projection: RuntimeExecutionPreparationSummaryProjection | None = None,
    status_only_projection: RuntimeExecutionPreparationStatusOnlyProjection | None = None,
    blocked_projection: RuntimeExecutionPreparationBlockedProjection | None = None,
    validation: RuntimeExecutionPreparationProjectionValidationResult | None = None,
    decision: RuntimeExecutionPreparationProjectionDecisionRecord | None = None,
    source_refs: RuntimeExecutionPreparationProjectionSourceRef | None = None,
    policy: RuntimeExecutionPreparationProjectionPolicy | None = None,
) -> RuntimeExecutionPreparationProjectionContractSnapshot:
    return RuntimeExecutionPreparationProjectionContractSnapshot(
        contract_status=CONTRACT_STATUS,
        policy=policy or build_runtime_execution_preparation_projection_policy(),
        allowed_statuses=ALLOWED_STATUSES,
        forbidden_statuses=FORBIDDEN_STATUSES,
        allowed_readiness=ALLOWED_READINESS,
        forbidden_readiness=FORBIDDEN_READINESS,
        projection_kinds=PROJECTION_KINDS,
        blocked_capabilities=BLOCKED_CAPABILITIES,
        forbidden_metadata_keys=FORBIDDEN_METADATA_KEYS,
        projection=projection,
        master_panel_projection=master_panel_projection,
        user_panel_projection=user_panel_projection,
        internal_audit_projection=internal_audit_projection,
        summary_projection=summary_projection,
        status_only_projection=status_only_projection,
        blocked_projection=blocked_projection,
        validation=validation,
        decision=decision,
        source_refs=source_refs,
        parent_read_model_contract_ref=PARENT_READ_MODEL_CONTRACT_REF,
        parent_package_contract_ref=PARENT_PACKAGE_CONTRACT_REF,
        parent_preparation_contract_ref=PARENT_PREPARATION_CONTRACT_REF,
    )


def get_runtime_execution_preparation_projection_contract_status() -> dict[str, Any]:
    return {
        "contract_status": CONTRACT_STATUS,
        "verdict": CONTRACT_VERDICT,
        "readiness": CONTRACT_READINESS,
        "next_step": CONTRACT_NEXT_STEP,
        "parent_read_model_contract_ref": PARENT_READ_MODEL_CONTRACT_REF,
        "parent_package_contract_ref": PARENT_PACKAGE_CONTRACT_REF,
        "parent_preparation_contract_ref": PARENT_PREPARATION_CONTRACT_REF,
        "read_model_contract_ready": read_model_contract.RUNTIME_EXECUTION_PREPARATION_READ_MODEL_CONTRACT_READY,
        "package_contract_ready": package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_READY,
        "preparation_contract_ready": parent_contract.RUNTIME_EXECUTION_PREPARATION_CONTRACT_READY,
        "contract_ready": RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTRACT_READY,
        "projection_operational": RUNTIME_EXECUTION_PREPARATION_PROJECTION_OPERATIONAL,
        "runtime_active": RUNTIME_EXECUTION_PREPARATION_PROJECTION_RUNTIME_ACTIVE,
        "execution_active": RUNTIME_EXECUTION_PREPARATION_PROJECTION_EXECUTION_ACTIVE,
        "dry_run_active": RUNTIME_EXECUTION_PREPARATION_PROJECTION_DRY_RUN_ACTIVE,
        "tools_enabled": RUNTIME_EXECUTION_PREPARATION_PROJECTION_TOOLS_ENABLED,
        "models_enabled": RUNTIME_EXECUTION_PREPARATION_PROJECTION_MODELS_ENABLED,
        "context_enabled": RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTEXT_ENABLED,
        "output_enabled": RUNTIME_EXECUTION_PREPARATION_PROJECTION_OUTPUT_ENABLED,
        "writes_enabled": RUNTIME_EXECUTION_PREPARATION_PROJECTION_WRITES_ENABLED,
        "stores_enabled": RUNTIME_EXECUTION_PREPARATION_PROJECTION_STORES_ENABLED,
        "memory_enabled": RUNTIME_EXECUTION_PREPARATION_PROJECTION_MEMORY_ENABLED,
        "network_enabled": RUNTIME_EXECUTION_PREPARATION_PROJECTION_NETWORK_ENABLED,
        "browser_enabled": RUNTIME_EXECUTION_PREPARATION_PROJECTION_BROWSER_ENABLED,
        "filesystem_enabled": RUNTIME_EXECUTION_PREPARATION_PROJECTION_FILESYSTEM_ENABLED,
        "env_enabled": RUNTIME_EXECUTION_PREPARATION_PROJECTION_ENV_ENABLED,
        "secrets_enabled": RUNTIME_EXECUTION_PREPARATION_PROJECTION_SECRETS_ENABLED,
        "api_enabled": RUNTIME_EXECUTION_PREPARATION_PROJECTION_API_ENABLED,
        "ui_enabled": RUNTIME_EXECUTION_PREPARATION_PROJECTION_UI_ENABLED,
        "ui_device_enabled": RUNTIME_EXECUTION_PREPARATION_PROJECTION_UI_DEVICE_ENABLED,
        "integrations_enabled": RUNTIME_EXECUTION_PREPARATION_PROJECTION_INTEGRATIONS_ENABLED,
        "excluded_external_concepts": tuple(sorted(EXCLUDED_EXTERNAL_CONCEPTS)),
    }


def _is_forbidden_metadata_key(normalized_key: str) -> bool:
    return any(fragment in normalized_key for fragment in FORBIDDEN_METADATA_KEYS)


def _forbidden_readiness_detected(readiness: RuntimeExecutionPreparationProjectionReadiness | str) -> tuple[str, ...]:
    value = _enum_or_string(readiness)
    return (value,) if value in FORBIDDEN_READINESS else ()


def _coerce_status(
    value: RuntimeExecutionPreparationProjectionStatus | str,
) -> RuntimeExecutionPreparationProjectionStatus:
    if isinstance(value, RuntimeExecutionPreparationProjectionStatus):
        return value
    return RuntimeExecutionPreparationProjectionStatus(str(value))


def _coerce_kind(value: RuntimeExecutionPreparationProjectionKind | str) -> RuntimeExecutionPreparationProjectionKind:
    if isinstance(value, RuntimeExecutionPreparationProjectionKind):
        return value
    return RuntimeExecutionPreparationProjectionKind(str(value))


def _coerce_visibility(
    value: RuntimeExecutionPreparationProjectionVisibility | str,
) -> RuntimeExecutionPreparationProjectionVisibility:
    if isinstance(value, RuntimeExecutionPreparationProjectionVisibility):
        return value
    return RuntimeExecutionPreparationProjectionVisibility(str(value))


def _coerce_decision(
    value: RuntimeExecutionPreparationProjectionDecision | str,
) -> RuntimeExecutionPreparationProjectionDecision:
    if isinstance(value, RuntimeExecutionPreparationProjectionDecision):
        return value
    return RuntimeExecutionPreparationProjectionDecision(str(value))


def _coerce_risk_level(
    value: RuntimeExecutionPreparationProjectionRiskLevel | str,
) -> RuntimeExecutionPreparationProjectionRiskLevel:
    if isinstance(value, RuntimeExecutionPreparationProjectionRiskLevel):
        return value
    return RuntimeExecutionPreparationProjectionRiskLevel(str(value))


def _clean_ref(value: str | None) -> str:
    return str(value or "").strip()


def _clean_optional_ref(value: str | None) -> str | None:
    clean = _clean_ref(value)
    return clean or None


def _clean_summary(value: str | None) -> str:
    text = _clean_ref(value)
    return "" if _has_forbidden_fragment(text) else text


def _enum_or_string(value: Any) -> str:
    return value.value if isinstance(value, Enum) else str(value)


def _to_tuple_of_strings(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, tuple | list | set | frozenset):
        return tuple(str(item) for item in value)
    return (str(value),)


def _to_json_safe(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return _to_json_safe(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): _to_json_safe(item) for key, item in value.items()}
    if isinstance(value, tuple | list | set | frozenset):
        return [_to_json_safe(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _sanitize_ref_list(values: tuple[str, ...] | list[str]) -> tuple[str, ...]:
    return tuple(item for item in _to_tuple_of_strings(values) if not _has_forbidden_fragment(item))


def _has_forbidden_fragment(value: Any) -> bool:
    text = json.dumps(_to_json_safe(value), sort_keys=True).lower()
    return any(fragment in text for fragment in FORBIDDEN_PROJECTION_FRAGMENTS)


def _unsafe_projection_fragments(projection_name: str, projection: Any) -> tuple[str, ...]:
    dumped = json.dumps(_to_json_safe(projection), sort_keys=True).lower()
    return tuple(
        f"{projection_name}_contains_forbidden_fragment:{fragment}"
        for fragment in FORBIDDEN_PROJECTION_FRAGMENTS
        if fragment in dumped
    )


def _unsafe_user_projection_fragments(projection: RuntimeExecutionPreparationUserPanelProjection) -> tuple[str, ...]:
    dumped = json.dumps(_to_json_safe(projection), sort_keys=True).lower()
    return tuple(
        f"user_panel_projection_contains_forbidden_fragment:{fragment}"
        for fragment in USER_PROJECTION_FORBIDDEN_FRAGMENTS
        if fragment in dumped
    )
