"""Contract-only Runtime Execution Preparation Package.

This non-operational module models a package for future execution preparation.
It depends on the parent Runtime Execution Preparation contract without mutating
it, and it never activates runtime, execution, dry-run, tools, models, context,
outputs, writes, stores, memory, network, browser, filesystem, env, secrets,
UI/device control, integrations, or OBLITERATUS.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
import json
from typing import Any, Mapping

from core import runtime_execution_preparation_contract as parent_contract


RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_READY = True
RUNTIME_EXECUTION_PREPARATION_PACKAGE_OPERATIONAL = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_RUNTIME_ACTIVE = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_EXECUTION_ACTIVE = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_DRY_RUN_ACTIVE = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_TOOLS_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_MODELS_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTEXT_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_OUTPUT_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_WRITES_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_STORES_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_MEMORY_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_NETWORK_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_BROWSER_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_FILESYSTEM_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_ENV_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_SECRETS_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_UI_DEVICE_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_PACKAGE_INTEGRATIONS_ENABLED = False

CONTRACT_STATUS = "RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_READY"
CONTRACT_VERDICT = "RUNTIME_EXECUTION_PREPARATION_PACKAGE_NO_OPERATIONAL_CONFIRMED"
CONTRACT_READINESS = "ready_for_runtime_execution_preparation_package_contract_e2e"
CONTRACT_NEXT_STEP = "PROMPT 4.3.1 — Checkpoint E2E Runtime Execution Preparation Package Contract"
PARENT_CONTRACT_REF = "core.runtime_execution_preparation_contract"
EXCLUDED_EXTERNAL_CONCEPTS = frozenset({"OBLITERATUS"})
OBLITERATUS_EXCLUSION_STATEMENTS = (
    "OBLITERATUS is excluded from Runtime Execution Preparation Package.",
    "OBLITERATUS is not an integration.",
    "OBLITERATUS is not a dependency.",
    "OBLITERATUS is not an adapter.",
    "OBLITERATUS is not a provider.",
    "OBLITERATUS is not a capability.",
    "OBLITERATUS is not a runtime.",
    "OBLITERATUS is not an execution source.",
    "OBLITERATUS is not a governance source.",
    "OBLITERATUS is not a state source.",
    "OBLITERATUS is not an observability source.",
    "OBLITERATUS is not an audit source.",
    "OBLITERATUS is not a package source.",
    "OBLITERATUS is not a package metadata source.",
    "OBLITERATUS is not a package decision source.",
)


class RuntimeExecutionPreparationPackageStatus(str, Enum):
    PACKAGE_UNINITIALIZED = "package_uninitialized"
    PACKAGE_DRAFT = "package_draft"
    PACKAGE_DEPENDENCIES_REQUIRED = "package_dependencies_required"
    PACKAGE_BOUNDARIES_REQUIRED = "package_boundaries_required"
    PACKAGE_METADATA_INVALID = "package_metadata_invalid"
    PACKAGE_READINESS_INVALID = "package_readiness_invalid"
    PACKAGE_POLICY_INVALID = "package_policy_invalid"
    PACKAGE_BLOCKED = "package_blocked"
    PACKAGE_READY_SIMULATED = "package_ready_simulated"
    PACKAGE_ARCHIVED_SIMULATED = "package_archived_simulated"
    PACKAGE_INVALID = "package_invalid"


class RuntimeExecutionPreparationPackageReadiness(str, Enum):
    READY_FOR_RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT = (
        "ready_for_runtime_execution_preparation_package_contract"
    )
    READY_FOR_RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_E2E = (
        "ready_for_runtime_execution_preparation_package_contract_e2e"
    )


class RuntimeExecutionPreparationPackageRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RuntimeExecutionPreparationPackageMode(str, Enum):
    CONTRACT_ONLY = "contract_only"
    SIMULATED_PACKAGE = "simulated_package"
    VALIDATION_ONLY = "validation_only"
    SNAPSHOT_ONLY = "snapshot_only"


class RuntimeExecutionPreparationPackageDecision(str, Enum):
    ALLOW_SIMULATED_PACKAGE = "allow_simulated_package"
    BLOCK_PACKAGE = "block_package"
    REQUIRE_DEPENDENCIES = "require_dependencies"
    REQUIRE_BOUNDARIES = "require_boundaries"
    REQUIRE_METADATA_SANITIZATION = "require_metadata_sanitization"
    REQUIRE_POLICY_DEFAULT_DENY = "require_policy_default_deny"
    REQUIRE_UI_SAFE_VIEW = "require_ui_safe_view"
    INVALID = "invalid"


class RuntimeExecutionPreparationPackageDependencyStatus(str, Enum):
    PRESENT = "present"
    MISSING_REQUIRED = "missing_required"
    MISSING_OPTIONAL = "missing_optional"


class RuntimeExecutionPreparationPackageCapability(str, Enum):
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
    UI_CONTROL = "ui_control"
    DEVICE_CONTROL = "device_control"
    INTEGRATIONS = "integrations"
    MARKET_CATALOG_RUNTIME = "market_catalog_runtime"
    BUSINESS_COMPOSITION_RUNTIME = "business_composition_runtime"
    OBLITERATUS_INTEGRATION = "obliteratus_integration"
    MASTER_PANEL_CAPABILITIES_FOR_USER_PANEL = "master_panel_capabilities_for_user_panel"
    RAW_INTERNAL_VISIBILITY = "raw_internal_visibility"


class RuntimeExecutionPreparationPackageVisibility(str, Enum):
    MASTER_PANEL_SAFE = "master_panel_safe"
    USER_PANEL_SAFE = "user_panel_safe"
    INTERNAL_ONLY = "internal_only"
    BLOCKED = "blocked"


ALLOWED_STATUSES = tuple(status.value for status in RuntimeExecutionPreparationPackageStatus)
FORBIDDEN_STATUSES = (
    "package_active",
    "package_running",
    "package_executing",
    "package_live",
    "package_enabled",
    "package_operational",
    "package_runtime_started",
    "package_execution_started",
    "package_dry_run_started",
    "package_tool_executing",
    "package_model_invoking",
    "package_context_injecting",
    "package_output_delivering",
    "package_writing",
    "package_store_mutating",
    "package_network_active",
    "package_browser_active",
    "package_filesystem_active",
    "package_env_active",
    "package_secret_active",
    "package_integration_active",
)
ALLOWED_READINESS = tuple(readiness.value for readiness in RuntimeExecutionPreparationPackageReadiness)
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
    "runtime_open",
    "runtime_active",
    "runtime_enabled",
    "execution_enabled",
    "operations_enabled",
    "package_operational",
    "package_runtime_enabled",
    "package_execution_enabled",
    "package_dry_run_enabled",
    "package_tool_enabled",
    "package_model_enabled",
    "package_context_enabled",
    "package_output_enabled",
    "package_store_enabled",
)
BLOCKED_CAPABILITIES = tuple(capability.value for capability in RuntimeExecutionPreparationPackageCapability)
FORBIDDEN_METADATA_KEYS = parent_contract.FORBIDDEN_METADATA_KEYS
SAFE_METADATA_KEYS = (
    "package_reason",
    "package_scope",
    "package_mode",
    "package_risk_level",
    "created_by",
    "source",
    "tags",
    "notes",
    "business_context_ref",
    "domain_ref",
    "agent_ref",
)
REQUIRED_DEPENDENCY_FIELDS = (
    "preparation_id",
    "intent_ref",
    "runtime_governance_ref",
    "runtime_state_ref",
    "observability_ref",
    "runtime_activation_gate_ref",
    "security_baseline_ref",
    "agent_permission_ref",
    "sandbox_boundary_ref",
    "tool_boundary_ref",
    "model_boundary_ref",
    "context_boundary_ref",
    "output_boundary_ref",
    "secrets_policy_ref",
    "prompt_injection_defense_ref",
)
OPTIONAL_DEPENDENCY_FIELDS = (
    "attempt_ref",
    "human_approval_ref",
    "kill_switch_ref",
    "rollback_ref",
    "dry_run_ref",
)


@dataclass(frozen=True)
class RuntimeExecutionPreparationPackagePolicy:
    contract_ready: bool = True
    package_operational_enabled: bool = False
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
    ui_device_enabled: bool = False
    integrations_enabled: bool = False
    master_panel_exposure_enabled: bool = False
    user_panel_raw_internal_exposure_enabled: bool = False
    automatic_approval_enabled: bool = False


@dataclass(frozen=True)
class RuntimeExecutionPreparationPackageMetadata:
    package_reason: str = ""
    package_scope: str = ""
    package_mode: str = ""
    package_risk_level: str = ""
    created_by: str = ""
    source: str = ""
    tags: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    business_context_ref: str = ""
    domain_ref: str = ""
    agent_ref: str = ""
    blocked_keys: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuntimeExecutionPreparationPackageDependencySet:
    preparation_id: str
    intent_ref: str
    attempt_ref: str | None
    runtime_governance_ref: str
    runtime_state_ref: str
    observability_ref: str
    runtime_activation_gate_ref: str
    security_baseline_ref: str
    agent_permission_ref: str
    sandbox_boundary_ref: str
    tool_boundary_ref: str
    model_boundary_ref: str
    context_boundary_ref: str
    output_boundary_ref: str
    secrets_policy_ref: str
    prompt_injection_defense_ref: str
    human_approval_ref: str | None = None
    kill_switch_ref: str | None = None
    rollback_ref: str | None = None
    dry_run_ref: str | None = None

    def required_dependencies(self) -> tuple[str, ...]:
        return REQUIRED_DEPENDENCY_FIELDS

    def optional_dependencies(self) -> tuple[str, ...]:
        return OPTIONAL_DEPENDENCY_FIELDS

    def missing_required_dependencies(self) -> tuple[str, ...]:
        return tuple(
            name for name in REQUIRED_DEPENDENCY_FIELDS if not str(getattr(self, name, "") or "").strip()
        )

    def missing_optional_dependencies(self) -> tuple[str, ...]:
        return tuple(name for name in OPTIONAL_DEPENDENCY_FIELDS if not getattr(self, name))


@dataclass(frozen=True)
class RuntimeExecutionPreparationPackageBoundarySet:
    security_baseline_ok: bool
    agent_permission_ok: bool
    sandbox_boundary_ok: bool
    tool_boundary_ok: bool
    model_boundary_ok: bool
    context_boundary_ok: bool
    output_boundary_ok: bool
    secrets_policy_ok: bool
    prompt_injection_defense_ok: bool
    runtime_governance_ok: bool
    runtime_state_ok: bool
    observability_ok: bool
    runtime_activation_gate_ok: bool
    human_approval_ok: bool = False
    kill_switch_ok: bool = False
    rollback_ok: bool = False
    dry_run_ok: bool = False
    master_user_panel_separation_ok: bool = True
    ui_safe_visibility_ok: bool = True

    def missing_critical_boundaries(self) -> tuple[str, ...]:
        checks = {
            "security_baseline": self.security_baseline_ok,
            "agent_permission": self.agent_permission_ok,
            "sandbox_boundary": self.sandbox_boundary_ok,
            "tool_boundary": self.tool_boundary_ok,
            "model_boundary": self.model_boundary_ok,
            "context_boundary": self.context_boundary_ok,
            "output_boundary": self.output_boundary_ok,
            "secrets_policy": self.secrets_policy_ok,
            "prompt_injection_defense": self.prompt_injection_defense_ok,
            "runtime_governance": self.runtime_governance_ok,
            "runtime_state": self.runtime_state_ok,
            "observability": self.observability_ok,
            "runtime_activation_gate": self.runtime_activation_gate_ok,
            "master_user_panel_separation": self.master_user_panel_separation_ok,
            "ui_safe_visibility": self.ui_safe_visibility_ok,
        }
        return tuple(name for name, ok in checks.items() if not ok)


@dataclass(frozen=True)
class RuntimeExecutionPreparationPackageCore:
    package_id: str
    preparation_id: str
    intent_ref: str
    attempt_ref: str | None
    runtime_governance_ref: str
    runtime_state_ref: str
    observability_ref: str
    runtime_activation_gate_ref: str
    security_baseline_ref: str
    agent_permission_ref: str
    sandbox_boundary_ref: str
    tool_boundary_ref: str
    model_boundary_ref: str
    context_boundary_ref: str
    output_boundary_ref: str
    secrets_policy_ref: str
    prompt_injection_defense_ref: str
    human_approval_ref: str | None
    kill_switch_ref: str | None
    rollback_ref: str | None
    dry_run_ref: str | None
    execution_scope: str
    execution_mode: RuntimeExecutionPreparationPackageMode
    execution_risk_level: RuntimeExecutionPreparationPackageRiskLevel
    required_dependencies: tuple[str, ...]
    optional_dependencies: tuple[str, ...]
    missing_required_dependencies: tuple[str, ...]
    missing_optional_dependencies: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    forbidden_readiness: tuple[str, ...]
    metadata: RuntimeExecutionPreparationPackageMetadata
    package_status: RuntimeExecutionPreparationPackageStatus | str
    package_readiness: RuntimeExecutionPreparationPackageReadiness | str
    prepared_snapshot: RuntimeExecutionPreparationPackageBoundarySet
    serialization_version: str


@dataclass(frozen=True)
class RuntimeExecutionPreparationPackageValidationResult:
    is_valid: bool
    status: RuntimeExecutionPreparationPackageStatus
    readiness: RuntimeExecutionPreparationPackageReadiness | str
    missing_required_dependencies: tuple[str, ...]
    missing_optional_dependencies: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    forbidden_readiness_detected: tuple[str, ...]
    forbidden_status_detected: tuple[str, ...]
    metadata_blocked_keys: tuple[str, ...]
    policy_violations: tuple[str, ...]
    boundary_violations: tuple[str, ...]
    ui_visibility_violations: tuple[str, ...]
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeExecutionPreparationPackageDecisionRecord:
    decision: RuntimeExecutionPreparationPackageDecision
    allowed: bool
    simulated_package_allowed: bool
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
    ui_device_allowed: bool
    integrations_allowed: bool
    reason: str
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeExecutionPreparationPackageSnapshot:
    package_id: str
    status: RuntimeExecutionPreparationPackageStatus | str
    readiness: RuntimeExecutionPreparationPackageReadiness | str
    dependency_set: RuntimeExecutionPreparationPackageDependencySet
    boundary_set: RuntimeExecutionPreparationPackageBoundarySet
    metadata: RuntimeExecutionPreparationPackageMetadata
    serialization_version: str


@dataclass(frozen=True)
class RuntimeExecutionPreparationPackageSafeView:
    package_id: str
    preparation_id: str
    status: str
    readiness: str
    risk_level: str
    execution_scope: str
    execution_mode: str
    missing_required_dependencies: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    warnings: tuple[str, ...]
    summary: str
    visibility: RuntimeExecutionPreparationPackageVisibility


@dataclass(frozen=True)
class RuntimeExecutionPreparationPackageContractSnapshot:
    contract_status: str
    policy: RuntimeExecutionPreparationPackagePolicy
    allowed_statuses: tuple[str, ...]
    forbidden_statuses: tuple[str, ...]
    allowed_readiness: tuple[str, ...]
    forbidden_readiness: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    forbidden_metadata_keys: tuple[str, ...]
    package: RuntimeExecutionPreparationPackageCore | None
    validation: RuntimeExecutionPreparationPackageValidationResult | None
    decision: RuntimeExecutionPreparationPackageDecisionRecord | None
    safe_view: RuntimeExecutionPreparationPackageSafeView | None
    parent_contract_ref: str


def build_runtime_execution_preparation_package_policy() -> RuntimeExecutionPreparationPackagePolicy:
    return RuntimeExecutionPreparationPackagePolicy()


def sanitize_runtime_execution_preparation_package_metadata(
    raw_metadata: Mapping[str, Any] | None,
) -> RuntimeExecutionPreparationPackageMetadata:
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
    return RuntimeExecutionPreparationPackageMetadata(
        package_reason=str(sanitized.get("package_reason", "")),
        package_scope=str(sanitized.get("package_scope", "")),
        package_mode=str(sanitized.get("package_mode", "")),
        package_risk_level=str(sanitized.get("package_risk_level", "")),
        created_by=str(sanitized.get("created_by", "")),
        source=str(sanitized.get("source", "")),
        tags=_to_tuple_of_strings(sanitized.get("tags", ())),
        notes=_to_tuple_of_strings(sanitized.get("notes", ())),
        business_context_ref=str(sanitized.get("business_context_ref", "")),
        domain_ref=str(sanitized.get("domain_ref", "")),
        agent_ref=str(sanitized.get("agent_ref", "")),
        blocked_keys=tuple(blocked),
    )


def build_runtime_execution_preparation_package_dependency_set(
    *,
    preparation_id: str,
    intent_ref: str,
    runtime_governance_ref: str,
    runtime_state_ref: str,
    observability_ref: str,
    runtime_activation_gate_ref: str,
    security_baseline_ref: str,
    agent_permission_ref: str,
    sandbox_boundary_ref: str,
    tool_boundary_ref: str,
    model_boundary_ref: str,
    context_boundary_ref: str,
    output_boundary_ref: str,
    secrets_policy_ref: str,
    prompt_injection_defense_ref: str,
    attempt_ref: str | None = None,
    human_approval_ref: str | None = None,
    kill_switch_ref: str | None = None,
    rollback_ref: str | None = None,
    dry_run_ref: str | None = None,
) -> RuntimeExecutionPreparationPackageDependencySet:
    return RuntimeExecutionPreparationPackageDependencySet(
        preparation_id=_clean_ref(preparation_id),
        intent_ref=_clean_ref(intent_ref),
        attempt_ref=_clean_optional_ref(attempt_ref),
        runtime_governance_ref=_clean_ref(runtime_governance_ref),
        runtime_state_ref=_clean_ref(runtime_state_ref),
        observability_ref=_clean_ref(observability_ref),
        runtime_activation_gate_ref=_clean_ref(runtime_activation_gate_ref),
        security_baseline_ref=_clean_ref(security_baseline_ref),
        agent_permission_ref=_clean_ref(agent_permission_ref),
        sandbox_boundary_ref=_clean_ref(sandbox_boundary_ref),
        tool_boundary_ref=_clean_ref(tool_boundary_ref),
        model_boundary_ref=_clean_ref(model_boundary_ref),
        context_boundary_ref=_clean_ref(context_boundary_ref),
        output_boundary_ref=_clean_ref(output_boundary_ref),
        secrets_policy_ref=_clean_ref(secrets_policy_ref),
        prompt_injection_defense_ref=_clean_ref(prompt_injection_defense_ref),
        human_approval_ref=_clean_optional_ref(human_approval_ref),
        kill_switch_ref=_clean_optional_ref(kill_switch_ref),
        rollback_ref=_clean_optional_ref(rollback_ref),
        dry_run_ref=_clean_optional_ref(dry_run_ref),
    )


def build_runtime_execution_preparation_package_boundary_set(
    *,
    security_baseline_ok: bool,
    agent_permission_ok: bool,
    sandbox_boundary_ok: bool,
    tool_boundary_ok: bool,
    model_boundary_ok: bool,
    context_boundary_ok: bool,
    output_boundary_ok: bool,
    secrets_policy_ok: bool,
    prompt_injection_defense_ok: bool,
    runtime_governance_ok: bool,
    runtime_state_ok: bool,
    observability_ok: bool,
    runtime_activation_gate_ok: bool,
    human_approval_ok: bool = False,
    kill_switch_ok: bool = False,
    rollback_ok: bool = False,
    dry_run_ok: bool = False,
    master_user_panel_separation_ok: bool = True,
    ui_safe_visibility_ok: bool = True,
) -> RuntimeExecutionPreparationPackageBoundarySet:
    return RuntimeExecutionPreparationPackageBoundarySet(
        security_baseline_ok=bool(security_baseline_ok),
        agent_permission_ok=bool(agent_permission_ok),
        sandbox_boundary_ok=bool(sandbox_boundary_ok),
        tool_boundary_ok=bool(tool_boundary_ok),
        model_boundary_ok=bool(model_boundary_ok),
        context_boundary_ok=bool(context_boundary_ok),
        output_boundary_ok=bool(output_boundary_ok),
        secrets_policy_ok=bool(secrets_policy_ok),
        prompt_injection_defense_ok=bool(prompt_injection_defense_ok),
        runtime_governance_ok=bool(runtime_governance_ok),
        runtime_state_ok=bool(runtime_state_ok),
        observability_ok=bool(observability_ok),
        runtime_activation_gate_ok=bool(runtime_activation_gate_ok),
        human_approval_ok=bool(human_approval_ok),
        kill_switch_ok=bool(kill_switch_ok),
        rollback_ok=bool(rollback_ok),
        dry_run_ok=bool(dry_run_ok),
        master_user_panel_separation_ok=bool(master_user_panel_separation_ok),
        ui_safe_visibility_ok=bool(ui_safe_visibility_ok),
    )


def build_runtime_execution_preparation_package(
    *,
    package_id: str,
    dependency_set: RuntimeExecutionPreparationPackageDependencySet,
    boundary_set: RuntimeExecutionPreparationPackageBoundarySet,
    execution_scope: str,
    execution_mode: RuntimeExecutionPreparationPackageMode | str,
    execution_risk_level: RuntimeExecutionPreparationPackageRiskLevel | str,
    metadata: RuntimeExecutionPreparationPackageMetadata | Mapping[str, Any] | None,
    package_status: RuntimeExecutionPreparationPackageStatus | str = (
        RuntimeExecutionPreparationPackageStatus.PACKAGE_READY_SIMULATED
    ),
    package_readiness: RuntimeExecutionPreparationPackageReadiness | str = (
        RuntimeExecutionPreparationPackageReadiness.READY_FOR_RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT
    ),
    blocked_capabilities: tuple[str, ...] | list[str] | None = None,
    forbidden_readiness: tuple[str, ...] | list[str] | None = None,
    serialization_version: str = "runtime_execution_preparation_package.v1",
) -> RuntimeExecutionPreparationPackageCore:
    clean_metadata = (
        metadata
        if isinstance(metadata, RuntimeExecutionPreparationPackageMetadata)
        else sanitize_runtime_execution_preparation_package_metadata(metadata)
    )
    return RuntimeExecutionPreparationPackageCore(
        package_id=_clean_ref(package_id),
        preparation_id=dependency_set.preparation_id,
        intent_ref=dependency_set.intent_ref,
        attempt_ref=dependency_set.attempt_ref,
        runtime_governance_ref=dependency_set.runtime_governance_ref,
        runtime_state_ref=dependency_set.runtime_state_ref,
        observability_ref=dependency_set.observability_ref,
        runtime_activation_gate_ref=dependency_set.runtime_activation_gate_ref,
        security_baseline_ref=dependency_set.security_baseline_ref,
        agent_permission_ref=dependency_set.agent_permission_ref,
        sandbox_boundary_ref=dependency_set.sandbox_boundary_ref,
        tool_boundary_ref=dependency_set.tool_boundary_ref,
        model_boundary_ref=dependency_set.model_boundary_ref,
        context_boundary_ref=dependency_set.context_boundary_ref,
        output_boundary_ref=dependency_set.output_boundary_ref,
        secrets_policy_ref=dependency_set.secrets_policy_ref,
        prompt_injection_defense_ref=dependency_set.prompt_injection_defense_ref,
        human_approval_ref=dependency_set.human_approval_ref,
        kill_switch_ref=dependency_set.kill_switch_ref,
        rollback_ref=dependency_set.rollback_ref,
        dry_run_ref=dependency_set.dry_run_ref,
        execution_scope=_clean_ref(execution_scope),
        execution_mode=_coerce_mode(execution_mode),
        execution_risk_level=_coerce_risk_level(execution_risk_level),
        required_dependencies=dependency_set.required_dependencies(),
        optional_dependencies=dependency_set.optional_dependencies(),
        missing_required_dependencies=dependency_set.missing_required_dependencies(),
        missing_optional_dependencies=dependency_set.missing_optional_dependencies(),
        blocked_capabilities=_to_tuple_of_strings(blocked_capabilities or BLOCKED_CAPABILITIES),
        forbidden_readiness=_to_tuple_of_strings(forbidden_readiness or FORBIDDEN_READINESS),
        metadata=clean_metadata,
        package_status=_coerce_status(package_status),
        package_readiness=package_readiness,
        prepared_snapshot=boundary_set,
        serialization_version=_clean_ref(serialization_version),
    )


def validate_runtime_execution_preparation_package_contract(
    package: RuntimeExecutionPreparationPackageCore,
    policy: RuntimeExecutionPreparationPackagePolicy | None = None,
    boundaries: RuntimeExecutionPreparationPackageBoundarySet | None = None,
) -> RuntimeExecutionPreparationPackageValidationResult:
    resolved_policy = policy or build_runtime_execution_preparation_package_policy()
    resolved_boundaries = boundaries or package.prepared_snapshot
    errors: list[str] = []
    warnings: list[str] = []
    policy_violations: list[str] = []
    boundary_violations = list(resolved_boundaries.missing_critical_boundaries())
    ui_visibility_violations: list[str] = []
    if not package.package_id:
        errors.append("missing_required_ref:package_id")
    dependency_set = _dependency_set_from_package(package)
    missing_required = list(dependency_set.missing_required_dependencies())
    missing_optional = list(dependency_set.missing_optional_dependencies())
    for missing in missing_required:
        errors.append(f"missing_required_ref:{missing}")
    for missing in missing_optional:
        warnings.append(f"missing_optional_ref:{missing}")
    for boundary in boundary_violations:
        errors.append(f"missing_boundary:{boundary}")
    if not resolved_boundaries.master_user_panel_separation_ok:
        ui_visibility_violations.append("master_user_panel_separation_violated")
    if not resolved_boundaries.ui_safe_visibility_ok:
        ui_visibility_violations.append("ui_safe_visibility_violated")
    if ui_visibility_violations:
        errors.extend(ui_visibility_violations)
    forbidden_readiness_detected = _forbidden_readiness_detected(
        package.package_readiness,
        package.forbidden_readiness,
    )
    for readiness in forbidden_readiness_detected:
        errors.append(f"forbidden_readiness:{readiness}")
    status_value = _enum_or_string(package.package_status)
    forbidden_status_detected = (status_value,) if status_value in FORBIDDEN_STATUSES else ()
    for status in forbidden_status_detected:
        errors.append(f"forbidden_status:{status}")
    if not forbidden_status_detected and status_value not in ALLOWED_STATUSES:
        errors.append(f"status_not_allowed:{status_value}")
    if package.metadata.blocked_keys:
        errors.append("dangerous_metadata_detected")
    if tuple(package.blocked_capabilities) != BLOCKED_CAPABILITIES:
        errors.append("blocked_capabilities_must_match_default_deny")
    for capability in package.blocked_capabilities:
        if capability not in BLOCKED_CAPABILITIES:
            errors.append(f"unknown_or_enabled_capability:{capability}")
    if not resolved_policy.contract_ready:
        policy_violations.append("policy_contract_ready_false")
    for field_name, value in asdict(resolved_policy).items():
        if field_name != "contract_ready" and value is True:
            policy_violations.append(f"operational_policy_flag_enabled:{field_name}")
    errors.extend(policy_violations)
    try:
        json.dumps(runtime_execution_preparation_package_to_dict(package), sort_keys=True)
    except (TypeError, ValueError):
        errors.append("package_not_json_safe")
    if errors:
        status = RuntimeExecutionPreparationPackageStatus.PACKAGE_INVALID
    elif missing_required:
        status = RuntimeExecutionPreparationPackageStatus.PACKAGE_DEPENDENCIES_REQUIRED
    elif boundary_violations:
        status = RuntimeExecutionPreparationPackageStatus.PACKAGE_BOUNDARIES_REQUIRED
    else:
        status = RuntimeExecutionPreparationPackageStatus.PACKAGE_READY_SIMULATED
    return RuntimeExecutionPreparationPackageValidationResult(
        is_valid=not errors and not missing_required,
        status=status,
        readiness=package.package_readiness,
        missing_required_dependencies=tuple(dict.fromkeys(missing_required)),
        missing_optional_dependencies=tuple(dict.fromkeys(missing_optional)),
        blocked_capabilities=tuple(package.blocked_capabilities),
        forbidden_readiness_detected=forbidden_readiness_detected,
        forbidden_status_detected=forbidden_status_detected,
        metadata_blocked_keys=package.metadata.blocked_keys,
        policy_violations=tuple(dict.fromkeys(policy_violations)),
        boundary_violations=tuple(dict.fromkeys(boundary_violations)),
        ui_visibility_violations=tuple(dict.fromkeys(ui_visibility_violations)),
        errors=tuple(dict.fromkeys(errors)),
        warnings=tuple(dict.fromkeys(warnings)),
    )


def decide_runtime_execution_preparation_package(
    validation_result: RuntimeExecutionPreparationPackageValidationResult,
    policy: RuntimeExecutionPreparationPackagePolicy | None = None,
) -> RuntimeExecutionPreparationPackageDecisionRecord:
    resolved_policy = policy or build_runtime_execution_preparation_package_policy()
    if any(value is True for key, value in asdict(resolved_policy).items() if key != "contract_ready"):
        decision = RuntimeExecutionPreparationPackageDecision.REQUIRE_POLICY_DEFAULT_DENY
        allowed = False
        reason = "policy_not_default_deny"
    elif validation_result.policy_violations:
        decision = RuntimeExecutionPreparationPackageDecision.REQUIRE_POLICY_DEFAULT_DENY
        allowed = False
        reason = "policy_violations"
    elif validation_result.metadata_blocked_keys:
        decision = RuntimeExecutionPreparationPackageDecision.REQUIRE_METADATA_SANITIZATION
        allowed = False
        reason = "metadata_blocked"
    elif validation_result.ui_visibility_violations:
        decision = RuntimeExecutionPreparationPackageDecision.REQUIRE_UI_SAFE_VIEW
        allowed = False
        reason = "ui_visibility_violations"
    elif validation_result.boundary_violations:
        decision = RuntimeExecutionPreparationPackageDecision.REQUIRE_BOUNDARIES
        allowed = False
        reason = "boundary_violations"
    elif validation_result.missing_required_dependencies:
        decision = RuntimeExecutionPreparationPackageDecision.REQUIRE_DEPENDENCIES
        allowed = False
        reason = "missing_required_dependencies"
    elif validation_result.errors:
        decision = RuntimeExecutionPreparationPackageDecision.INVALID
        allowed = False
        reason = "validation_errors"
    elif validation_result.is_valid:
        decision = RuntimeExecutionPreparationPackageDecision.ALLOW_SIMULATED_PACKAGE
        allowed = True
        reason = "simulated_package_only"
    else:
        decision = RuntimeExecutionPreparationPackageDecision.BLOCK_PACKAGE
        allowed = False
        reason = "blocked"
    return RuntimeExecutionPreparationPackageDecisionRecord(
        decision=decision,
        allowed=allowed,
        simulated_package_allowed=allowed
        and decision == RuntimeExecutionPreparationPackageDecision.ALLOW_SIMULATED_PACKAGE,
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
        ui_device_allowed=False,
        integrations_allowed=False,
        reason=reason,
        errors=validation_result.errors,
        warnings=validation_result.warnings,
    )


def build_runtime_execution_preparation_package_safe_view(
    package: RuntimeExecutionPreparationPackageCore,
    validation_result: RuntimeExecutionPreparationPackageValidationResult,
    visibility: RuntimeExecutionPreparationPackageVisibility | str,
) -> RuntimeExecutionPreparationPackageSafeView:
    resolved_visibility = _coerce_visibility(visibility)
    warnings = validation_result.warnings
    if resolved_visibility == RuntimeExecutionPreparationPackageVisibility.USER_PANEL_SAFE:
        warnings = tuple(dict.fromkeys((*warnings, "user_panel_view_reduced")))
    if resolved_visibility == RuntimeExecutionPreparationPackageVisibility.BLOCKED:
        summary = "Package visibility blocked."
    else:
        summary = "Runtime Execution Preparation Package is conceptual and non-operational."
    return RuntimeExecutionPreparationPackageSafeView(
        package_id=package.package_id,
        preparation_id=package.preparation_id,
        status=_enum_or_string(validation_result.status),
        readiness=_enum_or_string(validation_result.readiness),
        risk_level=package.execution_risk_level.value,
        execution_scope=package.execution_scope,
        execution_mode=package.execution_mode.value,
        missing_required_dependencies=validation_result.missing_required_dependencies,
        blocked_capabilities=package.blocked_capabilities,
        warnings=warnings,
        summary=summary,
        visibility=resolved_visibility,
    )


def runtime_execution_preparation_package_to_dict(value: Any) -> Any:
    return _to_json_safe(value)


def build_runtime_execution_preparation_package_contract_snapshot(
    *,
    package: RuntimeExecutionPreparationPackageCore | None = None,
    validation: RuntimeExecutionPreparationPackageValidationResult | None = None,
    decision: RuntimeExecutionPreparationPackageDecisionRecord | None = None,
    safe_view: RuntimeExecutionPreparationPackageSafeView | None = None,
    policy: RuntimeExecutionPreparationPackagePolicy | None = None,
) -> RuntimeExecutionPreparationPackageContractSnapshot:
    return RuntimeExecutionPreparationPackageContractSnapshot(
        contract_status=CONTRACT_STATUS,
        policy=policy or build_runtime_execution_preparation_package_policy(),
        allowed_statuses=ALLOWED_STATUSES,
        forbidden_statuses=FORBIDDEN_STATUSES,
        allowed_readiness=ALLOWED_READINESS,
        forbidden_readiness=FORBIDDEN_READINESS,
        blocked_capabilities=BLOCKED_CAPABILITIES,
        forbidden_metadata_keys=FORBIDDEN_METADATA_KEYS,
        package=package,
        validation=validation,
        decision=decision,
        safe_view=safe_view,
        parent_contract_ref=PARENT_CONTRACT_REF,
    )


def get_runtime_execution_preparation_package_contract_status() -> dict[str, Any]:
    return {
        "contract_status": CONTRACT_STATUS,
        "verdict": CONTRACT_VERDICT,
        "readiness": CONTRACT_READINESS,
        "next_step": CONTRACT_NEXT_STEP,
        "parent_contract_ref": PARENT_CONTRACT_REF,
        "parent_contract_ready": parent_contract.RUNTIME_EXECUTION_PREPARATION_CONTRACT_READY,
        "contract_ready": RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_READY,
        "package_operational": RUNTIME_EXECUTION_PREPARATION_PACKAGE_OPERATIONAL,
        "runtime_active": RUNTIME_EXECUTION_PREPARATION_PACKAGE_RUNTIME_ACTIVE,
        "execution_active": RUNTIME_EXECUTION_PREPARATION_PACKAGE_EXECUTION_ACTIVE,
        "dry_run_active": RUNTIME_EXECUTION_PREPARATION_PACKAGE_DRY_RUN_ACTIVE,
        "tools_enabled": RUNTIME_EXECUTION_PREPARATION_PACKAGE_TOOLS_ENABLED,
        "models_enabled": RUNTIME_EXECUTION_PREPARATION_PACKAGE_MODELS_ENABLED,
        "context_enabled": RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTEXT_ENABLED,
        "output_enabled": RUNTIME_EXECUTION_PREPARATION_PACKAGE_OUTPUT_ENABLED,
        "writes_enabled": RUNTIME_EXECUTION_PREPARATION_PACKAGE_WRITES_ENABLED,
        "stores_enabled": RUNTIME_EXECUTION_PREPARATION_PACKAGE_STORES_ENABLED,
        "memory_enabled": RUNTIME_EXECUTION_PREPARATION_PACKAGE_MEMORY_ENABLED,
        "network_enabled": RUNTIME_EXECUTION_PREPARATION_PACKAGE_NETWORK_ENABLED,
        "browser_enabled": RUNTIME_EXECUTION_PREPARATION_PACKAGE_BROWSER_ENABLED,
        "filesystem_enabled": RUNTIME_EXECUTION_PREPARATION_PACKAGE_FILESYSTEM_ENABLED,
        "env_enabled": RUNTIME_EXECUTION_PREPARATION_PACKAGE_ENV_ENABLED,
        "secrets_enabled": RUNTIME_EXECUTION_PREPARATION_PACKAGE_SECRETS_ENABLED,
        "ui_device_enabled": RUNTIME_EXECUTION_PREPARATION_PACKAGE_UI_DEVICE_ENABLED,
        "integrations_enabled": RUNTIME_EXECUTION_PREPARATION_PACKAGE_INTEGRATIONS_ENABLED,
        "excluded_external_concepts": tuple(sorted(EXCLUDED_EXTERNAL_CONCEPTS)),
    }


def _dependency_set_from_package(package: RuntimeExecutionPreparationPackageCore) -> RuntimeExecutionPreparationPackageDependencySet:
    return RuntimeExecutionPreparationPackageDependencySet(
        preparation_id=package.preparation_id,
        intent_ref=package.intent_ref,
        attempt_ref=package.attempt_ref,
        runtime_governance_ref=package.runtime_governance_ref,
        runtime_state_ref=package.runtime_state_ref,
        observability_ref=package.observability_ref,
        runtime_activation_gate_ref=package.runtime_activation_gate_ref,
        security_baseline_ref=package.security_baseline_ref,
        agent_permission_ref=package.agent_permission_ref,
        sandbox_boundary_ref=package.sandbox_boundary_ref,
        tool_boundary_ref=package.tool_boundary_ref,
        model_boundary_ref=package.model_boundary_ref,
        context_boundary_ref=package.context_boundary_ref,
        output_boundary_ref=package.output_boundary_ref,
        secrets_policy_ref=package.secrets_policy_ref,
        prompt_injection_defense_ref=package.prompt_injection_defense_ref,
        human_approval_ref=package.human_approval_ref,
        kill_switch_ref=package.kill_switch_ref,
        rollback_ref=package.rollback_ref,
        dry_run_ref=package.dry_run_ref,
    )


def _is_forbidden_metadata_key(normalized_key: str) -> bool:
    return any(fragment in normalized_key for fragment in FORBIDDEN_METADATA_KEYS)


def _forbidden_readiness_detected(readiness: RuntimeExecutionPreparationPackageReadiness | str, forbidden: tuple[str, ...]) -> tuple[str, ...]:
    value = _enum_or_string(readiness)
    detected = [value] if value in forbidden or value in FORBIDDEN_READINESS else []
    return tuple(detected)


def _coerce_status(value: RuntimeExecutionPreparationPackageStatus | str) -> RuntimeExecutionPreparationPackageStatus:
    if isinstance(value, RuntimeExecutionPreparationPackageStatus):
        return value
    return RuntimeExecutionPreparationPackageStatus(str(value))


def _coerce_mode(value: RuntimeExecutionPreparationPackageMode | str) -> RuntimeExecutionPreparationPackageMode:
    if isinstance(value, RuntimeExecutionPreparationPackageMode):
        return value
    return RuntimeExecutionPreparationPackageMode(str(value))


def _coerce_risk_level(value: RuntimeExecutionPreparationPackageRiskLevel | str) -> RuntimeExecutionPreparationPackageRiskLevel:
    if isinstance(value, RuntimeExecutionPreparationPackageRiskLevel):
        return value
    return RuntimeExecutionPreparationPackageRiskLevel(str(value))


def _coerce_visibility(value: RuntimeExecutionPreparationPackageVisibility | str) -> RuntimeExecutionPreparationPackageVisibility:
    if isinstance(value, RuntimeExecutionPreparationPackageVisibility):
        return value
    return RuntimeExecutionPreparationPackageVisibility(str(value))


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
