"""Contract-only context boundary for IA_CORE pre-runtime policy.

This module classifies conceptual context requests and validates boundary
decisions. It never builds runtime context, injects context, assembles real
prompts, performs retrieval/RAG, expands from real memory/filesystem/web,
includes secrets, executes embedded instructions, sends context to models or
providers, persists memory, writes stores, or activates integrations.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any


CONTEXT_BOUNDARY_STATUS = "contract_only"
CONTEXT_BOUNDARY_READY = True

CONTEXT_RUNTIME_ENABLED = False
CONTEXT_BUILDER_ENABLED = False
CONTEXT_INJECTION_ENABLED = False
CONTEXT_ASSEMBLY_ENABLED = False
CONTEXT_RETRIEVAL_ENABLED = False
CONTEXT_RAG_ENABLED = False
CONTEXT_MEMORY_EXPANSION_ENABLED = False
CONTEXT_FILESYSTEM_EXPANSION_ENABLED = False
CONTEXT_WEB_EXPANSION_ENABLED = False
CONTEXT_TOOL_RESULT_EXPANSION_ENABLED = False
CONTEXT_MODEL_OUTPUT_EXPANSION_ENABLED = False
CONTEXT_SCREEN_EXPANSION_ENABLED = False
CONTEXT_DOCUMENT_EXECUTION_ENABLED = False
CONTEXT_UNTRUSTED_INSTRUCTION_EXECUTION_ENABLED = False
CONTEXT_RAW_CONTEXT_LOGGING_ENABLED = False
CONTEXT_RAW_PROMPT_ASSEMBLY_ENABLED = False

CONTEXT_MODEL_INVOCATION_ENABLED = False
CONTEXT_TOOL_EXECUTION_ENABLED = False
CONTEXT_TOOL_ADAPTERS_ENABLED = False
CONTEXT_TOOL_CALLS_ENABLED = False
CONTEXT_MEMORY_PERSISTENCE_ENABLED = False
CONTEXT_EXTERNAL_ACCESS_ENABLED = False
CONTEXT_NETWORK_ENABLED = False
CONTEXT_API_ENABLED = False
CONTEXT_UI_ENABLED = False
CONTEXT_WRITES_ENABLED = False
CONTEXT_STORES_ENABLED = False

CONTEXT_FILESYSTEM_ENABLED = False
CONTEXT_COMMAND_EXECUTION_ENABLED = False
CONTEXT_SHELL_ENABLED = False
CONTEXT_PROCESS_SPAWN_ENABLED = False
CONTEXT_ENV_ACCESS_ENABLED = False
CONTEXT_SECRET_ACCESS_ENABLED = False
CONTEXT_HOST_ACCESS_ENABLED = False
CONTEXT_DEVICE_ACCESS_ENABLED = False
CONTEXT_BROWSER_ENABLED = False
CONTEXT_CLIPBOARD_ENABLED = False

CONTEXT_UI_TARS_ENABLED = False
CONTEXT_HERMES_ENABLED = False
CONTEXT_N8N_ENABLED = False
CONTEXT_HOME_ASSISTANT_ENABLED = False

CONTEXT_MARKET_CATALOG_RUNTIME_ENABLED = False
CONTEXT_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False

CONTEXT_TYPES = {
    "user_message_context",
    "system_context",
    "developer_context",
    "agent_instruction_context",
    "domain_context",
    "role_context",
    "specialization_context",
    "task_context",
    "document_context",
    "retrieved_context",
    "memory_context",
    "history_context",
    "tool_result_context",
    "model_output_context",
    "screen_context",
    "ui_context",
    "market_catalog_context",
    "business_composition_context",
    "audit_context",
    "read_model_context",
    "projection_context",
    "execution_intent_context",
    "attempt_context",
    "lifecycle_context",
    "secret_context",
    "environment_context",
    "external_context",
}
CONTRACTUAL_CONTEXT_TYPES = {
    "user_message_context",
    "system_context",
    "developer_context",
    "agent_instruction_context",
    "domain_context",
    "role_context",
    "specialization_context",
    "task_context",
    "audit_context",
    "execution_intent_context",
}
REDACTION_CONTEXT_TYPES = {"document_context", "retrieved_context", "screen_context", "ui_context"}
SANDBOX_CONTEXT_TYPES = {
    "memory_context",
    "history_context",
    "tool_result_context",
    "model_output_context",
    "market_catalog_context",
    "business_composition_context",
    "read_model_context",
    "projection_context",
    "attempt_context",
    "lifecycle_context",
    "external_context",
}
BLOCKED_CONTEXT_TYPES = {"secret_context", "environment_context"}

CONTEXT_SURFACES = {
    "user_input",
    "system_prompt",
    "developer_prompt",
    "agent_prompt",
    "domain_profile",
    "role_profile",
    "specialization_profile",
    "task_spec",
    "documents",
    "retrieval_index",
    "memory_store",
    "conversation_history",
    "tool_results",
    "model_outputs",
    "screen_content",
    "ui_state",
    "market_catalog",
    "business_composition_layer",
    "execution_intent",
    "execution_attempt",
    "lifecycle_history",
    "read_model",
    "projection",
    "audit_trail",
    "logs",
    "secrets",
    "environment",
    "filesystem",
    "network",
    "api",
    "browser",
    "external_services",
    "stores",
}
CONTRACTUAL_SURFACES = {
    "user_input",
    "system_prompt",
    "developer_prompt",
    "agent_prompt",
    "domain_profile",
    "role_profile",
    "specialization_profile",
    "task_spec",
    "execution_intent",
    "audit_trail",
}
REDACTION_SURFACES = {"documents", "retrieval_index", "conversation_history", "screen_content", "ui_state", "logs"}
SANDBOX_SURFACES = {
    "memory_store",
    "tool_results",
    "model_outputs",
    "market_catalog",
    "business_composition_layer",
    "execution_attempt",
    "lifecycle_history",
    "read_model",
    "projection",
    "filesystem",
    "network",
    "api",
    "browser",
    "external_services",
    "stores",
}
BLOCKED_SURFACES = {"secrets", "environment"}

ALLOWED_ACTIONS = {
    "classify_context_type",
    "classify_context_surface",
    "classify_context_risk",
    "build_context_boundary_decision",
    "evaluate_context_boundary_contract",
    "validate_context_boundary_decision",
    "serialize_context_boundary_decision",
    "generate_context_risk_report",
}
FORBIDDEN_ACTIONS = {
    "build_runtime_context",
    "inject_context",
    "assemble_runtime_prompt",
    "retrieve_context",
    "run_rag",
    "expand_from_memory",
    "expand_from_filesystem",
    "expand_from_web",
    "expand_from_tool_results",
    "expand_from_model_outputs",
    "expand_from_screen",
    "include_secret_in_context",
    "execute_document_instruction",
    "execute_tool_result_instruction",
    "execute_model_output_instruction",
    "log_raw_context",
    "log_raw_prompt",
    "send_context_to_model",
    "send_context_to_provider",
    "persist_context",
    "write_context_store",
    "update_memory_from_context",
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
ALLOWED_DECISIONS = {"allowed_contractually", "requires_redaction", "requires_sandbox", "requires_approval", "blocked", "invalid"}
ALLOWED_READINESS = {"ready_for_context_boundary_e2e_checkpoint", "blocked", "invalid"}
RISK_LEVELS = {"low", "medium", "high", "critical"}

FORBIDDEN_TRUE_FLAGS = {
    "runtime_enabled",
    "context_builder_enabled",
    "context_injection_enabled",
    "context_assembly_enabled",
    "context_retrieval_enabled",
    "context_rag_enabled",
    "memory_expansion_enabled",
    "filesystem_expansion_enabled",
    "web_expansion_enabled",
    "tool_result_expansion_enabled",
    "model_output_expansion_enabled",
    "screen_expansion_enabled",
    "document_execution_enabled",
    "untrusted_instruction_execution_enabled",
    "raw_context_logging_enabled",
    "raw_prompt_assembly_enabled",
    "model_invocation_enabled",
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
class ContextTypeClassification:
    context_type: str
    known: bool
    category: str
    risk_level: str
    requires_redaction: bool
    requires_sandbox: bool
    requires_human_approval: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ContextSurfaceClassification:
    surface: str
    known: bool
    category: str
    operational: bool
    risk_level: str
    blocked_by_default: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ContextRiskClassification:
    context_type: str | None
    surface: str | None
    operation: str | None
    risk_level: str
    forbidden_operation: bool
    requires_redaction: bool
    requires_sandbox: bool
    requires_human_approval: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ContextBoundaryDecision:
    context_boundary_decision_id: str
    status: str
    decision: str
    readiness: str
    context_name: str
    context_type: str
    requested_operation: str
    requested_surface: str
    risk_level: str
    requires_agent_permission: bool
    requires_secrets_policy: bool
    requires_prompt_injection_defense: bool
    requires_sandbox_boundary: bool
    requires_tool_boundary: bool
    requires_model_invocation_boundary: bool
    requires_human_approval: bool
    requires_redaction: bool
    requires_audit: bool
    allowed_to_build_runtime_context: bool
    allowed_to_inject_context: bool
    allowed_to_assemble_prompt: bool
    allowed_to_retrieve: bool
    allowed_to_expand_context: bool
    allowed_to_include_secrets: bool
    allowed_to_execute_embedded_instruction: bool
    allowed_to_send_to_model: bool
    allowed_to_send_to_provider: bool
    allowed_to_log_raw_context: bool
    allowed_to_persist: bool
    allowed_to_update_memory: bool
    allowed_to_use_network: bool
    allowed_to_read_host: bool
    allowed_to_write_host: bool
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


def classify_context_type(context_type_or_name: Any) -> ContextTypeClassification:
    value = "" if context_type_or_name is None else str(context_type_or_name)
    if value in CONTRACTUAL_CONTEXT_TYPES:
        category, risk, redaction, sandbox, approval = "contractual", "low", False, False, False
    elif value in REDACTION_CONTEXT_TYPES:
        category, risk, redaction, sandbox, approval = "redaction_required", "medium", True, False, False
    elif value in SANDBOX_CONTEXT_TYPES:
        category, risk, redaction, sandbox, approval = "sandbox_required", "high", False, True, False
    elif value in BLOCKED_CONTEXT_TYPES:
        category, risk, redaction, sandbox, approval = "blocked_sensitive", "critical", True, True, True
    else:
        category, risk, redaction, sandbox, approval = "unknown", "critical", True, True, True
    return ContextTypeClassification(
        context_type=value,
        known=value in CONTEXT_TYPES,
        category=category,
        risk_level=risk,
        requires_redaction=redaction,
        requires_sandbox=sandbox,
        requires_human_approval=approval,
    )


def classify_context_surface(surface: Any) -> ContextSurfaceClassification:
    value = "" if surface is None else str(surface)
    if value in CONTRACTUAL_SURFACES:
        category, risk, operational = "contractual", "low", False
    elif value in REDACTION_SURFACES:
        category, risk, operational = "redaction_required", "medium", False
    elif value in SANDBOX_SURFACES:
        category, risk, operational = "sandbox_required", "high", True
    elif value in BLOCKED_SURFACES:
        category, risk, operational = "blocked_sensitive", "critical", True
    else:
        category, risk, operational = "unknown", "critical", True
    return ContextSurfaceClassification(
        surface=value,
        known=value in CONTEXT_SURFACES,
        category=category,
        operational=operational,
        risk_level=risk,
        blocked_by_default=True,
    )


def classify_context_risk(context_type: Any = None, surface: Any = None, operation: Any = None) -> ContextRiskClassification:
    type_classification = classify_context_type(context_type)
    surface_classification = classify_context_surface(surface)
    operation_value = "" if operation is None else str(operation)
    forbidden_operation = operation_value in FORBIDDEN_ACTIONS
    requires_redaction = type_classification.requires_redaction or surface_classification.category == "redaction_required"
    requires_sandbox = type_classification.requires_sandbox or surface_classification.operational
    requires_approval = type_classification.requires_human_approval or surface_classification.surface in {"external_services", "stores"}
    risk = _max_risk(
        type_classification.risk_level,
        surface_classification.risk_level,
        "critical" if forbidden_operation else "low",
        "high" if requires_redaction else "low",
    )
    return ContextRiskClassification(
        context_type=type_classification.context_type,
        surface=surface_classification.surface,
        operation=operation_value,
        risk_level=risk,
        forbidden_operation=forbidden_operation,
        requires_redaction=requires_redaction,
        requires_sandbox=requires_sandbox,
        requires_human_approval=requires_approval,
    )


def build_context_boundary_decision(
    *,
    context_boundary_decision_id: str,
    context_name: str,
    context_type: str,
    requested_operation: str,
    requested_surface: str,
    decision: str = "allowed_contractually",
    status: str = "evaluated",
    readiness: str = "ready_for_context_boundary_e2e_checkpoint",
    risk_level: str = "low",
    requires_agent_permission: bool = True,
    requires_secrets_policy: bool = True,
    requires_prompt_injection_defense: bool = True,
    requires_sandbox_boundary: bool = True,
    requires_tool_boundary: bool = True,
    requires_model_invocation_boundary: bool = True,
    requires_human_approval: bool = False,
    requires_redaction: bool = False,
    requires_audit: bool = True,
    allowed_to_build_runtime_context: bool = False,
    allowed_to_inject_context: bool = False,
    allowed_to_assemble_prompt: bool = False,
    allowed_to_retrieve: bool = False,
    allowed_to_expand_context: bool = False,
    allowed_to_include_secrets: bool = False,
    allowed_to_execute_embedded_instruction: bool = False,
    allowed_to_send_to_model: bool = False,
    allowed_to_send_to_provider: bool = False,
    allowed_to_log_raw_context: bool = False,
    allowed_to_persist: bool = False,
    allowed_to_update_memory: bool = False,
    allowed_to_use_network: bool = False,
    allowed_to_read_host: bool = False,
    allowed_to_write_host: bool = False,
    blocking_reasons: list[dict[str, str]] | None = None,
    warnings: list[str] | None = None,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ContextBoundaryDecision:
    return ContextBoundaryDecision(
        context_boundary_decision_id=context_boundary_decision_id,
        status=status,
        decision=decision,
        readiness=readiness,
        context_name=context_name,
        context_type=context_type,
        requested_operation=requested_operation,
        requested_surface=requested_surface,
        risk_level=risk_level,
        requires_agent_permission=requires_agent_permission,
        requires_secrets_policy=requires_secrets_policy,
        requires_prompt_injection_defense=requires_prompt_injection_defense,
        requires_sandbox_boundary=requires_sandbox_boundary,
        requires_tool_boundary=requires_tool_boundary,
        requires_model_invocation_boundary=requires_model_invocation_boundary,
        requires_human_approval=requires_human_approval,
        requires_redaction=requires_redaction,
        requires_audit=requires_audit,
        allowed_to_build_runtime_context=allowed_to_build_runtime_context,
        allowed_to_inject_context=allowed_to_inject_context,
        allowed_to_assemble_prompt=allowed_to_assemble_prompt,
        allowed_to_retrieve=allowed_to_retrieve,
        allowed_to_expand_context=allowed_to_expand_context,
        allowed_to_include_secrets=allowed_to_include_secrets,
        allowed_to_execute_embedded_instruction=allowed_to_execute_embedded_instruction,
        allowed_to_send_to_model=allowed_to_send_to_model,
        allowed_to_send_to_provider=allowed_to_send_to_provider,
        allowed_to_log_raw_context=allowed_to_log_raw_context,
        allowed_to_persist=allowed_to_persist,
        allowed_to_update_memory=allowed_to_update_memory,
        allowed_to_use_network=allowed_to_use_network,
        allowed_to_read_host=allowed_to_read_host,
        allowed_to_write_host=allowed_to_write_host,
        blocking_reasons=list(blocking_reasons or []),
        warnings=list(warnings or []),
        lineage=dict(lineage or {}),
        metadata=dict(metadata or {}),
    )


def evaluate_context_boundary_contract(
    *,
    context_name: str,
    context_type: str,
    requested_operation: str,
    requested_surface: str,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ContextBoundaryDecision:
    type_classification = classify_context_type(context_type)
    surface_classification = classify_context_surface(requested_surface)
    risk = classify_context_risk(context_type, requested_surface, requested_operation)
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []

    _require(context_name, blockers, "missing_context_name", "context_name requerido")
    if not type_classification.known:
        _block(blockers, "unknown_context_type", "context_type desconocido")
    if not surface_classification.known:
        _block(blockers, "unknown_context_surface", "requested_surface desconocida")
    if requested_operation in FORBIDDEN_ACTIONS:
        _block(blockers, "operation_blocked_pre_runtime", "operacion prohibida en pre-runtime")
    if _contains_obliteratus([context_name, context_type, requested_surface, requested_operation, lineage, metadata]):
        _block(blockers, "obliteratus_not_allowed", "OBLITERATUS no es context provider, dependency, adapter ni capability")

    if blockers:
        decision = "invalid" if any(item["code"].startswith(("missing_", "unknown_", "obliteratus")) for item in blockers) else "blocked"
    elif context_type in BLOCKED_CONTEXT_TYPES or requested_surface in BLOCKED_SURFACES:
        decision = "blocked"
        _block(blockers, "sensitive_context_blocked", "contexto sensible bloqueado en pre-runtime")
    elif risk.requires_redaction:
        decision = "requires_redaction"
        warnings.append("redaction_required_no_context_injection_allowed")
    elif risk.requires_human_approval:
        decision = "requires_approval"
        warnings.append("human_approval_required_no_context_injection_allowed")
    elif risk.requires_sandbox:
        decision = "requires_sandbox"
        warnings.append("sandbox_required_contract_only_no_sandbox_created")
    else:
        decision = "allowed_contractually"

    return build_context_boundary_decision(
        context_boundary_decision_id=f"context_boundary_{context_name or 'missing_context'}_{context_type or 'missing_type'}_{requested_operation or 'missing_operation'}",
        context_name=context_name,
        context_type=context_type,
        requested_operation=requested_operation,
        requested_surface=requested_surface,
        decision=decision,
        status="invalid" if decision == "invalid" else "evaluated",
        readiness="ready_for_context_boundary_e2e_checkpoint" if decision not in {"invalid", "blocked"} else "blocked",
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
            "model_invocation_boundary": "active_contractual_boundary",
            "operational_readiness_gate_boundary": "closed",
            **deepcopy(lineage or {}),
        },
        metadata={**_boundary_flags(), **deepcopy(metadata or {})},
    )


def validate_context_boundary_decision(decision: ContextBoundaryDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_context_boundary_decision(decision)
    blockers: list[dict[str, str]] = []

    _require(payload.get("context_boundary_decision_id"), blockers, "missing_context_boundary_decision_id", "context_boundary_decision_id requerido")
    _allowed(payload.get("status"), ALLOWED_STATUSES, blockers, "invalid_status", "status invalido")
    _allowed(payload.get("decision"), ALLOWED_DECISIONS, blockers, "invalid_decision", "decision invalida")
    _allowed(payload.get("readiness"), ALLOWED_READINESS, blockers, "invalid_readiness", "readiness invalida")
    _require(payload.get("context_name"), blockers, "missing_context_name", "context_name requerido")
    _require(payload.get("context_type"), blockers, "missing_context_type", "context_type requerido")
    _require(payload.get("requested_operation"), blockers, "missing_requested_operation", "requested_operation requerida")
    _require(payload.get("requested_surface"), blockers, "missing_requested_surface", "requested_surface requerida")
    _allowed(payload.get("risk_level"), RISK_LEVELS, blockers, "invalid_risk_level", "risk_level invalido")

    for field_name in [
        "requires_agent_permission",
        "requires_secrets_policy",
        "requires_prompt_injection_defense",
        "requires_sandbox_boundary",
        "requires_tool_boundary",
        "requires_model_invocation_boundary",
        "requires_audit",
    ]:
        if payload.get(field_name) is not True:
            _block(blockers, f"{field_name}_required", f"{field_name} debe ser True")
    for field_name in ["requires_human_approval", "requires_redaction"]:
        if not isinstance(payload.get(field_name), bool):
            _block(blockers, f"{field_name}_not_bool", f"{field_name} debe ser bool")
    for field_name in [
        "allowed_to_build_runtime_context",
        "allowed_to_inject_context",
        "allowed_to_assemble_prompt",
        "allowed_to_retrieve",
        "allowed_to_expand_context",
        "allowed_to_include_secrets",
        "allowed_to_execute_embedded_instruction",
        "allowed_to_send_to_model",
        "allowed_to_send_to_provider",
        "allowed_to_log_raw_context",
        "allowed_to_persist",
        "allowed_to_update_memory",
        "allowed_to_use_network",
        "allowed_to_read_host",
        "allowed_to_write_host",
    ]:
        if payload.get(field_name) is not False:
            _block(blockers, f"{field_name}_not_allowed", f"{field_name} debe ser False")
    for field_name in ["blocking_reasons", "warnings"]:
        if not isinstance(payload.get(field_name), list):
            _block(blockers, f"{field_name}_not_list", f"{field_name} debe ser lista")
    for field_name in ["lineage", "metadata"]:
        if not isinstance(payload.get(field_name), dict):
            _block(blockers, f"{field_name}_not_dict", f"{field_name} debe ser dict")

    if payload.get("requested_operation") in FORBIDDEN_ACTIONS and payload.get("decision") not in {"blocked", "invalid"}:
        _block(blockers, "blocked_operation_not_blocked", "operacion prohibida debe quedar blocked o invalid")
    if payload.get("context_type") in BLOCKED_CONTEXT_TYPES and payload.get("decision") not in {"blocked", "invalid"}:
        _block(blockers, "blocked_context_type_not_blocked", "context_type sensible debe quedar blocked o invalid")
    if payload.get("requested_surface") in BLOCKED_SURFACES and payload.get("decision") not in {"blocked", "invalid"}:
        _block(blockers, "blocked_surface_not_blocked", "surface sensible debe quedar blocked o invalid")

    _validate_boundary_flags(payload, blockers)
    if _contains_obliteratus(payload):
        _block(blockers, "obliteratus_not_allowed", "OBLITERATUS no es context provider, dependency, adapter ni capability")

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "CONTEXT_BOUNDARY_READY" if not blockers else "CONTEXT_BOUNDARY_BLOCKED",
        "readiness": "ready_for_context_boundary_e2e_checkpoint" if not blockers else "blocked",
        "blocking_reasons": blockers,
        "warnings": [] if not blockers else ["context_boundary_decision_blocked"],
        "policy_status": CONTEXT_BOUNDARY_STATUS,
        "runtime_enabled": CONTEXT_RUNTIME_ENABLED,
        "context_injection_enabled": CONTEXT_INJECTION_ENABLED,
        "context_retrieval_enabled": CONTEXT_RETRIEVAL_ENABLED,
    }


def serialize_context_boundary_decision(decision: ContextBoundaryDecision | dict[str, Any]) -> dict[str, Any]:
    if isinstance(decision, ContextBoundaryDecision):
        return decision.to_dict()
    return deepcopy(decision)


def generate_context_risk_report(decision: ContextBoundaryDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_context_boundary_decision(decision)
    return {
        "risk": payload.get("risk_level", "medium"),
        "decision": payload.get("decision", "invalid"),
        "context_name": payload.get("context_name"),
        "context_type": payload.get("context_type"),
        "requested_surface": payload.get("requested_surface"),
        "requested_operation": payload.get("requested_operation"),
        "allowed_to_inject_context": False,
        "requires_redaction": bool(payload.get("requires_redaction")),
        "requires_human_approval": bool(payload.get("requires_human_approval")),
    }


def get_context_boundary_contract() -> dict[str, Any]:
    return {
        "status": CONTEXT_BOUNDARY_STATUS,
        "ready": CONTEXT_BOUNDARY_READY,
        "verdict": "CONTEXT_BOUNDARY_READY",
        "readiness": "ready_for_context_boundary_e2e_checkpoint",
        "next_step": "PROMPT 3.28.1 - Checkpoint E2E de context boundary",
        "mode": [
            "contract-only",
            "security-simulated",
            "non-operational",
            "pre-runtime",
            "context-request-only",
            "deny-by-default",
            "permission-aware",
            "secrets-aware",
            "prompt-injection-aware",
            "sandbox-aware",
            "tool-boundary-aware",
            "model-invocation-aware",
            "no real context injection",
        ],
        "central_rule": "En pre-runtime, el contexto puede describirse, clasificarse o evaluarse. Pero no puede inyectarse en una ejecucion real ni enviarse a un modelo real.",
        "context_types": sorted(CONTEXT_TYPES),
        "context_surfaces": sorted(CONTEXT_SURFACES),
        "allowed_actions": sorted(ALLOWED_ACTIONS),
        "forbidden_actions": sorted(FORBIDDEN_ACTIONS),
        "decisions": sorted(ALLOWED_DECISIONS),
        "boundary_flags": _boundary_flags(),
        "agent_permission_boundary": "active_contractual_boundary",
        "secrets_policy_boundary": "active_contractual_boundary",
        "prompt_injection_defense_boundary": "active_contractual_boundary",
        "sandbox_boundary": "active_contractual_boundary",
        "tool_boundary": "active_contractual_boundary",
        "model_invocation_boundary": "active_contractual_boundary",
        "operational_readiness_gate_boundary": "closed",
        "obliteratus": "not_context_provider_not_integration_not_dependency_not_adapter_not_capability",
    }


def _boundary_flags() -> dict[str, bool]:
    return {
        "runtime_enabled": CONTEXT_RUNTIME_ENABLED,
        "context_builder_enabled": CONTEXT_BUILDER_ENABLED,
        "context_injection_enabled": CONTEXT_INJECTION_ENABLED,
        "context_assembly_enabled": CONTEXT_ASSEMBLY_ENABLED,
        "context_retrieval_enabled": CONTEXT_RETRIEVAL_ENABLED,
        "context_rag_enabled": CONTEXT_RAG_ENABLED,
        "memory_expansion_enabled": CONTEXT_MEMORY_EXPANSION_ENABLED,
        "filesystem_expansion_enabled": CONTEXT_FILESYSTEM_EXPANSION_ENABLED,
        "web_expansion_enabled": CONTEXT_WEB_EXPANSION_ENABLED,
        "tool_result_expansion_enabled": CONTEXT_TOOL_RESULT_EXPANSION_ENABLED,
        "model_output_expansion_enabled": CONTEXT_MODEL_OUTPUT_EXPANSION_ENABLED,
        "screen_expansion_enabled": CONTEXT_SCREEN_EXPANSION_ENABLED,
        "document_execution_enabled": CONTEXT_DOCUMENT_EXECUTION_ENABLED,
        "untrusted_instruction_execution_enabled": CONTEXT_UNTRUSTED_INSTRUCTION_EXECUTION_ENABLED,
        "raw_context_logging_enabled": CONTEXT_RAW_CONTEXT_LOGGING_ENABLED,
        "raw_prompt_assembly_enabled": CONTEXT_RAW_PROMPT_ASSEMBLY_ENABLED,
        "model_invocation_enabled": CONTEXT_MODEL_INVOCATION_ENABLED,
        "tool_execution_enabled": CONTEXT_TOOL_EXECUTION_ENABLED,
        "tool_adapters_enabled": CONTEXT_TOOL_ADAPTERS_ENABLED,
        "tool_calls_enabled": CONTEXT_TOOL_CALLS_ENABLED,
        "memory_persistence_enabled": CONTEXT_MEMORY_PERSISTENCE_ENABLED,
        "external_access_enabled": CONTEXT_EXTERNAL_ACCESS_ENABLED,
        "network_enabled": CONTEXT_NETWORK_ENABLED,
        "api_enabled": CONTEXT_API_ENABLED,
        "ui_enabled": CONTEXT_UI_ENABLED,
        "writes_enabled": CONTEXT_WRITES_ENABLED,
        "stores_enabled": CONTEXT_STORES_ENABLED,
        "filesystem_enabled": CONTEXT_FILESYSTEM_ENABLED,
        "command_execution_enabled": CONTEXT_COMMAND_EXECUTION_ENABLED,
        "shell_enabled": CONTEXT_SHELL_ENABLED,
        "process_spawn_enabled": CONTEXT_PROCESS_SPAWN_ENABLED,
        "env_access_enabled": CONTEXT_ENV_ACCESS_ENABLED,
        "secret_access_enabled": CONTEXT_SECRET_ACCESS_ENABLED,
        "host_access_enabled": CONTEXT_HOST_ACCESS_ENABLED,
        "device_access_enabled": CONTEXT_DEVICE_ACCESS_ENABLED,
        "browser_enabled": CONTEXT_BROWSER_ENABLED,
        "clipboard_enabled": CONTEXT_CLIPBOARD_ENABLED,
        "ui_tars_enabled": CONTEXT_UI_TARS_ENABLED,
        "hermes_enabled": CONTEXT_HERMES_ENABLED,
        "n8n_enabled": CONTEXT_N8N_ENABLED,
        "home_assistant_enabled": CONTEXT_HOME_ASSISTANT_ENABLED,
        "market_catalog_runtime_enabled": CONTEXT_MARKET_CATALOG_RUNTIME_ENABLED,
        "business_composition_runtime_enabled": CONTEXT_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
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
