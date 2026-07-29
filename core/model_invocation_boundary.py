"""Contract-only model invocation boundary for IA_CORE pre-runtime policy.

This module classifies conceptual model invocation requests and validates
boundary decisions. It never invokes models, calls providers, starts inference,
streams output, expands context from real sources, logs raw prompts/outputs,
passes secrets to prompts, executes tools, persists memory, writes stores, or
activates integrations.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any


MODEL_INVOCATION_BOUNDARY_STATUS = "contract_only"
MODEL_INVOCATION_BOUNDARY_READY = True

MODEL_INVOCATION_RUNTIME_ENABLED = False
MODEL_INVOCATION_ENABLED = False
MODEL_INVOCATION_MODEL_ROUTER_ENABLED = False
MODEL_INVOCATION_MODEL_EXECUTOR_ENABLED = False
MODEL_INVOCATION_INFERENCE_RUNNER_ENABLED = False
MODEL_INVOCATION_PROVIDER_CALLS_ENABLED = False
MODEL_INVOCATION_LOCAL_PROVIDER_ENABLED = False
MODEL_INVOCATION_REMOTE_PROVIDER_ENABLED = False
MODEL_INVOCATION_STREAMING_ENABLED = False
MODEL_INVOCATION_CONTEXT_EXPANSION_ENABLED = False
MODEL_INVOCATION_RAW_PROMPT_LOGGING_ENABLED = False
MODEL_INVOCATION_RAW_OUTPUT_LOGGING_ENABLED = False

MODEL_INVOCATION_TOOL_EXECUTION_ENABLED = False
MODEL_INVOCATION_TOOL_ADAPTERS_ENABLED = False
MODEL_INVOCATION_TOOL_CALLS_ENABLED = False
MODEL_INVOCATION_MEMORY_PERSISTENCE_ENABLED = False
MODEL_INVOCATION_EXTERNAL_ACCESS_ENABLED = False
MODEL_INVOCATION_NETWORK_ENABLED = False
MODEL_INVOCATION_API_ENABLED = False
MODEL_INVOCATION_UI_ENABLED = False
MODEL_INVOCATION_WRITES_ENABLED = False
MODEL_INVOCATION_STORES_ENABLED = False

MODEL_INVOCATION_FILESYSTEM_ENABLED = False
MODEL_INVOCATION_COMMAND_EXECUTION_ENABLED = False
MODEL_INVOCATION_SHELL_ENABLED = False
MODEL_INVOCATION_PROCESS_SPAWN_ENABLED = False
MODEL_INVOCATION_ENV_ACCESS_ENABLED = False
MODEL_INVOCATION_SECRET_ACCESS_ENABLED = False
MODEL_INVOCATION_HOST_ACCESS_ENABLED = False
MODEL_INVOCATION_DEVICE_ACCESS_ENABLED = False
MODEL_INVOCATION_BROWSER_ENABLED = False
MODEL_INVOCATION_CLIPBOARD_ENABLED = False

MODEL_INVOCATION_UI_TARS_ENABLED = False
MODEL_INVOCATION_HERMES_ENABLED = False
MODEL_INVOCATION_N8N_ENABLED = False
MODEL_INVOCATION_HOME_ASSISTANT_ENABLED = False

MODEL_INVOCATION_MARKET_CATALOG_RUNTIME_ENABLED = False
MODEL_INVOCATION_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False

MODEL_TYPES = {
    "local_llm",
    "remote_llm",
    "embedding_model",
    "reranker_model",
    "vision_model",
    "audio_model",
    "multimodal_model",
    "reasoning_model",
    "small_fast_model",
    "large_capability_model",
    "specialized_domain_model",
    "tool_calling_model",
    "code_model",
    "classification_model",
    "summarization_model",
    "translation_model",
    "planning_model",
    "validation_model",
}
CONCEPTUAL_MODEL_TYPES = {
    "local_llm",
    "embedding_model",
    "reranker_model",
    "small_fast_model",
    "classification_model",
    "summarization_model",
    "translation_model",
    "planning_model",
    "validation_model",
}
SANDBOX_REQUIRED_MODEL_TYPES = {
    "remote_llm",
    "vision_model",
    "audio_model",
    "multimodal_model",
    "reasoning_model",
    "large_capability_model",
    "specialized_domain_model",
    "code_model",
}
BLOCKED_MODEL_TYPES = {"tool_calling_model"}

MODEL_SURFACES = {
    "prompt",
    "system_prompt",
    "developer_prompt",
    "agent_instruction",
    "context_window",
    "retrieved_context",
    "documents",
    "tool_results",
    "screen_content",
    "memory",
    "history",
    "read_model",
    "projection",
    "secrets",
    "environment",
    "filesystem",
    "network",
    "api",
    "provider_endpoint",
    "local_model_runtime",
    "remote_model_runtime",
    "streaming_output",
    "output_parser",
    "tool_call_suggestions",
    "structured_output",
    "external_services",
    "stores",
    "logs",
    "audit_trail",
}
CONTRACTUAL_SURFACES = {"prompt", "agent_instruction", "context_window", "output_parser", "structured_output", "audit_trail"}
REDACTION_SURFACES = {"system_prompt", "developer_prompt", "retrieved_context", "documents", "tool_results", "screen_content", "logs"}
SANDBOX_REQUIRED_SURFACES = {"memory", "history", "read_model", "projection", "filesystem", "network", "api", "provider_endpoint", "local_model_runtime", "remote_model_runtime", "streaming_output", "external_services", "stores"}
BLOCKED_SURFACES = {"secrets", "environment", "tool_call_suggestions"}
CRITICAL_SURFACES = BLOCKED_SURFACES | {"provider_endpoint", "remote_model_runtime", "stores"}

ALLOWED_ACTIONS = {
    "classify_model_type",
    "classify_model_surface",
    "classify_model_invocation_risk",
    "build_model_invocation_boundary_decision",
    "evaluate_model_invocation_boundary_contract",
    "validate_model_invocation_boundary_decision",
    "serialize_model_invocation_boundary_decision",
    "generate_model_invocation_risk_report",
}
FORBIDDEN_ACTIONS = {
    "invoke_model",
    "call_model_provider",
    "call_local_model",
    "call_remote_model",
    "start_inference",
    "stream_model_output",
    "expand_context_from_memory",
    "expand_context_from_filesystem",
    "expand_context_from_web",
    "inject_secret_into_prompt",
    "log_raw_prompt",
    "log_raw_output",
    "send_prompt_to_external_provider",
    "send_context_to_external_provider",
    "tool_call_from_model_output",
    "execute_model_suggested_action",
    "persist_model_output",
    "write_model_result_store",
    "update_memory_from_model_output",
    "open_browser",
    "call_api",
    "network_request",
    "read_real_file",
    "write_real_file",
    "read_env",
    "read_secret",
    "run_command",
    "open_shell",
    "spawn_process",
    "control_ui",
    "control_device",
    "trigger_workflow",
    "irreversible_action",
}

ALLOWED_STATUSES = {"contract_only", "evaluated", "blocked", "invalid"}
ALLOWED_DECISIONS = {"allowed_contractually", "requires_approval", "sandbox_required", "redaction_required", "blocked", "invalid"}
ALLOWED_READINESS = {"ready_for_model_invocation_boundary_e2e_checkpoint", "blocked", "invalid"}
RISK_LEVELS = {"low", "medium", "high", "critical"}

FORBIDDEN_TRUE_FLAGS = {
    "runtime_enabled",
    "model_invocation_enabled",
    "model_router_enabled",
    "model_executor_enabled",
    "inference_runner_enabled",
    "provider_calls_enabled",
    "local_provider_enabled",
    "remote_provider_enabled",
    "streaming_enabled",
    "context_expansion_enabled",
    "raw_prompt_logging_enabled",
    "raw_output_logging_enabled",
    "tool_execution_enabled",
    "tool_adapters_enabled",
    "tool_calls_enabled",
    "memory_persistence_enabled",
    "external_access_enabled",
    "network_enabled",
    "api_enabled",
    "ui_enabled",
    "writes_enabled",
    "stores_enabled",
    "filesystem_enabled",
    "command_execution_enabled",
    "shell_enabled",
    "process_spawn_enabled",
    "env_access_enabled",
    "secret_access_enabled",
    "host_access_enabled",
    "device_access_enabled",
    "browser_enabled",
    "clipboard_enabled",
    "ui_tars_enabled",
    "hermes_enabled",
    "n8n_enabled",
    "home_assistant_enabled",
    "market_catalog_active",
    "business_composition_enabled",
    "market_catalog_runtime_enabled",
    "business_composition_runtime_enabled",
    "gate_open",
    "operations_enabled",
}
FORBIDDEN_STRING_VALUES = {"ready_for_runtime", "gate_open", "operations_enabled", "market_catalog_active"}
OBLITERATUS_TOKEN = "obliteratus"


@dataclass(frozen=True)
class ModelTypeClassification:
    model_type: str
    known: bool
    category: str
    risk_level: str
    requires_sandbox: bool
    requires_human_approval: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ModelSurfaceClassification:
    surface: str
    known: bool
    category: str
    operational: bool
    risk_level: str
    blocked_by_default: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ModelInvocationRiskClassification:
    model_type: str | None
    surface: str | None
    operation: str | None
    risk_level: str
    forbidden_operation: bool
    requires_human_approval: bool
    requires_redaction: bool
    requires_sandbox: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ModelInvocationBoundaryDecision:
    model_invocation_boundary_decision_id: str
    status: str
    decision: str
    readiness: str
    model_name: str
    model_type: str
    requested_operation: str
    requested_surface: str
    risk_level: str
    requires_agent_permission: bool
    requires_secrets_policy: bool
    requires_prompt_injection_defense: bool
    requires_sandbox_boundary: bool
    requires_tool_boundary: bool
    requires_human_approval: bool
    requires_redaction: bool
    requires_audit: bool
    allowed_to_invoke_model: bool
    allowed_to_call_provider: bool
    allowed_to_use_network: bool
    allowed_to_send_context: bool
    allowed_to_include_secrets: bool
    allowed_to_log_raw_prompt: bool
    allowed_to_log_raw_output: bool
    allowed_to_stream_output: bool
    allowed_to_call_tool: bool
    allowed_to_persist: bool
    allowed_to_update_memory: bool
    allowed_to_execute_suggestion: bool
    blocking_reasons: list[dict[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    lineage: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["blocking_reasons"] = deepcopy(self.blocking_reasons)
        payload["warnings"] = deepcopy(self.warnings)
        payload["lineage"] = deepcopy(self.lineage)
        payload["metadata"] = deepcopy(self.metadata)
        return payload


def classify_model_type(model_type_or_name: Any) -> ModelTypeClassification:
    value = "" if model_type_or_name is None else str(model_type_or_name)
    if value in CONCEPTUAL_MODEL_TYPES:
        category = "conceptual"
        risk = "low"
        requires_sandbox = False
        requires_approval = False
    elif value in SANDBOX_REQUIRED_MODEL_TYPES:
        category = "capability_or_provider_sensitive"
        risk = "high"
        requires_sandbox = True
        requires_approval = value in {"remote_llm", "large_capability_model"}
    elif value in BLOCKED_MODEL_TYPES:
        category = "tool_calling_blocked"
        risk = "critical"
        requires_sandbox = True
        requires_approval = True
    else:
        category = "unknown"
        risk = "critical"
        requires_sandbox = True
        requires_approval = True
    return ModelTypeClassification(
        model_type=value,
        known=value in MODEL_TYPES,
        category=category,
        risk_level=risk,
        requires_sandbox=requires_sandbox,
        requires_human_approval=requires_approval,
    )


def classify_model_surface(surface: Any) -> ModelSurfaceClassification:
    value = "" if surface is None else str(surface)
    if value in CONTRACTUAL_SURFACES:
        category = "contractual"
        risk = "low"
        operational = False
    elif value in REDACTION_SURFACES:
        category = "redaction_required"
        risk = "medium"
        operational = False
    elif value in SANDBOX_REQUIRED_SURFACES:
        category = "sandbox_required"
        risk = "critical" if value in CRITICAL_SURFACES else "high"
        operational = True
    elif value in BLOCKED_SURFACES:
        category = "blocked_sensitive"
        risk = "critical"
        operational = True
    else:
        category = "unknown"
        risk = "critical"
        operational = True
    return ModelSurfaceClassification(
        surface=value,
        known=value in MODEL_SURFACES,
        category=category,
        operational=operational,
        risk_level=risk,
        blocked_by_default=True,
    )


def classify_model_invocation_risk(model_type: Any = None, surface: Any = None, operation: Any = None) -> ModelInvocationRiskClassification:
    type_classification = classify_model_type(model_type)
    surface_classification = classify_model_surface(surface)
    operation_value = "" if operation is None else str(operation)
    forbidden_operation = operation_value in FORBIDDEN_ACTIONS
    requires_redaction = surface_classification.category == "redaction_required" or operation_value == "inject_secret_into_prompt"
    requires_sandbox = type_classification.requires_sandbox or surface_classification.operational
    requires_approval = type_classification.requires_human_approval or surface_classification.surface in {"provider_endpoint", "remote_model_runtime"}
    risk = _max_risk(
        type_classification.risk_level,
        surface_classification.risk_level,
        "critical" if forbidden_operation else "low",
        "high" if requires_redaction else "low",
    )
    return ModelInvocationRiskClassification(
        model_type=type_classification.model_type,
        surface=surface_classification.surface,
        operation=operation_value,
        risk_level=risk,
        forbidden_operation=forbidden_operation,
        requires_human_approval=requires_approval,
        requires_redaction=requires_redaction,
        requires_sandbox=requires_sandbox,
    )


def build_model_invocation_boundary_decision(
    *,
    model_invocation_boundary_decision_id: str,
    model_name: str,
    model_type: str,
    requested_operation: str,
    requested_surface: str,
    decision: str = "allowed_contractually",
    status: str = "evaluated",
    readiness: str = "ready_for_model_invocation_boundary_e2e_checkpoint",
    risk_level: str = "low",
    requires_agent_permission: bool = True,
    requires_secrets_policy: bool = True,
    requires_prompt_injection_defense: bool = True,
    requires_sandbox_boundary: bool = True,
    requires_tool_boundary: bool = True,
    requires_human_approval: bool = False,
    requires_redaction: bool = False,
    requires_audit: bool = True,
    allowed_to_invoke_model: bool = False,
    allowed_to_call_provider: bool = False,
    allowed_to_use_network: bool = False,
    allowed_to_send_context: bool = False,
    allowed_to_include_secrets: bool = False,
    allowed_to_log_raw_prompt: bool = False,
    allowed_to_log_raw_output: bool = False,
    allowed_to_stream_output: bool = False,
    allowed_to_call_tool: bool = False,
    allowed_to_persist: bool = False,
    allowed_to_update_memory: bool = False,
    allowed_to_execute_suggestion: bool = False,
    blocking_reasons: list[dict[str, str]] | None = None,
    warnings: list[str] | None = None,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ModelInvocationBoundaryDecision:
    return ModelInvocationBoundaryDecision(
        model_invocation_boundary_decision_id=model_invocation_boundary_decision_id,
        status=status,
        decision=decision,
        readiness=readiness,
        model_name=model_name,
        model_type=model_type,
        requested_operation=requested_operation,
        requested_surface=requested_surface,
        risk_level=risk_level,
        requires_agent_permission=requires_agent_permission,
        requires_secrets_policy=requires_secrets_policy,
        requires_prompt_injection_defense=requires_prompt_injection_defense,
        requires_sandbox_boundary=requires_sandbox_boundary,
        requires_tool_boundary=requires_tool_boundary,
        requires_human_approval=requires_human_approval,
        requires_redaction=requires_redaction,
        requires_audit=requires_audit,
        allowed_to_invoke_model=allowed_to_invoke_model,
        allowed_to_call_provider=allowed_to_call_provider,
        allowed_to_use_network=allowed_to_use_network,
        allowed_to_send_context=allowed_to_send_context,
        allowed_to_include_secrets=allowed_to_include_secrets,
        allowed_to_log_raw_prompt=allowed_to_log_raw_prompt,
        allowed_to_log_raw_output=allowed_to_log_raw_output,
        allowed_to_stream_output=allowed_to_stream_output,
        allowed_to_call_tool=allowed_to_call_tool,
        allowed_to_persist=allowed_to_persist,
        allowed_to_update_memory=allowed_to_update_memory,
        allowed_to_execute_suggestion=allowed_to_execute_suggestion,
        blocking_reasons=list(blocking_reasons or []),
        warnings=list(warnings or []),
        lineage=dict(lineage or {}),
        metadata=dict(metadata or {}),
    )


def evaluate_model_invocation_boundary_contract(
    *,
    model_name: str,
    model_type: str,
    requested_operation: str,
    requested_surface: str,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ModelInvocationBoundaryDecision:
    type_classification = classify_model_type(model_type)
    surface_classification = classify_model_surface(requested_surface)
    risk = classify_model_invocation_risk(model_type, requested_surface, requested_operation)
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []

    _require(model_name, blockers, "missing_model_name", "model_name requerido")
    if not type_classification.known:
        _block(blockers, "unknown_model_type", "model_type desconocido")
    if not surface_classification.known:
        _block(blockers, "unknown_model_surface", "requested_surface desconocida")
    if requested_operation in FORBIDDEN_ACTIONS:
        _block(blockers, "operation_blocked_pre_runtime", "operacion prohibida en pre-runtime")
    if _contains_obliteratus([model_name, model_type, requested_surface, requested_operation, lineage, metadata]):
        _block(blockers, "obliteratus_not_allowed", "OBLITERATUS no es model provider, dependency, adapter ni capability")

    if blockers:
        decision = "invalid" if any(item["code"].startswith(("missing_", "unknown_", "obliteratus")) for item in blockers) else "blocked"
    elif model_type in BLOCKED_MODEL_TYPES or requested_surface in BLOCKED_SURFACES:
        decision = "blocked"
        _block(blockers, "sensitive_model_surface_blocked", "surface/model sensible bloqueado en pre-runtime")
    elif risk.requires_redaction:
        decision = "redaction_required"
        warnings.append("redaction_required_no_invocation_allowed")
    elif risk.requires_human_approval:
        decision = "requires_approval"
        warnings.append("human_approval_required_no_invocation_allowed")
    elif risk.requires_sandbox:
        decision = "sandbox_required"
        warnings.append("sandbox_required_contract_only_no_sandbox_created")
    else:
        decision = "allowed_contractually"

    return build_model_invocation_boundary_decision(
        model_invocation_boundary_decision_id=f"model_invocation_boundary_{model_name or 'missing_model'}_{model_type or 'missing_type'}_{requested_operation or 'missing_operation'}",
        model_name=model_name,
        model_type=model_type,
        requested_operation=requested_operation,
        requested_surface=requested_surface,
        decision=decision,
        status="invalid" if decision == "invalid" else "evaluated",
        readiness="ready_for_model_invocation_boundary_e2e_checkpoint" if decision not in {"invalid", "blocked"} else "blocked",
        risk_level=risk.risk_level,
        requires_human_approval=risk.requires_human_approval,
        requires_redaction=risk.requires_redaction,
        blocking_reasons=blockers,
        warnings=warnings,
        lineage={
            "agent_permission_boundary": "active_contractual_boundary",
            "secrets_policy_boundary": "active_contractual_boundary",
            "prompt_injection_defense_boundary": "active_contractual_boundary",
            "sandbox_boundary": "active_contractual_boundary",
            "tool_boundary": "active_contractual_boundary",
            "operational_readiness_gate_boundary": "closed",
            **deepcopy(lineage or {}),
        },
        metadata={**_boundary_flags(), **deepcopy(metadata or {})},
    )


def validate_model_invocation_boundary_decision(decision: ModelInvocationBoundaryDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_model_invocation_boundary_decision(decision)
    blockers: list[dict[str, str]] = []

    _require(payload.get("model_invocation_boundary_decision_id"), blockers, "missing_model_invocation_boundary_decision_id", "model_invocation_boundary_decision_id requerido")
    _allowed(payload.get("status"), ALLOWED_STATUSES, blockers, "invalid_status", "status invalido")
    _allowed(payload.get("decision"), ALLOWED_DECISIONS, blockers, "invalid_decision", "decision invalida")
    _allowed(payload.get("readiness"), ALLOWED_READINESS, blockers, "invalid_readiness", "readiness invalida")
    _require(payload.get("model_name"), blockers, "missing_model_name", "model_name requerido")
    _require(payload.get("model_type"), blockers, "missing_model_type", "model_type requerido")
    _require(payload.get("requested_operation"), blockers, "missing_requested_operation", "requested_operation requerida")
    _require(payload.get("requested_surface"), blockers, "missing_requested_surface", "requested_surface requerida")
    _allowed(payload.get("risk_level"), RISK_LEVELS, blockers, "invalid_risk_level", "risk_level invalido")

    for field_name in [
        "requires_agent_permission",
        "requires_secrets_policy",
        "requires_prompt_injection_defense",
        "requires_sandbox_boundary",
        "requires_tool_boundary",
        "requires_audit",
    ]:
        if payload.get(field_name) is not True:
            _block(blockers, f"{field_name}_required", f"{field_name} debe ser True")
    for field_name in ["requires_human_approval", "requires_redaction"]:
        if not isinstance(payload.get(field_name), bool):
            _block(blockers, f"{field_name}_not_bool", f"{field_name} debe ser bool")
    for field_name in [
        "allowed_to_invoke_model",
        "allowed_to_call_provider",
        "allowed_to_use_network",
        "allowed_to_send_context",
        "allowed_to_include_secrets",
        "allowed_to_log_raw_prompt",
        "allowed_to_log_raw_output",
        "allowed_to_stream_output",
        "allowed_to_call_tool",
        "allowed_to_persist",
        "allowed_to_update_memory",
        "allowed_to_execute_suggestion",
    ]:
        if payload.get(field_name) is not False:
            _block(blockers, f"{field_name}_not_allowed", f"{field_name} debe ser False")
    for field_name in ["blocking_reasons", "warnings"]:
        if not isinstance(payload.get(field_name), list):
            _block(blockers, f"{field_name}_not_list", f"{field_name} debe ser lista")
    for field_name in ["lineage", "metadata"]:
        if not isinstance(payload.get(field_name), dict):
            _block(blockers, f"{field_name}_not_dict", f"{field_name} debe ser dict")

    operation = payload.get("requested_operation")
    if operation in FORBIDDEN_ACTIONS and payload.get("decision") not in {"blocked", "invalid"}:
        _block(blockers, "blocked_operation_not_blocked", "operacion prohibida debe quedar blocked o invalid")
    if payload.get("model_type") in BLOCKED_MODEL_TYPES and payload.get("decision") not in {"blocked", "invalid"}:
        _block(blockers, "blocked_model_type_not_blocked", "model_type sensible debe quedar blocked o invalid")
    if payload.get("requested_surface") in BLOCKED_SURFACES and payload.get("decision") not in {"blocked", "invalid"}:
        _block(blockers, "blocked_surface_not_blocked", "surface sensible debe quedar blocked o invalid")

    _validate_boundary_flags(payload, blockers)
    if _contains_obliteratus(payload):
        _block(blockers, "obliteratus_not_allowed", "OBLITERATUS no es model provider, dependency, adapter ni capability")

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "MODEL_INVOCATION_BOUNDARY_READY" if not blockers else "MODEL_INVOCATION_BOUNDARY_BLOCKED",
        "readiness": "ready_for_model_invocation_boundary_e2e_checkpoint" if not blockers else "blocked",
        "blocking_reasons": blockers,
        "warnings": [] if not blockers else ["model_invocation_boundary_decision_blocked"],
        "policy_status": MODEL_INVOCATION_BOUNDARY_STATUS,
        "runtime_enabled": MODEL_INVOCATION_RUNTIME_ENABLED,
        "model_invocation_enabled": MODEL_INVOCATION_ENABLED,
        "provider_calls_enabled": MODEL_INVOCATION_PROVIDER_CALLS_ENABLED,
    }


def serialize_model_invocation_boundary_decision(decision: ModelInvocationBoundaryDecision | dict[str, Any]) -> dict[str, Any]:
    if isinstance(decision, ModelInvocationBoundaryDecision):
        return decision.to_dict()
    return deepcopy(decision)


def generate_model_invocation_risk_report(decision: ModelInvocationBoundaryDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_model_invocation_boundary_decision(decision)
    return {
        "risk": payload.get("risk_level", "medium"),
        "decision": payload.get("decision", "invalid"),
        "model_name": payload.get("model_name"),
        "model_type": payload.get("model_type"),
        "requested_surface": payload.get("requested_surface"),
        "requested_operation": payload.get("requested_operation"),
        "allowed_to_invoke_model": False,
        "requires_redaction": bool(payload.get("requires_redaction")),
        "requires_human_approval": bool(payload.get("requires_human_approval")),
    }


def get_model_invocation_boundary_contract() -> dict[str, Any]:
    return {
        "status": MODEL_INVOCATION_BOUNDARY_STATUS,
        "ready": MODEL_INVOCATION_BOUNDARY_READY,
        "verdict": "MODEL_INVOCATION_BOUNDARY_READY",
        "readiness": "ready_for_model_invocation_boundary_e2e_checkpoint",
        "next_step": "PROMPT 3.27.1 - Checkpoint E2E de model invocation boundary",
        "mode": [
            "contract-only",
            "security-simulated",
            "non-operational",
            "pre-runtime",
            "model-request-only",
            "deny-by-default",
            "permission-aware",
            "secrets-aware",
            "prompt-injection-aware",
            "sandbox-aware",
            "tool-boundary-aware",
            "no real model invocation",
        ],
        "central_rule": "En pre-runtime, un modelo puede describirse, clasificarse o evaluarse. Pero no puede invocarse.",
        "model_types": sorted(MODEL_TYPES),
        "model_surfaces": sorted(MODEL_SURFACES),
        "allowed_actions": sorted(ALLOWED_ACTIONS),
        "forbidden_actions": sorted(FORBIDDEN_ACTIONS),
        "decisions": sorted(ALLOWED_DECISIONS),
        "boundary_flags": _boundary_flags(),
        "agent_permission_boundary": "active_contractual_boundary",
        "secrets_policy_boundary": "active_contractual_boundary",
        "prompt_injection_defense_boundary": "active_contractual_boundary",
        "sandbox_boundary": "active_contractual_boundary",
        "tool_boundary": "active_contractual_boundary",
        "operational_readiness_gate_boundary": "closed",
        "obliteratus": "not_model_provider_not_integration_not_dependency_not_adapter_not_capability",
    }


def _boundary_flags() -> dict[str, bool]:
    return {
        "runtime_enabled": MODEL_INVOCATION_RUNTIME_ENABLED,
        "model_invocation_enabled": MODEL_INVOCATION_ENABLED,
        "model_router_enabled": MODEL_INVOCATION_MODEL_ROUTER_ENABLED,
        "model_executor_enabled": MODEL_INVOCATION_MODEL_EXECUTOR_ENABLED,
        "inference_runner_enabled": MODEL_INVOCATION_INFERENCE_RUNNER_ENABLED,
        "provider_calls_enabled": MODEL_INVOCATION_PROVIDER_CALLS_ENABLED,
        "local_provider_enabled": MODEL_INVOCATION_LOCAL_PROVIDER_ENABLED,
        "remote_provider_enabled": MODEL_INVOCATION_REMOTE_PROVIDER_ENABLED,
        "streaming_enabled": MODEL_INVOCATION_STREAMING_ENABLED,
        "context_expansion_enabled": MODEL_INVOCATION_CONTEXT_EXPANSION_ENABLED,
        "raw_prompt_logging_enabled": MODEL_INVOCATION_RAW_PROMPT_LOGGING_ENABLED,
        "raw_output_logging_enabled": MODEL_INVOCATION_RAW_OUTPUT_LOGGING_ENABLED,
        "tool_execution_enabled": MODEL_INVOCATION_TOOL_EXECUTION_ENABLED,
        "tool_adapters_enabled": MODEL_INVOCATION_TOOL_ADAPTERS_ENABLED,
        "tool_calls_enabled": MODEL_INVOCATION_TOOL_CALLS_ENABLED,
        "memory_persistence_enabled": MODEL_INVOCATION_MEMORY_PERSISTENCE_ENABLED,
        "external_access_enabled": MODEL_INVOCATION_EXTERNAL_ACCESS_ENABLED,
        "network_enabled": MODEL_INVOCATION_NETWORK_ENABLED,
        "api_enabled": MODEL_INVOCATION_API_ENABLED,
        "ui_enabled": MODEL_INVOCATION_UI_ENABLED,
        "writes_enabled": MODEL_INVOCATION_WRITES_ENABLED,
        "stores_enabled": MODEL_INVOCATION_STORES_ENABLED,
        "filesystem_enabled": MODEL_INVOCATION_FILESYSTEM_ENABLED,
        "command_execution_enabled": MODEL_INVOCATION_COMMAND_EXECUTION_ENABLED,
        "shell_enabled": MODEL_INVOCATION_SHELL_ENABLED,
        "process_spawn_enabled": MODEL_INVOCATION_PROCESS_SPAWN_ENABLED,
        "env_access_enabled": MODEL_INVOCATION_ENV_ACCESS_ENABLED,
        "secret_access_enabled": MODEL_INVOCATION_SECRET_ACCESS_ENABLED,
        "host_access_enabled": MODEL_INVOCATION_HOST_ACCESS_ENABLED,
        "device_access_enabled": MODEL_INVOCATION_DEVICE_ACCESS_ENABLED,
        "browser_enabled": MODEL_INVOCATION_BROWSER_ENABLED,
        "clipboard_enabled": MODEL_INVOCATION_CLIPBOARD_ENABLED,
        "ui_tars_enabled": MODEL_INVOCATION_UI_TARS_ENABLED,
        "hermes_enabled": MODEL_INVOCATION_HERMES_ENABLED,
        "n8n_enabled": MODEL_INVOCATION_N8N_ENABLED,
        "home_assistant_enabled": MODEL_INVOCATION_HOME_ASSISTANT_ENABLED,
        "market_catalog_runtime_enabled": MODEL_INVOCATION_MARKET_CATALOG_RUNTIME_ENABLED,
        "business_composition_runtime_enabled": MODEL_INVOCATION_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    }


def _validate_boundary_flags(payload: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    for scope in [payload, payload.get("metadata", {}), payload.get("lineage", {})]:
        if isinstance(scope, dict):
            for key, value in scope.items():
                if key in FORBIDDEN_TRUE_FLAGS and value is True:
                    _block(blockers, f"{key}_not_allowed", f"{key}=True no permitido")
    for name, value in _boundary_flags().items():
        if value is not False:
            _block(blockers, f"{name}_not_allowed", f"{name} debe ser False")
    for value in _flatten_values(payload):
        if isinstance(value, str) and value.lower() in FORBIDDEN_STRING_VALUES:
            _block(blockers, "forbidden_state_value", f"valor prohibido: {value}")


def _max_risk(*levels: str) -> str:
    order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    return max(levels, key=lambda level: order[level])


def _flatten_values(value: Any) -> list[Any]:
    if isinstance(value, dict):
        items: list[Any] = []
        for key, child in value.items():
            items.append(key)
            items.extend(_flatten_values(child))
        return items
    if isinstance(value, list | tuple | set):
        items = []
        for child in value:
            items.extend(_flatten_values(child))
        return items
    return [value]


def _contains_obliteratus(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_obliteratus(k) or _contains_obliteratus(v) for k, v in value.items())
    if isinstance(value, list | tuple | set):
        return any(_contains_obliteratus(item) for item in value)
    return isinstance(value, str) and OBLITERATUS_TOKEN in value.lower()


def _require(value: Any, blockers: list[dict[str, str]], code: str, message: str) -> None:
    if value in (None, ""):
        _block(blockers, code, message)


def _allowed(value: Any, allowed: set[str], blockers: list[dict[str, str]], code: str, message: str) -> None:
    if value not in allowed:
        _block(blockers, code, message)


def _block(blockers: list[dict[str, str]], code: str, message: str) -> None:
    blocker = {"code": code, "message": message}
    if blocker not in blockers:
        blockers.append(blocker)
