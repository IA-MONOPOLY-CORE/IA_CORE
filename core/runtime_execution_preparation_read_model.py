"""Contract-only Runtime Execution Preparation Read Model.

This read-only, non-operational module projects safe information from the
Runtime Execution Preparation Package contract. It never stores, writes,
executes, invokes tools/models, accesses external systems, exposes APIs/UI,
or replaces permissions and the Security Layer.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
import json
from typing import Any, Mapping

from core import runtime_execution_preparation_contract as parent_contract
from core import runtime_execution_preparation_package as package_contract


RUNTIME_EXECUTION_PREPARATION_READ_MODEL_CONTRACT_READY = True
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_OPERATIONAL = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_RUNTIME_ACTIVE = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_EXECUTION_ACTIVE = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_DRY_RUN_ACTIVE = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_TOOLS_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_MODELS_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_CONTEXT_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_OUTPUT_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_WRITES_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_STORES_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_MEMORY_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_NETWORK_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_BROWSER_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_FILESYSTEM_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_ENV_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_SECRETS_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_API_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_UI_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_UI_DEVICE_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_READ_MODEL_INTEGRATIONS_ENABLED = False

CONTRACT_STATUS = "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_CONTRACT_READY"
CONTRACT_VERDICT = "RUNTIME_EXECUTION_PREPARATION_READ_MODEL_NO_OPERATIONAL_CONFIRMED"
CONTRACT_READINESS = "ready_for_runtime_execution_preparation_read_model_contract_e2e"
CONTRACT_NEXT_STEP = "PROMPT 4.5.1 - Checkpoint E2E Runtime Execution Preparation Read Model Contract"
PARENT_PACKAGE_CONTRACT_REF = "core.runtime_execution_preparation_package"
PARENT_PREPARATION_CONTRACT_REF = "core.runtime_execution_preparation_contract"
EXCLUDED_EXTERNAL_CONCEPTS = frozenset({"OBLITERATUS"})
OBLITERATUS_EXCLUSION_STATEMENTS = (
    "OBLITERATUS is excluded from Runtime Execution Preparation Read Model.",
    "OBLITERATUS is not an integration.",
    "OBLITERATUS is not a dependency.",
    "OBLITERATUS is not an adapter.",
    "OBLITERATUS is not a provider.",
    "OBLITERATUS is not a capability.",
    "OBLITERATUS is not a runtime.",
    "OBLITERATUS is not an execution source.",
    "OBLITERATUS is not a package source.",
    "OBLITERATUS is not a read model source.",
    "OBLITERATUS is not a read model metadata source.",
    "OBLITERATUS is not a read model view source.",
    "OBLITERATUS is not an audit source.",
)


class RuntimeExecutionPreparationReadModelStatus(str, Enum):
    READ_MODEL_UNINITIALIZED = "read_model_uninitialized"
    READ_MODEL_DRAFT = "read_model_draft"
    READ_MODEL_SOURCE_REQUIRED = "read_model_source_required"
    READ_MODEL_PROJECTION_REQUIRED = "read_model_projection_required"
    READ_MODEL_VISIBILITY_REQUIRED = "read_model_visibility_required"
    READ_MODEL_SAFE_VIEW_REQUIRED = "read_model_safe_view_required"
    READ_MODEL_READY_SIMULATED = "read_model_ready_simulated"
    READ_MODEL_BLOCKED = "read_model_blocked"
    READ_MODEL_INVALID = "read_model_invalid"
    READ_MODEL_ARCHIVED_SIMULATED = "read_model_archived_simulated"


class RuntimeExecutionPreparationReadModelReadiness(str, Enum):
    READY_FOR_RUNTIME_EXECUTION_PREPARATION_READ_MODEL_CONTRACT = (
        "ready_for_runtime_execution_preparation_read_model_contract"
    )
    READY_FOR_RUNTIME_EXECUTION_PREPARATION_READ_MODEL_CONTRACT_E2E = (
        "ready_for_runtime_execution_preparation_read_model_contract_e2e"
    )


class RuntimeExecutionPreparationReadModelVisibility(str, Enum):
    MASTER_PANEL_VIEW = "master_panel_view"
    USER_PANEL_VIEW = "user_panel_view"
    INTERNAL_AUDIT_VIEW = "internal_audit_view"
    INTERNAL_ONLY = "internal_only"
    BLOCKED = "blocked"


class RuntimeExecutionPreparationReadModelViewKind(str, Enum):
    MASTER_PANEL_VIEW = "master_panel_view"
    USER_PANEL_VIEW = "user_panel_view"
    INTERNAL_AUDIT_VIEW = "internal_audit_view"


class RuntimeExecutionPreparationReadModelDecision(str, Enum):
    ALLOW_READ_ONLY_MODEL = "allow_read_only_model"
    BLOCK_READ_MODEL = "block_read_model"
    REQUIRE_SOURCE_REFS = "require_source_refs"
    REQUIRE_SAFE_VIEW = "require_safe_view"
    REQUIRE_METADATA_SANITIZATION = "require_metadata_sanitization"
    REQUIRE_POLICY_DEFAULT_DENY = "require_policy_default_deny"
    REQUIRE_VISIBILITY_FILTERING = "require_visibility_filtering"
    INVALID = "invalid"


class RuntimeExecutionPreparationReadModelCapability(str, Enum):
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


class RuntimeExecutionPreparationReadModelRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


ALLOWED_STATUSES = tuple(status.value for status in RuntimeExecutionPreparationReadModelStatus)
FORBIDDEN_STATUSES = (
    "read_model_active",
    "read_model_running",
    "read_model_executing",
    "read_model_live",
    "read_model_enabled",
    "read_model_operational",
    "read_model_runtime_started",
    "read_model_execution_started",
    "read_model_dry_run_started",
    "read_model_tool_executing",
    "read_model_model_invoking",
    "read_model_context_injecting",
    "read_model_output_delivering",
    "read_model_writing",
    "read_model_store_mutating",
    "read_model_network_active",
    "read_model_browser_active",
    "read_model_filesystem_active",
    "read_model_env_active",
    "read_model_secret_active",
    "read_model_integration_active",
    "read_model_api_active",
    "read_model_ui_control_active",
)
ALLOWED_READINESS = tuple(readiness.value for readiness in RuntimeExecutionPreparationReadModelReadiness)
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
    "read_model_operational",
    "read_model_store_enabled",
    "read_model_writer_enabled",
    "read_model_api_enabled",
    "read_model_ui_enabled",
)
BLOCKED_CAPABILITIES = tuple(capability.value for capability in RuntimeExecutionPreparationReadModelCapability)
SAFE_METADATA_KEYS = (
    "read_model_reason",
    "read_model_scope",
    "created_by",
    "source",
    "tags",
    "notes",
    "package_ref",
    "contract_ref",
    "visibility",
)
FORBIDDEN_METADATA_KEYS = tuple(
    dict.fromkeys(
        (
            *package_contract.FORBIDDEN_METADATA_KEYS,
            "master_panel_internal_capability",
            "admin_secret",
            "permission_bypass",
        )
    )
)
REQUIRED_SOURCE_REF_FIELDS = (
    "package_id",
    "preparation_id",
    "intent_ref",
    "source_package_ref",
    "source_contract_ref",
)
FORBIDDEN_VIEW_FRAGMENTS = (
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
)
USER_PANEL_FORBIDDEN_FRAGMENTS = (
    *FORBIDDEN_VIEW_FRAGMENTS,
    "technical_refs",
    "technical_ref",
    "metadata",
    "master_panel",
    "admin",
    "security_internal",
    "permission_internal",
    "intent_internal",
    "attempt_internal",
)


@dataclass(frozen=True)
class RuntimeExecutionPreparationReadModelPolicy:
    contract_ready: bool = True
    read_only_enabled: bool = True
    read_model_operational_enabled: bool = False
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


@dataclass(frozen=True)
class RuntimeExecutionPreparationReadModelMetadata:
    read_model_reason: str = ""
    read_model_scope: str = ""
    created_by: str = ""
    source: str = ""
    tags: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    package_ref: str = ""
    contract_ref: str = ""
    visibility: str = ""
    blocked_keys: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuntimeExecutionPreparationReadModelSourceRef:
    package_id: str
    preparation_id: str
    intent_ref: str
    attempt_ref: str | None
    source_package_ref: str
    source_contract_ref: str
    safe_view_ref: str
    parent_contract_ref: str
    serialization_version: str

    def missing_critical_source_refs(self) -> tuple[str, ...]:
        return tuple(
            field for field in REQUIRED_SOURCE_REF_FIELDS if not str(getattr(self, field, "") or "").strip()
        )


@dataclass(frozen=True)
class RuntimeExecutionPreparationReadModelCore:
    read_model_id: str
    package_id: str
    preparation_id: str
    intent_ref: str
    attempt_ref: str | None
    status: RuntimeExecutionPreparationReadModelStatus | str
    readiness: RuntimeExecutionPreparationReadModelReadiness | str
    risk_level: RuntimeExecutionPreparationReadModelRiskLevel | str
    execution_scope: str
    execution_mode: str
    decision: RuntimeExecutionPreparationReadModelDecision | str
    validation_status: str
    missing_required_dependencies: tuple[str, ...]
    missing_optional_dependencies: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    warnings: tuple[str, ...]
    errors: tuple[str, ...]
    safe_summary: str
    visibility: RuntimeExecutionPreparationReadModelVisibility | str
    source_package_ref: str
    source_contract_ref: str
    serialization_version: str
    metadata: RuntimeExecutionPreparationReadModelMetadata


@dataclass(frozen=True)
class RuntimeExecutionPreparationMasterPanelView:
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
    missing_required_dependencies: tuple[str, ...]
    missing_optional_dependencies: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    warnings: tuple[str, ...]
    errors: tuple[str, ...]
    safe_summary: str
    technical_refs: tuple[str, ...]
    visibility: RuntimeExecutionPreparationReadModelVisibility


@dataclass(frozen=True)
class RuntimeExecutionPreparationUserPanelView:
    read_model_id: str
    package_id: str
    status: str
    readiness: str
    risk_level: str
    safe_summary: str
    missing_required_dependencies_summary: str
    blocked_capabilities_summary: str
    warnings_summary: str
    visibility: RuntimeExecutionPreparationReadModelVisibility


@dataclass(frozen=True)
class RuntimeExecutionPreparationInternalAuditView:
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
    blocked_capabilities: tuple[str, ...]
    warnings: tuple[str, ...]
    errors: tuple[str, ...]
    visibility: RuntimeExecutionPreparationReadModelVisibility


@dataclass(frozen=True)
class RuntimeExecutionPreparationReadModelValidationResult:
    is_valid: bool
    status: RuntimeExecutionPreparationReadModelStatus
    readiness: RuntimeExecutionPreparationReadModelReadiness | str
    missing_source_refs: tuple[str, ...]
    forbidden_readiness_detected: tuple[str, ...]
    forbidden_status_detected: tuple[str, ...]
    metadata_blocked_keys: tuple[str, ...]
    policy_violations: tuple[str, ...]
    visibility_violations: tuple[str, ...]
    view_violations: tuple[str, ...]
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeExecutionPreparationReadModelDecisionRecord:
    decision: RuntimeExecutionPreparationReadModelDecision
    allowed: bool
    read_only_model_allowed: bool
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
    reason: str
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeExecutionPreparationReadModelSnapshot:
    read_model: RuntimeExecutionPreparationReadModelCore
    master_panel_view: RuntimeExecutionPreparationMasterPanelView
    user_panel_view: RuntimeExecutionPreparationUserPanelView
    internal_audit_view: RuntimeExecutionPreparationInternalAuditView
    validation: RuntimeExecutionPreparationReadModelValidationResult
    decision: RuntimeExecutionPreparationReadModelDecisionRecord
    source_refs: RuntimeExecutionPreparationReadModelSourceRef
    policy: RuntimeExecutionPreparationReadModelPolicy


@dataclass(frozen=True)
class RuntimeExecutionPreparationReadModelContractSnapshot:
    contract_status: str
    policy: RuntimeExecutionPreparationReadModelPolicy
    allowed_statuses: tuple[str, ...]
    forbidden_statuses: tuple[str, ...]
    allowed_readiness: tuple[str, ...]
    forbidden_readiness: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    forbidden_metadata_keys: tuple[str, ...]
    read_model: RuntimeExecutionPreparationReadModelCore | None
    master_panel_view: RuntimeExecutionPreparationMasterPanelView | None
    user_panel_view: RuntimeExecutionPreparationUserPanelView | None
    internal_audit_view: RuntimeExecutionPreparationInternalAuditView | None
    validation: RuntimeExecutionPreparationReadModelValidationResult | None
    decision: RuntimeExecutionPreparationReadModelDecisionRecord | None
    source_refs: RuntimeExecutionPreparationReadModelSourceRef | None
    parent_package_contract_ref: str
    parent_preparation_contract_ref: str


def build_runtime_execution_preparation_read_model_policy() -> RuntimeExecutionPreparationReadModelPolicy:
    return RuntimeExecutionPreparationReadModelPolicy()


def sanitize_runtime_execution_preparation_read_model_metadata(
    raw_metadata: Mapping[str, Any] | None,
) -> RuntimeExecutionPreparationReadModelMetadata:
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
    return RuntimeExecutionPreparationReadModelMetadata(
        read_model_reason=str(sanitized.get("read_model_reason", "")),
        read_model_scope=str(sanitized.get("read_model_scope", "")),
        created_by=str(sanitized.get("created_by", "")),
        source=str(sanitized.get("source", "")),
        tags=_to_tuple_of_strings(sanitized.get("tags", ())),
        notes=_to_tuple_of_strings(sanitized.get("notes", ())),
        package_ref=str(sanitized.get("package_ref", "")),
        contract_ref=str(sanitized.get("contract_ref", "")),
        visibility=str(sanitized.get("visibility", "")),
        blocked_keys=tuple(blocked),
    )


def build_runtime_execution_preparation_read_model_source_ref(
    *,
    package_id: str,
    preparation_id: str,
    intent_ref: str,
    source_package_ref: str,
    source_contract_ref: str,
    attempt_ref: str | None = None,
    safe_view_ref: str = "",
    parent_contract_ref: str = PARENT_PREPARATION_CONTRACT_REF,
    serialization_version: str = "runtime_execution_preparation_read_model_source_ref.v1",
) -> RuntimeExecutionPreparationReadModelSourceRef:
    return RuntimeExecutionPreparationReadModelSourceRef(
        package_id=_clean_ref(package_id),
        preparation_id=_clean_ref(preparation_id),
        intent_ref=_clean_ref(intent_ref),
        attempt_ref=_clean_optional_ref(attempt_ref),
        source_package_ref=_clean_ref(source_package_ref),
        source_contract_ref=_clean_ref(source_contract_ref),
        safe_view_ref=_clean_ref(safe_view_ref),
        parent_contract_ref=_clean_ref(parent_contract_ref),
        serialization_version=_clean_ref(serialization_version),
    )


def build_runtime_execution_preparation_read_model(
    *,
    read_model_id: str,
    source_ref: RuntimeExecutionPreparationReadModelSourceRef,
    status: RuntimeExecutionPreparationReadModelStatus | str = (
        RuntimeExecutionPreparationReadModelStatus.READ_MODEL_READY_SIMULATED
    ),
    readiness: RuntimeExecutionPreparationReadModelReadiness | str = (
        RuntimeExecutionPreparationReadModelReadiness.READY_FOR_RUNTIME_EXECUTION_PREPARATION_READ_MODEL_CONTRACT
    ),
    risk_level: RuntimeExecutionPreparationReadModelRiskLevel | str = RuntimeExecutionPreparationReadModelRiskLevel.LOW,
    execution_scope: str = "",
    execution_mode: str = "contract_only",
    decision: RuntimeExecutionPreparationReadModelDecision | str = (
        RuntimeExecutionPreparationReadModelDecision.ALLOW_READ_ONLY_MODEL
    ),
    validation_status: str = "valid",
    missing_required_dependencies: tuple[str, ...] | list[str] | None = None,
    missing_optional_dependencies: tuple[str, ...] | list[str] | None = None,
    blocked_capabilities: tuple[str, ...] | list[str] | None = None,
    warnings: tuple[str, ...] | list[str] | None = None,
    errors: tuple[str, ...] | list[str] | None = None,
    safe_summary: str = "Runtime Execution Preparation Read Model is read-only and non-operational.",
    visibility: RuntimeExecutionPreparationReadModelVisibility | str = (
        RuntimeExecutionPreparationReadModelVisibility.INTERNAL_ONLY
    ),
    metadata: RuntimeExecutionPreparationReadModelMetadata | Mapping[str, Any] | None = None,
    serialization_version: str = "runtime_execution_preparation_read_model.v1",
) -> RuntimeExecutionPreparationReadModelCore:
    clean_metadata = (
        metadata
        if isinstance(metadata, RuntimeExecutionPreparationReadModelMetadata)
        else sanitize_runtime_execution_preparation_read_model_metadata(metadata)
    )
    return RuntimeExecutionPreparationReadModelCore(
        read_model_id=_clean_ref(read_model_id),
        package_id=source_ref.package_id,
        preparation_id=source_ref.preparation_id,
        intent_ref=source_ref.intent_ref,
        attempt_ref=source_ref.attempt_ref,
        status=_coerce_status(status),
        readiness=readiness,
        risk_level=_coerce_risk_level(risk_level),
        execution_scope=_clean_ref(execution_scope),
        execution_mode=_clean_ref(execution_mode),
        decision=_coerce_decision(decision),
        validation_status=_clean_ref(validation_status),
        missing_required_dependencies=_to_tuple_of_strings(missing_required_dependencies or ()),
        missing_optional_dependencies=_to_tuple_of_strings(missing_optional_dependencies or ()),
        blocked_capabilities=_to_tuple_of_strings(blocked_capabilities or BLOCKED_CAPABILITIES),
        warnings=_to_tuple_of_strings(warnings or ()),
        errors=_to_tuple_of_strings(errors or ()),
        safe_summary=_clean_ref(safe_summary),
        visibility=_coerce_visibility(visibility),
        source_package_ref=source_ref.source_package_ref,
        source_contract_ref=source_ref.source_contract_ref,
        serialization_version=_clean_ref(serialization_version),
        metadata=clean_metadata,
    )


def build_runtime_execution_preparation_master_panel_view(
    read_model: RuntimeExecutionPreparationReadModelCore,
    technical_refs: tuple[str, ...] | list[str] | None = None,
) -> RuntimeExecutionPreparationMasterPanelView:
    return RuntimeExecutionPreparationMasterPanelView(
        read_model_id=read_model.read_model_id,
        package_id=read_model.package_id,
        preparation_id=read_model.preparation_id,
        intent_ref=read_model.intent_ref,
        attempt_ref=read_model.attempt_ref,
        status=_enum_or_string(read_model.status),
        readiness=_enum_or_string(read_model.readiness),
        risk_level=_enum_or_string(read_model.risk_level),
        execution_scope=read_model.execution_scope,
        execution_mode=read_model.execution_mode,
        decision=_enum_or_string(read_model.decision),
        validation_status=read_model.validation_status,
        missing_required_dependencies=read_model.missing_required_dependencies,
        missing_optional_dependencies=read_model.missing_optional_dependencies,
        blocked_capabilities=read_model.blocked_capabilities,
        warnings=read_model.warnings,
        errors=read_model.errors,
        safe_summary=read_model.safe_summary,
        technical_refs=_sanitize_ref_list(technical_refs or ()),
        visibility=RuntimeExecutionPreparationReadModelVisibility.MASTER_PANEL_VIEW,
    )


def build_runtime_execution_preparation_user_panel_view(
    read_model: RuntimeExecutionPreparationReadModelCore,
) -> RuntimeExecutionPreparationUserPanelView:
    return RuntimeExecutionPreparationUserPanelView(
        read_model_id=read_model.read_model_id,
        package_id=read_model.package_id,
        status=_enum_or_string(read_model.status),
        readiness=_enum_or_string(read_model.readiness),
        risk_level=_enum_or_string(read_model.risk_level),
        safe_summary=read_model.safe_summary,
        missing_required_dependencies_summary=_count_summary(read_model.missing_required_dependencies, "missing_required"),
        blocked_capabilities_summary=_count_summary(read_model.blocked_capabilities, "blocked_capabilities"),
        warnings_summary=_count_summary(read_model.warnings, "warnings"),
        visibility=RuntimeExecutionPreparationReadModelVisibility.USER_PANEL_VIEW,
    )


def build_runtime_execution_preparation_internal_audit_view(
    read_model: RuntimeExecutionPreparationReadModelCore,
    sanitized_refs: tuple[str, ...] | list[str] | None = None,
) -> RuntimeExecutionPreparationInternalAuditView:
    return RuntimeExecutionPreparationInternalAuditView(
        read_model_id=read_model.read_model_id,
        package_id=read_model.package_id,
        preparation_id=read_model.preparation_id,
        intent_ref=read_model.intent_ref,
        attempt_ref=read_model.attempt_ref,
        status=_enum_or_string(read_model.status),
        readiness=_enum_or_string(read_model.readiness),
        risk_level=_enum_or_string(read_model.risk_level),
        decision=_enum_or_string(read_model.decision),
        validation_status=read_model.validation_status,
        sanitized_refs=_sanitize_ref_list(sanitized_refs or ()),
        blocked_keys=read_model.metadata.blocked_keys,
        blocked_capabilities=read_model.blocked_capabilities,
        warnings=read_model.warnings,
        errors=read_model.errors,
        visibility=RuntimeExecutionPreparationReadModelVisibility.INTERNAL_AUDIT_VIEW,
    )


def validate_runtime_execution_preparation_read_model(
    read_model: RuntimeExecutionPreparationReadModelCore,
    policy: RuntimeExecutionPreparationReadModelPolicy | None = None,
    master_view: RuntimeExecutionPreparationMasterPanelView | None = None,
    user_view: RuntimeExecutionPreparationUserPanelView | None = None,
    audit_view: RuntimeExecutionPreparationInternalAuditView | None = None,
) -> RuntimeExecutionPreparationReadModelValidationResult:
    resolved_policy = policy or build_runtime_execution_preparation_read_model_policy()
    errors: list[str] = []
    warnings: list[str] = []
    policy_violations: list[str] = []
    visibility_violations: list[str] = []
    view_violations: list[str] = []
    missing_refs = list(
        build_runtime_execution_preparation_read_model_source_ref(
            package_id=read_model.package_id,
            preparation_id=read_model.preparation_id,
            intent_ref=read_model.intent_ref,
            attempt_ref=read_model.attempt_ref,
            source_package_ref=read_model.source_package_ref,
            source_contract_ref=read_model.source_contract_ref,
        ).missing_critical_source_refs()
    )
    if not read_model.read_model_id:
        errors.append("missing_required_ref:read_model_id")
    for missing in missing_refs:
        errors.append(f"missing_source_ref:{missing}")
    forbidden_readiness_detected = _forbidden_readiness_detected(read_model.readiness)
    for readiness in forbidden_readiness_detected:
        errors.append(f"forbidden_readiness:{readiness}")
    status_value = _enum_or_string(read_model.status)
    forbidden_status_detected = (status_value,) if status_value in FORBIDDEN_STATUSES else ()
    for status in forbidden_status_detected:
        errors.append(f"forbidden_status:{status}")
    if not forbidden_status_detected and status_value not in ALLOWED_STATUSES:
        errors.append(f"status_not_allowed:{status_value}")
    if read_model.metadata.blocked_keys:
        errors.append("dangerous_metadata_detected")
    if tuple(read_model.blocked_capabilities) != BLOCKED_CAPABILITIES:
        errors.append("blocked_capabilities_must_match_default_deny")
    if not resolved_policy.contract_ready:
        policy_violations.append("policy_contract_ready_false")
    if not resolved_policy.read_only_enabled:
        policy_violations.append("policy_read_only_enabled_false")
    for field_name, value in asdict(resolved_policy).items():
        if field_name not in {"contract_ready", "read_only_enabled"} and value is True:
            policy_violations.append(f"operational_policy_flag_enabled:{field_name}")
    errors.extend(policy_violations)
    for view_name, view in (
        ("master_panel_view", master_view),
        ("user_panel_view", user_view),
        ("internal_audit_view", audit_view),
    ):
        if view is not None:
            view_violations.extend(_unsafe_view_fragments(view_name, view))
    if user_view is not None:
        view_violations.extend(_unsafe_user_view_fragments(user_view))
    if master_view is None or user_view is None or audit_view is None:
        visibility_violations.append("safe_views_required")
    if visibility_violations:
        errors.extend(visibility_violations)
    if view_violations:
        errors.extend(view_violations)
    try:
        json.dumps(runtime_execution_preparation_read_model_to_dict(read_model), sort_keys=True)
    except (TypeError, ValueError):
        errors.append("read_model_not_json_safe")
    status = (
        RuntimeExecutionPreparationReadModelStatus.READ_MODEL_READY_SIMULATED
        if not errors and not missing_refs
        else RuntimeExecutionPreparationReadModelStatus.READ_MODEL_INVALID
    )
    return RuntimeExecutionPreparationReadModelValidationResult(
        is_valid=not errors and not missing_refs,
        status=status,
        readiness=read_model.readiness,
        missing_source_refs=tuple(dict.fromkeys(missing_refs)),
        forbidden_readiness_detected=forbidden_readiness_detected,
        forbidden_status_detected=forbidden_status_detected,
        metadata_blocked_keys=read_model.metadata.blocked_keys,
        policy_violations=tuple(dict.fromkeys(policy_violations)),
        visibility_violations=tuple(dict.fromkeys(visibility_violations)),
        view_violations=tuple(dict.fromkeys(view_violations)),
        errors=tuple(dict.fromkeys(errors)),
        warnings=tuple(dict.fromkeys(warnings)),
    )


def decide_runtime_execution_preparation_read_model(
    validation_result: RuntimeExecutionPreparationReadModelValidationResult,
    policy: RuntimeExecutionPreparationReadModelPolicy | None = None,
) -> RuntimeExecutionPreparationReadModelDecisionRecord:
    resolved_policy = policy or build_runtime_execution_preparation_read_model_policy()
    if any(
        value is True
        for key, value in asdict(resolved_policy).items()
        if key not in {"contract_ready", "read_only_enabled"}
    ):
        decision = RuntimeExecutionPreparationReadModelDecision.REQUIRE_POLICY_DEFAULT_DENY
        allowed = False
        reason = "policy_not_default_deny"
    elif validation_result.policy_violations:
        decision = RuntimeExecutionPreparationReadModelDecision.REQUIRE_POLICY_DEFAULT_DENY
        allowed = False
        reason = "policy_violations"
    elif validation_result.metadata_blocked_keys:
        decision = RuntimeExecutionPreparationReadModelDecision.REQUIRE_METADATA_SANITIZATION
        allowed = False
        reason = "metadata_blocked"
    elif validation_result.view_violations:
        decision = RuntimeExecutionPreparationReadModelDecision.REQUIRE_VISIBILITY_FILTERING
        allowed = False
        reason = "view_violations"
    elif validation_result.visibility_violations:
        decision = RuntimeExecutionPreparationReadModelDecision.REQUIRE_SAFE_VIEW
        allowed = False
        reason = "safe_view_required"
    elif validation_result.missing_source_refs:
        decision = RuntimeExecutionPreparationReadModelDecision.REQUIRE_SOURCE_REFS
        allowed = False
        reason = "missing_source_refs"
    elif validation_result.errors:
        decision = RuntimeExecutionPreparationReadModelDecision.INVALID
        allowed = False
        reason = "validation_errors"
    elif validation_result.is_valid:
        decision = RuntimeExecutionPreparationReadModelDecision.ALLOW_READ_ONLY_MODEL
        allowed = True
        reason = "read_only_model_only"
    else:
        decision = RuntimeExecutionPreparationReadModelDecision.BLOCK_READ_MODEL
        allowed = False
        reason = "blocked"
    return RuntimeExecutionPreparationReadModelDecisionRecord(
        decision=decision,
        allowed=allowed,
        read_only_model_allowed=allowed
        and decision == RuntimeExecutionPreparationReadModelDecision.ALLOW_READ_ONLY_MODEL,
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
        reason=reason,
        errors=validation_result.errors,
        warnings=validation_result.warnings,
    )


def runtime_execution_preparation_read_model_to_dict(value: Any) -> Any:
    return _to_json_safe(value)


def build_runtime_execution_preparation_read_model_snapshot(
    *,
    read_model: RuntimeExecutionPreparationReadModelCore,
    master_panel_view: RuntimeExecutionPreparationMasterPanelView,
    user_panel_view: RuntimeExecutionPreparationUserPanelView,
    internal_audit_view: RuntimeExecutionPreparationInternalAuditView,
    validation: RuntimeExecutionPreparationReadModelValidationResult,
    decision: RuntimeExecutionPreparationReadModelDecisionRecord,
    source_refs: RuntimeExecutionPreparationReadModelSourceRef,
    policy: RuntimeExecutionPreparationReadModelPolicy | None = None,
) -> RuntimeExecutionPreparationReadModelSnapshot:
    return RuntimeExecutionPreparationReadModelSnapshot(
        read_model=read_model,
        master_panel_view=master_panel_view,
        user_panel_view=user_panel_view,
        internal_audit_view=internal_audit_view,
        validation=validation,
        decision=decision,
        source_refs=source_refs,
        policy=policy or build_runtime_execution_preparation_read_model_policy(),
    )


def build_runtime_execution_preparation_read_model_contract_snapshot(
    *,
    read_model: RuntimeExecutionPreparationReadModelCore | None = None,
    master_panel_view: RuntimeExecutionPreparationMasterPanelView | None = None,
    user_panel_view: RuntimeExecutionPreparationUserPanelView | None = None,
    internal_audit_view: RuntimeExecutionPreparationInternalAuditView | None = None,
    validation: RuntimeExecutionPreparationReadModelValidationResult | None = None,
    decision: RuntimeExecutionPreparationReadModelDecisionRecord | None = None,
    source_refs: RuntimeExecutionPreparationReadModelSourceRef | None = None,
    policy: RuntimeExecutionPreparationReadModelPolicy | None = None,
) -> RuntimeExecutionPreparationReadModelContractSnapshot:
    return RuntimeExecutionPreparationReadModelContractSnapshot(
        contract_status=CONTRACT_STATUS,
        policy=policy or build_runtime_execution_preparation_read_model_policy(),
        allowed_statuses=ALLOWED_STATUSES,
        forbidden_statuses=FORBIDDEN_STATUSES,
        allowed_readiness=ALLOWED_READINESS,
        forbidden_readiness=FORBIDDEN_READINESS,
        blocked_capabilities=BLOCKED_CAPABILITIES,
        forbidden_metadata_keys=FORBIDDEN_METADATA_KEYS,
        read_model=read_model,
        master_panel_view=master_panel_view,
        user_panel_view=user_panel_view,
        internal_audit_view=internal_audit_view,
        validation=validation,
        decision=decision,
        source_refs=source_refs,
        parent_package_contract_ref=PARENT_PACKAGE_CONTRACT_REF,
        parent_preparation_contract_ref=PARENT_PREPARATION_CONTRACT_REF,
    )


def get_runtime_execution_preparation_read_model_contract_status() -> dict[str, Any]:
    return {
        "contract_status": CONTRACT_STATUS,
        "verdict": CONTRACT_VERDICT,
        "readiness": CONTRACT_READINESS,
        "next_step": CONTRACT_NEXT_STEP,
        "parent_package_contract_ref": PARENT_PACKAGE_CONTRACT_REF,
        "parent_preparation_contract_ref": PARENT_PREPARATION_CONTRACT_REF,
        "package_contract_ready": package_contract.RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_READY,
        "preparation_contract_ready": parent_contract.RUNTIME_EXECUTION_PREPARATION_CONTRACT_READY,
        "contract_ready": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_CONTRACT_READY,
        "read_model_operational": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_OPERATIONAL,
        "runtime_active": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_RUNTIME_ACTIVE,
        "execution_active": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_EXECUTION_ACTIVE,
        "dry_run_active": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_DRY_RUN_ACTIVE,
        "tools_enabled": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_TOOLS_ENABLED,
        "models_enabled": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_MODELS_ENABLED,
        "context_enabled": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_CONTEXT_ENABLED,
        "output_enabled": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_OUTPUT_ENABLED,
        "writes_enabled": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_WRITES_ENABLED,
        "stores_enabled": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_STORES_ENABLED,
        "memory_enabled": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_MEMORY_ENABLED,
        "network_enabled": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_NETWORK_ENABLED,
        "browser_enabled": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_BROWSER_ENABLED,
        "filesystem_enabled": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_FILESYSTEM_ENABLED,
        "env_enabled": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_ENV_ENABLED,
        "secrets_enabled": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_SECRETS_ENABLED,
        "api_enabled": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_API_ENABLED,
        "ui_enabled": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_UI_ENABLED,
        "ui_device_enabled": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_UI_DEVICE_ENABLED,
        "integrations_enabled": RUNTIME_EXECUTION_PREPARATION_READ_MODEL_INTEGRATIONS_ENABLED,
        "excluded_external_concepts": tuple(sorted(EXCLUDED_EXTERNAL_CONCEPTS)),
    }


def _is_forbidden_metadata_key(normalized_key: str) -> bool:
    return any(fragment in normalized_key for fragment in FORBIDDEN_METADATA_KEYS)


def _forbidden_readiness_detected(readiness: RuntimeExecutionPreparationReadModelReadiness | str) -> tuple[str, ...]:
    value = _enum_or_string(readiness)
    return (value,) if value in FORBIDDEN_READINESS else ()


def _coerce_status(value: RuntimeExecutionPreparationReadModelStatus | str) -> RuntimeExecutionPreparationReadModelStatus:
    if isinstance(value, RuntimeExecutionPreparationReadModelStatus):
        return value
    return RuntimeExecutionPreparationReadModelStatus(str(value))


def _coerce_visibility(
    value: RuntimeExecutionPreparationReadModelVisibility | str,
) -> RuntimeExecutionPreparationReadModelVisibility:
    if isinstance(value, RuntimeExecutionPreparationReadModelVisibility):
        return value
    return RuntimeExecutionPreparationReadModelVisibility(str(value))


def _coerce_decision(value: RuntimeExecutionPreparationReadModelDecision | str) -> RuntimeExecutionPreparationReadModelDecision:
    if isinstance(value, RuntimeExecutionPreparationReadModelDecision):
        return value
    return RuntimeExecutionPreparationReadModelDecision(str(value))


def _coerce_risk_level(value: RuntimeExecutionPreparationReadModelRiskLevel | str) -> RuntimeExecutionPreparationReadModelRiskLevel:
    if isinstance(value, RuntimeExecutionPreparationReadModelRiskLevel):
        return value
    return RuntimeExecutionPreparationReadModelRiskLevel(str(value))


def _clean_ref(value: str | None) -> str:
    return str(value or "").strip()


def _clean_optional_ref(value: str | None) -> str | None:
    clean = _clean_ref(value)
    return clean or None


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


def _count_summary(values: tuple[str, ...], label: str) -> str:
    return f"{label}:{len(values)}"


def _sanitize_ref_list(values: tuple[str, ...] | list[str]) -> tuple[str, ...]:
    return tuple(item for item in _to_tuple_of_strings(values) if not _has_forbidden_fragment(item))


def _has_forbidden_fragment(value: Any) -> bool:
    text = json.dumps(_to_json_safe(value), sort_keys=True).lower()
    return any(fragment in text for fragment in FORBIDDEN_VIEW_FRAGMENTS)


def _unsafe_view_fragments(view_name: str, view: Any) -> tuple[str, ...]:
    dumped = json.dumps(_to_json_safe(view), sort_keys=True).lower()
    return tuple(
        f"{view_name}_contains_forbidden_fragment:{fragment}"
        for fragment in FORBIDDEN_VIEW_FRAGMENTS
        if fragment in dumped
    )


def _unsafe_user_view_fragments(view: RuntimeExecutionPreparationUserPanelView) -> tuple[str, ...]:
    dumped = json.dumps(_to_json_safe(view), sort_keys=True).lower()
    return tuple(
        f"user_panel_view_contains_forbidden_fragment:{fragment}"
        for fragment in USER_PANEL_FORBIDDEN_FRAGMENTS
        if fragment in dumped
    )
