"""Non-operational Runtime Execution Preparation contract.

This contract-only module models a future execution preparation package as deterministic,
JSON-safe data only. It never executes runtime, dry-runs, tools, models,
context injection, output delivery, writes, stores, memory, network, browser,
filesystem, env, secrets, integrations, or OBLITERATUS.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
import json
from typing import Any, Mapping


RUNTIME_EXECUTION_PREPARATION_CONTRACT_READY = True
RUNTIME_EXECUTION_PREPARATION_OPERATIONAL = False
RUNTIME_EXECUTION_PREPARATION_RUNTIME_ACTIVE = False
RUNTIME_EXECUTION_PREPARATION_EXECUTION_ACTIVE = False
RUNTIME_EXECUTION_PREPARATION_DRY_RUN_ACTIVE = False
RUNTIME_EXECUTION_PREPARATION_TOOLS_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_MODELS_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_CONTEXT_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_OUTPUT_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_WRITES_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_STORES_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_MEMORY_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_NETWORK_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_BROWSER_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_FILESYSTEM_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_ENV_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_SECRETS_ENABLED = False
RUNTIME_EXECUTION_PREPARATION_INTEGRATIONS_ENABLED = False

CONTRACT_STATUS = "RUNTIME_EXECUTION_PREPARATION_CONTRACT_READY"
CONTRACT_VERDICT = "RUNTIME_EXECUTION_PREPARATION_NO_OPERATIONAL_CONFIRMED"
CONTRACT_READINESS = "ready_for_runtime_execution_preparation_contract_e2e"
CONTRACT_NEXT_STEP = "PROMPT 4.1.1 — Checkpoint E2E Runtime Execution Preparation Contract"

EXCLUDED_EXTERNAL_CONCEPTS = frozenset({"OBLITERATUS"})
OBLITERATUS_EXCLUSION_STATEMENTS = (
    "OBLITERATUS is excluded from Runtime Execution Preparation.",
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
)


class RuntimeExecutionPreparationStatus(str, Enum):
    UNINITIALIZED = "runtime_execution_preparation_uninitialized"
    GOVERNANCE_REQUIRED = "runtime_execution_preparation_governance_required"
    STATE_REQUIRED = "runtime_execution_preparation_state_required"
    OBSERVABILITY_REQUIRED = "runtime_execution_preparation_observability_required"
    SECURITY_REQUIRED = "runtime_execution_preparation_security_required"
    INTENT_REQUIRED = "runtime_execution_preparation_intent_required"
    ATTEMPT_REQUIRED = "runtime_execution_preparation_attempt_required"
    BOUNDARIES_REQUIRED = "runtime_execution_preparation_boundaries_required"
    HUMAN_APPROVAL_REQUIRED = "runtime_execution_preparation_human_approval_required"
    KILL_SWITCH_REQUIRED = "runtime_execution_preparation_kill_switch_required"
    ROLLBACK_REQUIRED = "runtime_execution_preparation_rollback_required"
    DRY_RUN_REQUIRED = "runtime_execution_preparation_dry_run_required"
    READY_SIMULATED = "runtime_execution_preparation_ready_simulated"
    BLOCKED = "runtime_execution_preparation_blocked"
    INVALID = "runtime_execution_preparation_invalid"
    ARCHIVED_SIMULATED = "runtime_execution_preparation_archived_simulated"


class RuntimeExecutionPreparationReadiness(str, Enum):
    READY_FOR_RUNTIME_EXECUTION_PREPARATION_CONTRACT = "ready_for_runtime_execution_preparation_contract"
    READY_FOR_RUNTIME_EXECUTION_PREPARATION_CONTRACT_E2E = "ready_for_runtime_execution_preparation_contract_e2e"


class RuntimeExecutionPreparationRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RuntimeExecutionPreparationMode(str, Enum):
    CONTRACT_ONLY = "contract_only"
    SIMULATED_PREPARATION = "simulated_preparation"
    VALIDATION_ONLY = "validation_only"
    SNAPSHOT_ONLY = "snapshot_only"


class RuntimeExecutionPreparationDecision(str, Enum):
    ALLOW_SIMULATED_PREPARATION = "allow_simulated_preparation"
    BLOCK_PREPARATION = "block_preparation"
    REQUIRE_DEPENDENCIES = "require_dependencies"
    REQUIRE_HUMAN_APPROVAL = "require_human_approval"
    REQUIRE_DRY_RUN = "require_dry_run"
    INVALID = "invalid"


class RuntimeExecutionPreparationBlockReason(str, Enum):
    MISSING_DEPENDENCY = "missing_dependency"
    MISSING_INTENT = "missing_intent"
    MISSING_BOUNDARY = "missing_boundary"
    FORBIDDEN_READINESS = "forbidden_readiness"
    FORBIDDEN_STATUS = "forbidden_status"
    OPERATIONAL_CAPABILITY_REQUESTED = "operational_capability_requested"
    OPERATIONAL_POLICY_FLAG = "operational_policy_flag"
    DANGEROUS_METADATA = "dangerous_metadata"
    METADATA_NOT_JSON_SAFE = "metadata_not_json_safe"
    OBLITERATUS_EXCLUDED = "obliteratus_excluded"


class RuntimeExecutionPreparationDependencyKind(str, Enum):
    SECURITY_BASELINE = "security_baseline"
    EXECUTION_INTENT = "execution_intent"
    ATTEMPT_REFERENCE = "attempt_reference"
    RUNTIME_GOVERNANCE = "runtime_governance"
    RUNTIME_STATE = "runtime_state"
    OBSERVABILITY = "observability"
    RUNTIME_ACTIVATION_GATE = "runtime_activation_gate"
    AGENT_PERMISSION = "agent_permission"
    SANDBOX_BOUNDARY = "sandbox_boundary"
    TOOL_BOUNDARY = "tool_boundary"
    MODEL_BOUNDARY = "model_boundary"
    CONTEXT_BOUNDARY = "context_boundary"
    OUTPUT_BOUNDARY = "output_boundary"
    SECRETS_POLICY = "secrets_policy"
    PROMPT_INJECTION_DEFENSE = "prompt_injection_defense"
    HUMAN_APPROVAL = "human_approval"
    KILL_SWITCH = "kill_switch"
    ROLLBACK = "rollback"
    DRY_RUN = "dry_run"


class RuntimeExecutionPreparationCapability(str, Enum):
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


ALLOWED_STATUSES = tuple(status.value for status in RuntimeExecutionPreparationStatus)
FORBIDDEN_STATUSES = (
    "runtime_execution_preparation_active",
    "runtime_execution_preparation_running",
    "runtime_execution_preparation_executing",
    "runtime_execution_preparation_live",
    "runtime_execution_preparation_open",
    "runtime_execution_preparation_enabled",
    "runtime_execution_preparation_operational",
    "runtime_execution_preparation_runtime_started",
    "runtime_execution_preparation_dry_run_started",
    "runtime_execution_preparation_tool_executing",
    "runtime_execution_preparation_model_invoking",
    "runtime_execution_preparation_context_injecting",
    "runtime_execution_preparation_output_delivering",
    "runtime_execution_preparation_writing",
    "runtime_execution_preparation_store_mutating",
    "runtime_execution_preparation_network_active",
    "runtime_execution_preparation_api_active",
    "runtime_execution_preparation_browser_active",
    "runtime_execution_preparation_filesystem_active",
    "runtime_execution_preparation_env_active",
    "runtime_execution_preparation_secret_active",
    "runtime_execution_preparation_integration_active",
)
ALLOWED_READINESS = tuple(readiness.value for readiness in RuntimeExecutionPreparationReadiness)
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
    "gate_open",
    "approval_enabled",
    "human_approval_operational",
    "kill_switch_enabled",
    "rollback_enabled",
    "observability_runtime_enabled",
    "runtime_execution_enabled",
    "runtime_execution_preparation_operational",
)
BLOCKED_CAPABILITIES = tuple(capability.value for capability in RuntimeExecutionPreparationCapability)
FORBIDDEN_METADATA_KEYS = (
    "secret",
    "secrets",
    "api_key",
    "apikey",
    "token",
    "access_token",
    "refresh_token",
    "password",
    "passwd",
    "credential",
    "credentials",
    "private_key",
    "raw_payload",
    "payload",
    "raw_output",
    "output",
    "file_content",
    "env",
    "environment",
    "cookie",
    "authorization",
    "bearer",
    "raw_prompt",
    "prompt",
    "raw_completion",
    "completion",
    "model_response",
    "tool_response",
    "external_response",
    "browser_content",
    "filesystem_content",
    "personal_data_unsanitized",
)
SAFE_METADATA_KEYS = (
    "preparation_reason",
    "preparation_scope",
    "preparation_mode",
    "preparation_risk_level",
    "created_by",
    "source",
    "tags",
    "notes",
)
REQUIRED_REF_FIELDS = (
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
OPTIONAL_REF_FIELDS = (
    "attempt_ref",
    "human_approval_ref",
    "kill_switch_ref",
    "rollback_ref",
    "dry_run_ref",
)


@dataclass(frozen=True)
class RuntimeExecutionPreparationPolicy:
    contract_ready: bool = True
    operational_enabled: bool = False
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
    integrations_enabled: bool = False
    automatic_approval_enabled: bool = False
    kill_switch_operational_enabled: bool = False
    rollback_operational_enabled: bool = False


@dataclass(frozen=True)
class RuntimeExecutionPreparationMetadata:
    preparation_reason: str = ""
    preparation_scope: str = ""
    preparation_mode: str = ""
    preparation_risk_level: str = ""
    created_by: str = ""
    source: str = ""
    tags: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    blocked_keys: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuntimeExecutionPreparationDependency:
    kind: RuntimeExecutionPreparationDependencyKind
    ref: str
    required: bool = True
    present: bool = True
    status: str = "present"
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuntimeExecutionPreparationBoundarySnapshot:
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

    def missing_required(self) -> tuple[str, ...]:
        required_checks = {
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
        }
        return tuple(name for name, ok in required_checks.items() if not ok)

    def missing_optional(self) -> tuple[str, ...]:
        optional_checks = {
            "human_approval": self.human_approval_ok,
            "kill_switch": self.kill_switch_ok,
            "rollback": self.rollback_ok,
            "dry_run": self.dry_run_ok,
        }
        return tuple(name for name, ok in optional_checks.items() if not ok)


@dataclass(frozen=True)
class RuntimeExecutionPreparationPackage:
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
    execution_mode: RuntimeExecutionPreparationMode
    execution_risk_level: RuntimeExecutionPreparationRiskLevel
    required_dependencies: tuple[RuntimeExecutionPreparationDependency, ...]
    missing_dependencies: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    forbidden_readiness: tuple[str, ...]
    metadata: RuntimeExecutionPreparationMetadata
    prepared_snapshot: RuntimeExecutionPreparationBoundarySnapshot
    status: RuntimeExecutionPreparationStatus
    readiness: RuntimeExecutionPreparationReadiness | str


@dataclass(frozen=True)
class RuntimeExecutionPreparationValidationResult:
    is_valid: bool
    status: RuntimeExecutionPreparationStatus
    readiness: RuntimeExecutionPreparationReadiness | str
    missing_dependencies: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    forbidden_readiness_detected: tuple[str, ...]
    metadata_blocked_keys: tuple[str, ...]
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeExecutionPreparationDecisionRecord:
    decision: RuntimeExecutionPreparationDecision
    allowed: bool
    simulated_preparation_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    dry_run_execution_allowed: bool
    tool_execution_allowed: bool
    model_invocation_allowed: bool
    context_injection_allowed: bool
    output_delivery_allowed: bool
    writes_allowed: bool
    stores_allowed: bool
    reason: str
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeExecutionPreparationContractSnapshot:
    contract_status: str
    policy: RuntimeExecutionPreparationPolicy
    allowed_statuses: tuple[str, ...]
    forbidden_statuses: tuple[str, ...]
    allowed_readiness: tuple[str, ...]
    forbidden_readiness: tuple[str, ...]
    blocked_capabilities: tuple[str, ...]
    forbidden_metadata_keys: tuple[str, ...]
    dependencies: tuple[RuntimeExecutionPreparationDependency, ...]
    package: RuntimeExecutionPreparationPackage | None
    validation: RuntimeExecutionPreparationValidationResult | None
    decision: RuntimeExecutionPreparationDecisionRecord | None


def build_runtime_execution_preparation_policy() -> RuntimeExecutionPreparationPolicy:
    return RuntimeExecutionPreparationPolicy()


def sanitize_runtime_execution_preparation_metadata(
    raw_metadata: Mapping[str, Any] | None,
) -> RuntimeExecutionPreparationMetadata:
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
    return RuntimeExecutionPreparationMetadata(
        preparation_reason=str(sanitized.get("preparation_reason", "")),
        preparation_scope=str(sanitized.get("preparation_scope", "")),
        preparation_mode=str(sanitized.get("preparation_mode", "")),
        preparation_risk_level=str(sanitized.get("preparation_risk_level", "")),
        created_by=str(sanitized.get("created_by", "")),
        source=str(sanitized.get("source", "")),
        tags=_to_tuple_of_strings(sanitized.get("tags", ())),
        notes=_to_tuple_of_strings(sanitized.get("notes", ())),
        blocked_keys=tuple(blocked),
    )


def build_runtime_execution_preparation_dependency(
    *,
    kind: RuntimeExecutionPreparationDependencyKind | str,
    ref: str | None,
    required: bool = True,
    present: bool | None = None,
    status: str | None = None,
    notes: tuple[str, ...] | list[str] = (),
) -> RuntimeExecutionPreparationDependency:
    dependency_kind = _coerce_dependency_kind(kind)
    clean_ref = str(ref or "").strip()
    resolved_present = bool(clean_ref) if present is None else bool(present)
    resolved_status = status or ("present" if resolved_present else "missing")
    return RuntimeExecutionPreparationDependency(
        kind=dependency_kind,
        ref=clean_ref,
        required=bool(required),
        present=resolved_present,
        status=str(resolved_status),
        notes=_to_tuple_of_strings(notes),
    )


def build_runtime_execution_preparation_boundary_snapshot(
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
) -> RuntimeExecutionPreparationBoundarySnapshot:
    return RuntimeExecutionPreparationBoundarySnapshot(
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
    )


def build_runtime_execution_preparation_package(
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
    execution_scope: str,
    execution_mode: RuntimeExecutionPreparationMode | str,
    execution_risk_level: RuntimeExecutionPreparationRiskLevel | str,
    metadata: RuntimeExecutionPreparationMetadata | Mapping[str, Any] | None,
    prepared_snapshot: RuntimeExecutionPreparationBoundarySnapshot,
    attempt_ref: str | None = None,
    human_approval_ref: str | None = None,
    kill_switch_ref: str | None = None,
    rollback_ref: str | None = None,
    dry_run_ref: str | None = None,
    required_dependencies: tuple[RuntimeExecutionPreparationDependency, ...] | list[RuntimeExecutionPreparationDependency] | None = None,
    missing_dependencies: tuple[str, ...] | list[str] | None = None,
    blocked_capabilities: tuple[str, ...] | list[str] | None = None,
    forbidden_readiness: tuple[str, ...] | list[str] | None = None,
    status: RuntimeExecutionPreparationStatus | str = RuntimeExecutionPreparationStatus.READY_SIMULATED,
    readiness: RuntimeExecutionPreparationReadiness | str = RuntimeExecutionPreparationReadiness.READY_FOR_RUNTIME_EXECUTION_PREPARATION_CONTRACT,
) -> RuntimeExecutionPreparationPackage:
    clean_metadata = (
        metadata
        if isinstance(metadata, RuntimeExecutionPreparationMetadata)
        else sanitize_runtime_execution_preparation_metadata(metadata)
    )
    dependencies = tuple(required_dependencies) if required_dependencies is not None else _default_dependencies(
        intent_ref=intent_ref,
        attempt_ref=attempt_ref,
        runtime_governance_ref=runtime_governance_ref,
        runtime_state_ref=runtime_state_ref,
        observability_ref=observability_ref,
        runtime_activation_gate_ref=runtime_activation_gate_ref,
        security_baseline_ref=security_baseline_ref,
        agent_permission_ref=agent_permission_ref,
        sandbox_boundary_ref=sandbox_boundary_ref,
        tool_boundary_ref=tool_boundary_ref,
        model_boundary_ref=model_boundary_ref,
        context_boundary_ref=context_boundary_ref,
        output_boundary_ref=output_boundary_ref,
        secrets_policy_ref=secrets_policy_ref,
        prompt_injection_defense_ref=prompt_injection_defense_ref,
        human_approval_ref=human_approval_ref,
        kill_switch_ref=kill_switch_ref,
        rollback_ref=rollback_ref,
        dry_run_ref=dry_run_ref,
    )
    auto_missing = tuple(dep.kind.value for dep in dependencies if dep.required and not dep.present)
    snapshot_missing = prepared_snapshot.missing_required()
    explicit_missing = _to_tuple_of_strings(missing_dependencies or ())
    return RuntimeExecutionPreparationPackage(
        preparation_id=str(preparation_id or "").strip(),
        intent_ref=str(intent_ref or "").strip(),
        attempt_ref=_clean_optional_ref(attempt_ref),
        runtime_governance_ref=str(runtime_governance_ref or "").strip(),
        runtime_state_ref=str(runtime_state_ref or "").strip(),
        observability_ref=str(observability_ref or "").strip(),
        runtime_activation_gate_ref=str(runtime_activation_gate_ref or "").strip(),
        security_baseline_ref=str(security_baseline_ref or "").strip(),
        agent_permission_ref=str(agent_permission_ref or "").strip(),
        sandbox_boundary_ref=str(sandbox_boundary_ref or "").strip(),
        tool_boundary_ref=str(tool_boundary_ref or "").strip(),
        model_boundary_ref=str(model_boundary_ref or "").strip(),
        context_boundary_ref=str(context_boundary_ref or "").strip(),
        output_boundary_ref=str(output_boundary_ref or "").strip(),
        secrets_policy_ref=str(secrets_policy_ref or "").strip(),
        prompt_injection_defense_ref=str(prompt_injection_defense_ref or "").strip(),
        human_approval_ref=_clean_optional_ref(human_approval_ref),
        kill_switch_ref=_clean_optional_ref(kill_switch_ref),
        rollback_ref=_clean_optional_ref(rollback_ref),
        dry_run_ref=_clean_optional_ref(dry_run_ref),
        execution_scope=str(execution_scope or "").strip(),
        execution_mode=_coerce_mode(execution_mode),
        execution_risk_level=_coerce_risk_level(execution_risk_level),
        required_dependencies=dependencies,
        missing_dependencies=tuple(dict.fromkeys((*auto_missing, *snapshot_missing, *explicit_missing))),
        blocked_capabilities=_to_tuple_of_strings(blocked_capabilities or BLOCKED_CAPABILITIES),
        forbidden_readiness=_to_tuple_of_strings(forbidden_readiness or FORBIDDEN_READINESS),
        metadata=clean_metadata,
        prepared_snapshot=prepared_snapshot,
        status=_coerce_status(status),
        readiness=readiness,
    )


def validate_runtime_execution_preparation_package(
    package: RuntimeExecutionPreparationPackage,
    policy: RuntimeExecutionPreparationPolicy | None = None,
) -> RuntimeExecutionPreparationValidationResult:
    resolved_policy = policy or build_runtime_execution_preparation_policy()
    errors: list[str] = []
    warnings: list[str] = []
    missing: list[str] = list(package.missing_dependencies)
    for field_name in REQUIRED_REF_FIELDS:
        if not str(getattr(package, field_name, "") or "").strip():
            errors.append(f"missing_required_ref:{field_name}")
            missing.append(field_name)
    for optional_field in OPTIONAL_REF_FIELDS:
        if not getattr(package, optional_field):
            warnings.append(f"missing_optional_ref:{optional_field}")
    for dependency in package.required_dependencies:
        if dependency.required and (not dependency.present or not dependency.ref):
            errors.append(f"missing_dependency:{dependency.kind.value}")
            missing.append(dependency.kind.value)
    for name in package.prepared_snapshot.missing_required():
        errors.append(f"missing_boundary:{name}")
        missing.append(name)
    forbidden_readiness_detected = _forbidden_readiness_detected(package.readiness, package.forbidden_readiness)
    for readiness in forbidden_readiness_detected:
        errors.append(f"forbidden_readiness:{readiness}")
    if _enum_or_string(package.status) in FORBIDDEN_STATUSES:
        errors.append(f"forbidden_status:{_enum_or_string(package.status)}")
    if _enum_or_string(package.status) not in ALLOWED_STATUSES:
        errors.append(f"status_not_allowed:{_enum_or_string(package.status)}")
    if package.metadata.blocked_keys:
        errors.append("dangerous_metadata_detected")
    for capability in package.blocked_capabilities:
        if capability not in BLOCKED_CAPABILITIES:
            errors.append(f"unknown_or_enabled_capability:{capability}")
        else:
            errors.append(f"operational_capability_blocked:{capability}") if capability not in BLOCKED_CAPABILITIES else None
    if tuple(package.blocked_capabilities) != BLOCKED_CAPABILITIES:
        errors.append("blocked_capabilities_must_match_default_deny")
    if not resolved_policy.contract_ready:
        errors.append("policy_contract_ready_false")
    for field_name, value in asdict(resolved_policy).items():
        if field_name != "contract_ready" and value is True:
            errors.append(f"operational_policy_flag_enabled:{field_name}")
    try:
        json.dumps(runtime_execution_preparation_to_dict(package), sort_keys=True)
    except (TypeError, ValueError):
        errors.append("package_not_json_safe")
    unique_missing = tuple(dict.fromkeys(missing))
    if errors:
        status = RuntimeExecutionPreparationStatus.INVALID
    elif unique_missing:
        status = RuntimeExecutionPreparationStatus.BLOCKED
    else:
        status = RuntimeExecutionPreparationStatus.READY_SIMULATED
    return RuntimeExecutionPreparationValidationResult(
        is_valid=not errors and not unique_missing,
        status=status,
        readiness=package.readiness,
        missing_dependencies=unique_missing,
        blocked_capabilities=tuple(package.blocked_capabilities),
        forbidden_readiness_detected=forbidden_readiness_detected,
        metadata_blocked_keys=package.metadata.blocked_keys,
        errors=tuple(dict.fromkeys(errors)),
        warnings=tuple(dict.fromkeys(warnings)),
    )


def decide_runtime_execution_preparation(
    validation_result: RuntimeExecutionPreparationValidationResult,
    policy: RuntimeExecutionPreparationPolicy | None = None,
) -> RuntimeExecutionPreparationDecisionRecord:
    resolved_policy = policy or build_runtime_execution_preparation_policy()
    operational_policy_enabled = any(
        value is True for key, value in asdict(resolved_policy).items() if key != "contract_ready"
    )
    if operational_policy_enabled or not resolved_policy.contract_ready:
        decision = RuntimeExecutionPreparationDecision.INVALID
        allowed = False
        reason = "invalid_policy"
    elif validation_result.errors:
        decision = RuntimeExecutionPreparationDecision.INVALID
        allowed = False
        reason = "validation_errors"
    elif validation_result.missing_dependencies:
        if any(item.startswith("human_approval") or item == "dry_run" for item in validation_result.missing_dependencies):
            decision = RuntimeExecutionPreparationDecision.REQUIRE_HUMAN_APPROVAL
        else:
            decision = RuntimeExecutionPreparationDecision.REQUIRE_DEPENDENCIES
        allowed = False
        reason = "missing_dependencies"
    elif validation_result.is_valid:
        decision = RuntimeExecutionPreparationDecision.ALLOW_SIMULATED_PREPARATION
        allowed = True
        reason = "simulated_preparation_only"
    else:
        decision = RuntimeExecutionPreparationDecision.BLOCK_PREPARATION
        allowed = False
        reason = "blocked"
    return RuntimeExecutionPreparationDecisionRecord(
        decision=decision,
        allowed=allowed,
        simulated_preparation_allowed=allowed and decision == RuntimeExecutionPreparationDecision.ALLOW_SIMULATED_PREPARATION,
        runtime_execution_allowed=False,
        runtime_activation_allowed=False,
        dry_run_execution_allowed=False,
        tool_execution_allowed=False,
        model_invocation_allowed=False,
        context_injection_allowed=False,
        output_delivery_allowed=False,
        writes_allowed=False,
        stores_allowed=False,
        reason=reason,
        errors=validation_result.errors,
        warnings=validation_result.warnings,
    )


def runtime_execution_preparation_to_dict(value: Any) -> Any:
    return _to_json_safe(value)


def build_runtime_execution_preparation_contract_snapshot(
    *,
    package: RuntimeExecutionPreparationPackage | None = None,
    validation: RuntimeExecutionPreparationValidationResult | None = None,
    decision: RuntimeExecutionPreparationDecisionRecord | None = None,
    policy: RuntimeExecutionPreparationPolicy | None = None,
) -> RuntimeExecutionPreparationContractSnapshot:
    resolved_policy = policy or build_runtime_execution_preparation_policy()
    dependencies = package.required_dependencies if package is not None else ()
    return RuntimeExecutionPreparationContractSnapshot(
        contract_status=CONTRACT_STATUS,
        policy=resolved_policy,
        allowed_statuses=ALLOWED_STATUSES,
        forbidden_statuses=FORBIDDEN_STATUSES,
        allowed_readiness=ALLOWED_READINESS,
        forbidden_readiness=FORBIDDEN_READINESS,
        blocked_capabilities=BLOCKED_CAPABILITIES,
        forbidden_metadata_keys=FORBIDDEN_METADATA_KEYS,
        dependencies=dependencies,
        package=package,
        validation=validation,
        decision=decision,
    )


def get_runtime_execution_preparation_contract_status() -> dict[str, Any]:
    return {
        "contract_status": CONTRACT_STATUS,
        "verdict": CONTRACT_VERDICT,
        "readiness": CONTRACT_READINESS,
        "next_step": CONTRACT_NEXT_STEP,
        "contract_ready": RUNTIME_EXECUTION_PREPARATION_CONTRACT_READY,
        "operational": RUNTIME_EXECUTION_PREPARATION_OPERATIONAL,
        "runtime_active": RUNTIME_EXECUTION_PREPARATION_RUNTIME_ACTIVE,
        "execution_active": RUNTIME_EXECUTION_PREPARATION_EXECUTION_ACTIVE,
        "dry_run_active": RUNTIME_EXECUTION_PREPARATION_DRY_RUN_ACTIVE,
        "tools_enabled": RUNTIME_EXECUTION_PREPARATION_TOOLS_ENABLED,
        "models_enabled": RUNTIME_EXECUTION_PREPARATION_MODELS_ENABLED,
        "context_enabled": RUNTIME_EXECUTION_PREPARATION_CONTEXT_ENABLED,
        "output_enabled": RUNTIME_EXECUTION_PREPARATION_OUTPUT_ENABLED,
        "writes_enabled": RUNTIME_EXECUTION_PREPARATION_WRITES_ENABLED,
        "stores_enabled": RUNTIME_EXECUTION_PREPARATION_STORES_ENABLED,
        "memory_enabled": RUNTIME_EXECUTION_PREPARATION_MEMORY_ENABLED,
        "network_enabled": RUNTIME_EXECUTION_PREPARATION_NETWORK_ENABLED,
        "browser_enabled": RUNTIME_EXECUTION_PREPARATION_BROWSER_ENABLED,
        "filesystem_enabled": RUNTIME_EXECUTION_PREPARATION_FILESYSTEM_ENABLED,
        "env_enabled": RUNTIME_EXECUTION_PREPARATION_ENV_ENABLED,
        "secrets_enabled": RUNTIME_EXECUTION_PREPARATION_SECRETS_ENABLED,
        "integrations_enabled": RUNTIME_EXECUTION_PREPARATION_INTEGRATIONS_ENABLED,
        "excluded_external_concepts": tuple(sorted(EXCLUDED_EXTERNAL_CONCEPTS)),
    }


def _default_dependencies(**refs: str | None) -> tuple[RuntimeExecutionPreparationDependency, ...]:
    mapping = (
        (RuntimeExecutionPreparationDependencyKind.EXECUTION_INTENT, "intent_ref", True),
        (RuntimeExecutionPreparationDependencyKind.ATTEMPT_REFERENCE, "attempt_ref", False),
        (RuntimeExecutionPreparationDependencyKind.RUNTIME_GOVERNANCE, "runtime_governance_ref", True),
        (RuntimeExecutionPreparationDependencyKind.RUNTIME_STATE, "runtime_state_ref", True),
        (RuntimeExecutionPreparationDependencyKind.OBSERVABILITY, "observability_ref", True),
        (RuntimeExecutionPreparationDependencyKind.RUNTIME_ACTIVATION_GATE, "runtime_activation_gate_ref", True),
        (RuntimeExecutionPreparationDependencyKind.SECURITY_BASELINE, "security_baseline_ref", True),
        (RuntimeExecutionPreparationDependencyKind.AGENT_PERMISSION, "agent_permission_ref", True),
        (RuntimeExecutionPreparationDependencyKind.SANDBOX_BOUNDARY, "sandbox_boundary_ref", True),
        (RuntimeExecutionPreparationDependencyKind.TOOL_BOUNDARY, "tool_boundary_ref", True),
        (RuntimeExecutionPreparationDependencyKind.MODEL_BOUNDARY, "model_boundary_ref", True),
        (RuntimeExecutionPreparationDependencyKind.CONTEXT_BOUNDARY, "context_boundary_ref", True),
        (RuntimeExecutionPreparationDependencyKind.OUTPUT_BOUNDARY, "output_boundary_ref", True),
        (RuntimeExecutionPreparationDependencyKind.SECRETS_POLICY, "secrets_policy_ref", True),
        (RuntimeExecutionPreparationDependencyKind.PROMPT_INJECTION_DEFENSE, "prompt_injection_defense_ref", True),
        (RuntimeExecutionPreparationDependencyKind.HUMAN_APPROVAL, "human_approval_ref", False),
        (RuntimeExecutionPreparationDependencyKind.KILL_SWITCH, "kill_switch_ref", False),
        (RuntimeExecutionPreparationDependencyKind.ROLLBACK, "rollback_ref", False),
        (RuntimeExecutionPreparationDependencyKind.DRY_RUN, "dry_run_ref", False),
    )
    return tuple(
        build_runtime_execution_preparation_dependency(
            kind=kind,
            ref=refs.get(ref_name),
            required=required,
        )
        for kind, ref_name, required in mapping
    )


def _is_forbidden_metadata_key(normalized_key: str) -> bool:
    return any(fragment in normalized_key for fragment in FORBIDDEN_METADATA_KEYS)


def _forbidden_readiness_detected(readiness: RuntimeExecutionPreparationReadiness | str, forbidden: tuple[str, ...]) -> tuple[str, ...]:
    value = _enum_or_string(readiness)
    detected = [value] if value in forbidden or value in FORBIDDEN_READINESS else []
    return tuple(detected)


def _coerce_dependency_kind(value: RuntimeExecutionPreparationDependencyKind | str) -> RuntimeExecutionPreparationDependencyKind:
    if isinstance(value, RuntimeExecutionPreparationDependencyKind):
        return value
    return RuntimeExecutionPreparationDependencyKind(str(value))


def _coerce_mode(value: RuntimeExecutionPreparationMode | str) -> RuntimeExecutionPreparationMode:
    if isinstance(value, RuntimeExecutionPreparationMode):
        return value
    return RuntimeExecutionPreparationMode(str(value))


def _coerce_risk_level(value: RuntimeExecutionPreparationRiskLevel | str) -> RuntimeExecutionPreparationRiskLevel:
    if isinstance(value, RuntimeExecutionPreparationRiskLevel):
        return value
    return RuntimeExecutionPreparationRiskLevel(str(value))


def _coerce_status(value: RuntimeExecutionPreparationStatus | str) -> RuntimeExecutionPreparationStatus:
    if isinstance(value, RuntimeExecutionPreparationStatus):
        return value
    return RuntimeExecutionPreparationStatus(str(value))


def _clean_optional_ref(value: str | None) -> str | None:
    clean = str(value or "").strip()
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

