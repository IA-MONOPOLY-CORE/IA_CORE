"""Contract-only output boundary for IA_CORE pre-runtime policy.

This module classifies conceptual output requests and validates boundary
decisions. It never publishes content, sends messages, writes files or stores,
updates memory, calls APIs/webhooks, renders operational UI, leaks secrets,
executes instructions, invokes models, runs tools, or activates integrations.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any


OUTPUT_BOUNDARY_STATUS = "contract_only"
OUTPUT_BOUNDARY_READY = True

OUTPUT_RUNTIME_ENABLED = False
OUTPUT_WRITER_ENABLED = False
OUTPUT_PUBLISHER_ENABLED = False
OUTPUT_NOTIFIER_ENABLED = False
OUTPUT_DELIVERY_ENABLED = False
OUTPUT_MESSAGING_ENABLED = False
OUTPUT_EMAIL_ENABLED = False
OUTPUT_WEBHOOK_ENABLED = False
OUTPUT_API_DELIVERY_ENABLED = False
OUTPUT_UI_DELIVERY_ENABLED = False
OUTPUT_FILE_WRITE_ENABLED = False
OUTPUT_STORE_WRITE_ENABLED = False
OUTPUT_MEMORY_UPDATE_ENABLED = False
OUTPUT_EXTERNAL_DELIVERY_ENABLED = False
OUTPUT_RAW_OUTPUT_LOGGING_ENABLED = False
OUTPUT_SECRET_LEAKAGE_ALLOWED = False
OUTPUT_UNREDACTED_SENSITIVE_DATA_ALLOWED = False
OUTPUT_IRREVERSIBLE_ACTION_ENABLED = False

OUTPUT_CONTEXT_INJECTION_ENABLED = False
OUTPUT_MODEL_INVOCATION_ENABLED = False
OUTPUT_TOOL_EXECUTION_ENABLED = False
OUTPUT_TOOL_ADAPTERS_ENABLED = False
OUTPUT_TOOL_CALLS_ENABLED = False
OUTPUT_MEMORY_PERSISTENCE_ENABLED = False
OUTPUT_EXTERNAL_ACCESS_ENABLED = False
OUTPUT_NETWORK_ENABLED = False
OUTPUT_API_ENABLED = False
OUTPUT_UI_ENABLED = False
OUTPUT_WRITES_ENABLED = False
OUTPUT_STORES_ENABLED = False

OUTPUT_FILESYSTEM_ENABLED = False
OUTPUT_COMMAND_EXECUTION_ENABLED = False
OUTPUT_SHELL_ENABLED = False
OUTPUT_PROCESS_SPAWN_ENABLED = False
OUTPUT_ENV_ACCESS_ENABLED = False
OUTPUT_SECRET_ACCESS_ENABLED = False
OUTPUT_HOST_ACCESS_ENABLED = False
OUTPUT_DEVICE_ACCESS_ENABLED = False
OUTPUT_BROWSER_ENABLED = False
OUTPUT_CLIPBOARD_ENABLED = False

OUTPUT_UI_TARS_ENABLED = False
OUTPUT_HERMES_ENABLED = False
OUTPUT_N8N_ENABLED = False
OUTPUT_HOME_ASSISTANT_ENABLED = False

OUTPUT_MARKET_CATALOG_RUNTIME_ENABLED = False
OUTPUT_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False

OUTPUT_TYPES = {
    "analysis_output",
    "draft_output",
    "summary_output",
    "report_output",
    "recommendation_output",
    "validation_output",
    "classification_output",
    "planning_output",
    "audit_output",
    "read_model_output",
    "projection_output",
    "execution_result_output",
    "tool_result_output",
    "model_output",
    "context_output",
    "user_visible_output",
    "internal_output",
    "debug_output",
    "log_output",
    "notification_output",
    "message_output",
    "email_output",
    "file_output",
    "store_output",
    "memory_update_output",
    "api_response_output",
    "ui_output",
    "workflow_output",
    "publishing_output",
    "payment_output",
    "irreversible_action_output",
    "secret_bearing_output",
    "sensitive_data_output",
    "external_delivery_output",
}
CONTRACTUAL_OUTPUT_TYPES = {
    "analysis_output",
    "draft_output",
    "summary_output",
    "report_output",
    "recommendation_output",
    "validation_output",
    "classification_output",
    "planning_output",
    "audit_output",
    "read_model_output",
    "projection_output",
    "execution_result_output",
    "internal_output",
}
REDACTION_OUTPUT_TYPES = {"tool_result_output", "model_output", "context_output", "user_visible_output", "debug_output", "log_output", "sensitive_data_output"}
SANDBOX_OUTPUT_TYPES = {"file_output", "store_output", "memory_update_output", "api_response_output", "ui_output", "workflow_output", "external_delivery_output"}
APPROVAL_OUTPUT_TYPES = {"notification_output", "message_output", "email_output", "publishing_output", "payment_output"}
BLOCKED_OUTPUT_TYPES = {"irreversible_action_output", "secret_bearing_output"}

OUTPUT_SURFACES = {
    "user_response",
    "internal_report",
    "audit_trail",
    "logs",
    "debug_trace",
    "read_model",
    "projection",
    "execution_result",
    "tool_result",
    "model_result",
    "context_result",
    "file_system",
    "memory_store",
    "database_store",
    "external_api",
    "webhook",
    "email",
    "messaging",
    "notification",
    "ui",
    "browser",
    "clipboard",
    "workflow",
    "scheduler",
    "worker",
    "queue",
    "payment_provider",
    "publishing_channel",
    "external_services",
    "secrets",
    "sensitive_data",
    "host",
    "device",
}
CONTRACTUAL_SURFACES = {"user_response", "internal_report", "audit_trail", "read_model", "projection", "execution_result"}
REDACTION_SURFACES = {"logs", "debug_trace", "tool_result", "model_result", "context_result", "sensitive_data"}
SANDBOX_SURFACES = {"file_system", "memory_store", "database_store", "ui", "browser", "clipboard", "workflow", "scheduler", "worker", "queue", "host", "device"}
APPROVAL_SURFACES = {"external_api", "webhook", "email", "messaging", "notification", "payment_provider", "publishing_channel", "external_services"}
BLOCKED_SURFACES = {"secrets"}

ALLOWED_ACTIONS = {
    "classify_output_type",
    "classify_output_surface",
    "classify_output_risk",
    "build_output_boundary_decision",
    "evaluate_output_boundary_contract",
    "validate_output_boundary_decision",
    "serialize_output_boundary_decision",
    "generate_output_risk_report",
}
FORBIDDEN_ACTIONS = {
    "publish_output",
    "send_output",
    "deliver_output",
    "write_file_output",
    "write_store_output",
    "update_memory_from_output",
    "send_email",
    "send_message",
    "send_notification",
    "call_webhook",
    "call_delivery_api",
    "render_ui_output",
    "copy_to_clipboard",
    "post_to_external_service",
    "publish_content",
    "trigger_workflow",
    "enqueue_output_job",
    "schedule_output_job",
    "send_payment",
    "perform_irreversible_action",
    "log_raw_output",
    "leak_secret",
    "emit_unredacted_sensitive_data",
    "send_output_to_model",
    "send_output_to_provider",
    "execute_output_instruction",
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
}

ALLOWED_STATUSES = {"contract_only", "evaluated", "blocked", "invalid"}
ALLOWED_DECISIONS = {"allowed_contractually", "requires_redaction", "requires_approval", "requires_sandbox", "blocked", "invalid"}
ALLOWED_READINESS = {"ready_for_output_boundary_e2e_checkpoint", "blocked", "invalid"}
RISK_LEVELS = {"low", "medium", "high", "critical"}

FORBIDDEN_TRUE_FLAGS = {
    "runtime_enabled",
    "output_writer_enabled",
    "output_publisher_enabled",
    "output_notifier_enabled",
    "output_delivery_enabled",
    "messaging_enabled",
    "email_enabled",
    "webhook_enabled",
    "api_delivery_enabled",
    "ui_delivery_enabled",
    "file_write_enabled",
    "store_write_enabled",
    "memory_update_enabled",
    "external_delivery_enabled",
    "raw_output_logging_enabled",
    "secret_leakage_allowed",
    "unredacted_sensitive_data_allowed",
    "irreversible_action_enabled",
    "context_injection_enabled",
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
    "market_catalog_runtime_enabled",
    "business_composition_runtime_enabled",
}
FORBIDDEN_STRING_VALUES = {"market_catalog_active", "business_composition_enabled", "gate_open", "operations_enabled", "ready_for_runtime"}
OBLITERATUS_TOKEN = "obliteratus"


@dataclass(frozen=True)
class OutputTypeClassification:
    output_type: str
    known: bool
    category: str
    risk_level: str
    requires_redaction: bool = False
    requires_sandbox: bool = False
    requires_human_approval: bool = False
    blocked_by_default: bool = True


@dataclass(frozen=True)
class OutputSurfaceClassification:
    surface: str
    known: bool
    category: str
    risk_level: str
    operational: bool = True
    external: bool = False
    blocked_by_default: bool = True


@dataclass(frozen=True)
class OutputRiskClassification:
    output_type: str
    surface: str
    operation: str
    risk_level: str
    forbidden_operation: bool
    requires_redaction: bool
    requires_sandbox: bool
    requires_human_approval: bool


@dataclass(frozen=True)
class OutputBoundaryDecision:
    output_boundary_decision_id: str
    status: str
    decision: str
    readiness: str
    output_name: str
    output_type: str
    requested_operation: str
    requested_surface: str
    risk_level: str
    requires_agent_permission: bool = True
    requires_secrets_policy: bool = True
    requires_prompt_injection_defense: bool = True
    requires_sandbox_boundary: bool = True
    requires_tool_boundary: bool = True
    requires_model_invocation_boundary: bool = True
    requires_context_boundary: bool = True
    requires_human_approval: bool = False
    requires_redaction: bool = False
    requires_audit: bool = True
    allowed_to_publish: bool = False
    allowed_to_send: bool = False
    allowed_to_deliver: bool = False
    allowed_to_write_file: bool = False
    allowed_to_write_store: bool = False
    allowed_to_update_memory: bool = False
    allowed_to_call_api: bool = False
    allowed_to_use_network: bool = False
    allowed_to_render_ui: bool = False
    allowed_to_call_webhook: bool = False
    allowed_to_notify: bool = False
    allowed_to_include_secrets: bool = False
    allowed_to_emit_sensitive_data: bool = False
    allowed_to_log_raw_output: bool = False
    allowed_to_trigger_workflow: bool = False
    allowed_to_perform_irreversible_action: bool = False
    blocking_reasons: list[dict[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    lineage: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def classify_output_type(output_type_or_name: str) -> OutputTypeClassification:
    value = (output_type_or_name or "").strip().lower()
    if value in CONTRACTUAL_OUTPUT_TYPES:
        return OutputTypeClassification(value, True, "contractual", "low")
    if value in REDACTION_OUTPUT_TYPES:
        return OutputTypeClassification(value, True, "redaction_required", "high", requires_redaction=True)
    if value in SANDBOX_OUTPUT_TYPES:
        return OutputTypeClassification(value, True, "sandbox_required", "high", requires_sandbox=True)
    if value in APPROVAL_OUTPUT_TYPES:
        return OutputTypeClassification(value, True, "approval_required", "high", requires_human_approval=True)
    if value in BLOCKED_OUTPUT_TYPES:
        return OutputTypeClassification(value, True, "blocked", "critical")
    return OutputTypeClassification(value, False, "unknown", "critical")


def classify_output_surface(surface: str) -> OutputSurfaceClassification:
    value = (surface or "").strip().lower()
    if value in CONTRACTUAL_SURFACES:
        return OutputSurfaceClassification(value, True, "contractual", "low", operational=False)
    if value in REDACTION_SURFACES:
        return OutputSurfaceClassification(value, True, "redaction_required", "high")
    if value in SANDBOX_SURFACES:
        return OutputSurfaceClassification(value, True, "sandbox_required", "high")
    if value in APPROVAL_SURFACES:
        return OutputSurfaceClassification(value, True, "approval_required", "high", external=True)
    if value in BLOCKED_SURFACES:
        return OutputSurfaceClassification(value, True, "blocked", "critical")
    return OutputSurfaceClassification(value, False, "unknown", "critical")


def classify_output_risk(output_type: str | None = None, surface: str | None = None, operation: str | None = None) -> OutputRiskClassification:
    type_classification = classify_output_type(output_type or "")
    surface_classification = classify_output_surface(surface or "")
    operation_value = (operation or "").strip().lower()
    forbidden_operation = operation_value in FORBIDDEN_ACTIONS
    requires_redaction = type_classification.requires_redaction or surface_classification.category == "redaction_required"
    requires_sandbox = type_classification.requires_sandbox or surface_classification.category == "sandbox_required"
    requires_approval = type_classification.requires_human_approval or surface_classification.category == "approval_required"
    risk = _max_risk(
        type_classification.risk_level,
        surface_classification.risk_level,
        "critical" if forbidden_operation else "low",
        "high" if requires_redaction or requires_sandbox or requires_approval else "low",
    )
    return OutputRiskClassification(
        output_type=type_classification.output_type,
        surface=surface_classification.surface,
        operation=operation_value,
        risk_level=risk,
        forbidden_operation=forbidden_operation,
        requires_redaction=requires_redaction,
        requires_sandbox=requires_sandbox,
        requires_human_approval=requires_approval,
    )


def build_output_boundary_decision(
    *,
    output_boundary_decision_id: str,
    output_name: str,
    output_type: str,
    requested_operation: str,
    requested_surface: str,
    decision: str = "allowed_contractually",
    status: str = "evaluated",
    readiness: str = "ready_for_output_boundary_e2e_checkpoint",
    risk_level: str = "low",
    requires_human_approval: bool = False,
    requires_redaction: bool = False,
    blocking_reasons: list[dict[str, str]] | None = None,
    warnings: list[str] | None = None,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> OutputBoundaryDecision:
    return OutputBoundaryDecision(
        output_boundary_decision_id=output_boundary_decision_id,
        status=status,
        decision=decision,
        readiness=readiness,
        output_name=output_name,
        output_type=output_type,
        requested_operation=requested_operation,
        requested_surface=requested_surface,
        risk_level=risk_level,
        requires_human_approval=requires_human_approval,
        requires_redaction=requires_redaction,
        blocking_reasons=deepcopy(blocking_reasons or []),
        warnings=deepcopy(warnings or []),
        lineage={
            "agent_permission_boundary": "active_contractual_boundary",
            "secrets_policy_boundary": "active_contractual_boundary",
            "prompt_injection_defense_boundary": "active_contractual_boundary",
            "sandbox_boundary": "active_contractual_boundary",
            "tool_boundary": "active_contractual_boundary",
            "model_invocation_boundary": "active_contractual_boundary",
            "context_boundary": "active_contractual_boundary",
            "operational_readiness_gate_boundary": "closed",
            **deepcopy(lineage or {}),
        },
        metadata={**_boundary_flags(), **deepcopy(metadata or {})},
    )


def evaluate_output_boundary_contract(
    *,
    output_name: str,
    output_type: str,
    requested_operation: str,
    requested_surface: str,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> OutputBoundaryDecision:
    type_classification = classify_output_type(output_type)
    surface_classification = classify_output_surface(requested_surface)
    risk = classify_output_risk(output_type, requested_surface, requested_operation)
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []

    _require(output_name, blockers, "missing_output_name", "output_name requerido")
    if not type_classification.known:
        _block(blockers, "unknown_output_type", "output_type desconocido")
    if not surface_classification.known:
        _block(blockers, "unknown_output_surface", "requested_surface desconocida")
    if requested_operation in FORBIDDEN_ACTIONS:
        _block(blockers, "operation_blocked_pre_runtime", "operacion prohibida en pre-runtime")
    if _contains_obliteratus([output_name, output_type, requested_surface, requested_operation, lineage, metadata]):
        _block(blockers, "obliteratus_not_allowed", "OBLITERATUS no es output provider, dependency, adapter ni capability")

    if blockers:
        decision = "invalid" if any(item["code"].startswith(("missing_", "unknown_", "obliteratus")) for item in blockers) else "blocked"
    elif output_type in BLOCKED_OUTPUT_TYPES or requested_surface in BLOCKED_SURFACES:
        decision = "blocked"
        _block(blockers, "sensitive_output_blocked", "salida sensible bloqueada en pre-runtime")
    elif risk.requires_redaction:
        decision = "requires_redaction"
        warnings.append("redaction_required_no_output_delivery_allowed")
    elif risk.requires_human_approval:
        decision = "requires_approval"
        warnings.append("human_approval_required_no_output_delivery_allowed")
    elif risk.requires_sandbox:
        decision = "requires_sandbox"
        warnings.append("sandbox_required_contract_only_no_sandbox_created")
    else:
        decision = "allowed_contractually"

    return build_output_boundary_decision(
        output_boundary_decision_id=f"output_boundary_{output_name or 'missing_output'}_{output_type or 'missing_type'}_{requested_operation or 'missing_operation'}",
        output_name=output_name,
        output_type=output_type,
        requested_operation=requested_operation,
        requested_surface=requested_surface,
        decision=decision,
        status="invalid" if decision == "invalid" else "evaluated",
        readiness="ready_for_output_boundary_e2e_checkpoint" if decision not in {"invalid", "blocked"} else "blocked",
        risk_level=risk.risk_level,
        requires_human_approval=risk.requires_human_approval,
        requires_redaction=risk.requires_redaction,
        blocking_reasons=blockers,
        warnings=warnings,
        lineage=lineage,
        metadata=metadata,
    )


def validate_output_boundary_decision(decision: OutputBoundaryDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_output_boundary_decision(decision)
    blockers: list[dict[str, str]] = []

    _require(payload.get("output_boundary_decision_id"), blockers, "missing_output_boundary_decision_id", "output_boundary_decision_id requerido")
    _allowed(payload.get("status"), ALLOWED_STATUSES, blockers, "invalid_status", "status invalido")
    _allowed(payload.get("decision"), ALLOWED_DECISIONS, blockers, "invalid_decision", "decision invalida")
    _allowed(payload.get("readiness"), ALLOWED_READINESS, blockers, "invalid_readiness", "readiness invalida")
    _require(payload.get("output_name"), blockers, "missing_output_name", "output_name requerido")
    _require(payload.get("output_type"), blockers, "missing_output_type", "output_type requerido")
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
        "requires_context_boundary",
        "requires_audit",
    ]:
        if payload.get(field_name) is not True:
            _block(blockers, f"{field_name}_required", f"{field_name} debe ser True")
    for field_name in ["requires_human_approval", "requires_redaction"]:
        if not isinstance(payload.get(field_name), bool):
            _block(blockers, f"{field_name}_not_bool", f"{field_name} debe ser bool")
    for field_name in [
        "allowed_to_publish",
        "allowed_to_send",
        "allowed_to_deliver",
        "allowed_to_write_file",
        "allowed_to_write_store",
        "allowed_to_update_memory",
        "allowed_to_call_api",
        "allowed_to_use_network",
        "allowed_to_render_ui",
        "allowed_to_call_webhook",
        "allowed_to_notify",
        "allowed_to_include_secrets",
        "allowed_to_emit_sensitive_data",
        "allowed_to_log_raw_output",
        "allowed_to_trigger_workflow",
        "allowed_to_perform_irreversible_action",
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
    if payload.get("output_type") in BLOCKED_OUTPUT_TYPES and payload.get("decision") not in {"blocked", "invalid"}:
        _block(blockers, "blocked_output_type_not_blocked", "output_type sensible debe quedar blocked o invalid")
    if payload.get("requested_surface") in BLOCKED_SURFACES and payload.get("decision") not in {"blocked", "invalid"}:
        _block(blockers, "blocked_surface_not_blocked", "surface sensible debe quedar blocked o invalid")

    _validate_boundary_flags(payload, blockers)
    if _contains_obliteratus(payload):
        _block(blockers, "obliteratus_not_allowed", "OBLITERATUS no es output provider, dependency, adapter ni capability")

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "OUTPUT_BOUNDARY_READY" if not blockers else "OUTPUT_BOUNDARY_BLOCKED",
        "readiness": "ready_for_output_boundary_e2e_checkpoint" if not blockers else "blocked",
        "blocking_reasons": blockers,
        "warnings": [] if not blockers else ["output_boundary_decision_blocked"],
        "policy_status": OUTPUT_BOUNDARY_STATUS,
        "runtime_enabled": OUTPUT_RUNTIME_ENABLED,
        "output_delivery_enabled": OUTPUT_DELIVERY_ENABLED,
        "output_publisher_enabled": OUTPUT_PUBLISHER_ENABLED,
    }


def serialize_output_boundary_decision(decision: OutputBoundaryDecision | dict[str, Any]) -> dict[str, Any]:
    if isinstance(decision, OutputBoundaryDecision):
        return decision.to_dict()
    return deepcopy(decision)


def generate_output_risk_report(decision: OutputBoundaryDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_output_boundary_decision(decision)
    return {
        "risk": payload.get("risk_level", "medium"),
        "decision": payload.get("decision", "invalid"),
        "output_name": payload.get("output_name"),
        "output_type": payload.get("output_type"),
        "requested_surface": payload.get("requested_surface"),
        "requested_operation": payload.get("requested_operation"),
        "allowed_to_publish": False,
        "allowed_to_send": False,
        "allowed_to_deliver": False,
        "requires_redaction": bool(payload.get("requires_redaction")),
        "requires_human_approval": bool(payload.get("requires_human_approval")),
    }


def get_output_boundary_contract() -> dict[str, Any]:
    return {
        "status": OUTPUT_BOUNDARY_STATUS,
        "ready": OUTPUT_BOUNDARY_READY,
        "verdict": "OUTPUT_BOUNDARY_READY",
        "readiness": "ready_for_output_boundary_e2e_checkpoint",
        "next_step": "PROMPT 3.29.1 - Checkpoint E2E de output boundary",
        "mode": [
            "contract-only",
            "security-simulated",
            "non-operational",
            "pre-runtime",
            "output-request-only",
            "deny-by-default",
            "permission-aware",
            "secrets-aware",
            "prompt-injection-aware",
            "sandbox-aware",
            "tool-boundary-aware",
            "model-invocation-aware",
            "context-boundary-aware",
            "no real output publishing",
        ],
        "central_rule": "En pre-runtime, una salida puede describirse, clasificarse o evaluarse. Pero no puede publicarse, enviarse, persistirse, entregarse ni convertirse en accion real.",
        "output_types": sorted(OUTPUT_TYPES),
        "output_surfaces": sorted(OUTPUT_SURFACES),
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
        "context_boundary": "active_contractual_boundary",
        "operational_readiness_gate_boundary": "closed",
        "obliteratus": "not_output_provider_not_integration_not_dependency_not_adapter_not_capability",
    }


def _boundary_flags() -> dict[str, bool]:
    return {
        "runtime_enabled": OUTPUT_RUNTIME_ENABLED,
        "output_writer_enabled": OUTPUT_WRITER_ENABLED,
        "output_publisher_enabled": OUTPUT_PUBLISHER_ENABLED,
        "output_notifier_enabled": OUTPUT_NOTIFIER_ENABLED,
        "output_delivery_enabled": OUTPUT_DELIVERY_ENABLED,
        "messaging_enabled": OUTPUT_MESSAGING_ENABLED,
        "email_enabled": OUTPUT_EMAIL_ENABLED,
        "webhook_enabled": OUTPUT_WEBHOOK_ENABLED,
        "api_delivery_enabled": OUTPUT_API_DELIVERY_ENABLED,
        "ui_delivery_enabled": OUTPUT_UI_DELIVERY_ENABLED,
        "file_write_enabled": OUTPUT_FILE_WRITE_ENABLED,
        "store_write_enabled": OUTPUT_STORE_WRITE_ENABLED,
        "memory_update_enabled": OUTPUT_MEMORY_UPDATE_ENABLED,
        "external_delivery_enabled": OUTPUT_EXTERNAL_DELIVERY_ENABLED,
        "raw_output_logging_enabled": OUTPUT_RAW_OUTPUT_LOGGING_ENABLED,
        "secret_leakage_allowed": OUTPUT_SECRET_LEAKAGE_ALLOWED,
        "unredacted_sensitive_data_allowed": OUTPUT_UNREDACTED_SENSITIVE_DATA_ALLOWED,
        "irreversible_action_enabled": OUTPUT_IRREVERSIBLE_ACTION_ENABLED,
        "context_injection_enabled": OUTPUT_CONTEXT_INJECTION_ENABLED,
        "model_invocation_enabled": OUTPUT_MODEL_INVOCATION_ENABLED,
        "tool_execution_enabled": OUTPUT_TOOL_EXECUTION_ENABLED,
        "tool_adapters_enabled": OUTPUT_TOOL_ADAPTERS_ENABLED,
        "tool_calls_enabled": OUTPUT_TOOL_CALLS_ENABLED,
        "memory_persistence_enabled": OUTPUT_MEMORY_PERSISTENCE_ENABLED,
        "external_access_enabled": OUTPUT_EXTERNAL_ACCESS_ENABLED,
        "network_enabled": OUTPUT_NETWORK_ENABLED,
        "api_enabled": OUTPUT_API_ENABLED,
        "ui_enabled": OUTPUT_UI_ENABLED,
        "writes_enabled": OUTPUT_WRITES_ENABLED,
        "stores_enabled": OUTPUT_STORES_ENABLED,
        "filesystem_enabled": OUTPUT_FILESYSTEM_ENABLED,
        "command_execution_enabled": OUTPUT_COMMAND_EXECUTION_ENABLED,
        "shell_enabled": OUTPUT_SHELL_ENABLED,
        "process_spawn_enabled": OUTPUT_PROCESS_SPAWN_ENABLED,
        "env_access_enabled": OUTPUT_ENV_ACCESS_ENABLED,
        "secret_access_enabled": OUTPUT_SECRET_ACCESS_ENABLED,
        "host_access_enabled": OUTPUT_HOST_ACCESS_ENABLED,
        "device_access_enabled": OUTPUT_DEVICE_ACCESS_ENABLED,
        "browser_enabled": OUTPUT_BROWSER_ENABLED,
        "clipboard_enabled": OUTPUT_CLIPBOARD_ENABLED,
        "ui_tars_enabled": OUTPUT_UI_TARS_ENABLED,
        "hermes_enabled": OUTPUT_HERMES_ENABLED,
        "n8n_enabled": OUTPUT_N8N_ENABLED,
        "home_assistant_enabled": OUTPUT_HOME_ASSISTANT_ENABLED,
        "market_catalog_runtime_enabled": OUTPUT_MARKET_CATALOG_RUNTIME_ENABLED,
        "business_composition_runtime_enabled": OUTPUT_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
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
