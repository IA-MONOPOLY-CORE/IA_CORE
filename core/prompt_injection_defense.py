"""Contract-only prompt injection defense for IA_CORE.

This module is input-isolation-first, instruction-hierarchy-aware,
security-simulated and non-operational. It classifies only text explicitly
passed by callers and never executes instructions, calls tools, invokes models,
reads secrets, persists memory, accesses external services, writes stores,
opens UI, or activates integrations.
"""

from __future__ import annotations

import re
import unicodedata
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any


PROMPT_INJECTION_DEFENSE_STATUS = "contract_only"
PROMPT_INJECTION_DEFENSE_READY = True

PROMPT_INJECTION_RUNTIME_ENABLED = False
PROMPT_INJECTION_TOOL_EXECUTION_ENABLED = False
PROMPT_INJECTION_MODEL_INVOCATION_ENABLED = False
PROMPT_INJECTION_MEMORY_PERSISTENCE_ENABLED = False
PROMPT_INJECTION_EXTERNAL_ACCESS_ENABLED = False
PROMPT_INJECTION_API_ENABLED = False
PROMPT_INJECTION_UI_ENABLED = False
PROMPT_INJECTION_WRITES_ENABLED = False
PROMPT_INJECTION_STORES_ENABLED = False

PROMPT_INJECTION_AUTONOMOUS_ACTION_ENABLED = False
PROMPT_INJECTION_UNTRUSTED_INSTRUCTION_EXECUTION_ENABLED = False
PROMPT_INJECTION_TOOL_RESULT_INSTRUCTION_EXECUTION_ENABLED = False
PROMPT_INJECTION_DOCUMENT_INSTRUCTION_EXECUTION_ENABLED = False
PROMPT_INJECTION_SCREEN_INSTRUCTION_EXECUTION_ENABLED = False
PROMPT_INJECTION_WEB_INSTRUCTION_EXECUTION_ENABLED = False

PROMPT_INJECTION_UI_TARS_ENABLED = False
PROMPT_INJECTION_HERMES_ENABLED = False
PROMPT_INJECTION_N8N_ENABLED = False
PROMPT_INJECTION_HOME_ASSISTANT_ENABLED = False

PROMPT_INJECTION_MARKET_CATALOG_RUNTIME_ENABLED = False
PROMPT_INJECTION_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False

UNTRUSTED_SOURCES = {
    "user_message",
    "external_document",
    "uploaded_document",
    "web_page",
    "screen_content",
    "tool_result",
    "email_content",
    "chat_message",
    "clipboard_content",
    "ocr_text",
    "browser_dom",
    "api_response",
    "model_output",
    "retrieved_context",
    "memory_candidate",
    "agent_generated_text",
}
TRUSTED_SOURCE_TYPES = {"system_instruction", "developer_instruction", "internal_contract", "operator_approved"}
SOURCE_TYPES = UNTRUSTED_SOURCES | TRUSTED_SOURCE_TYPES

ATTACK_CATEGORIES = {
    "direct_prompt_injection",
    "indirect_prompt_injection",
    "instruction_override",
    "system_prompt_extraction",
    "developer_prompt_extraction",
    "secret_exfiltration_attempt",
    "tool_hijacking",
    "data_exfiltration",
    "memory_poisoning",
    "role_confusion",
    "authority_impersonation",
    "policy_bypass",
    "jailbreak_attempt",
    "hidden_instruction",
    "encoded_instruction",
    "multilingual_instruction_attack",
    "markdown_instruction_attack",
    "html_instruction_attack",
    "link_based_instruction_attack",
    "prompt_leak_request",
    "approval_bypass",
    "ui_action_hijack",
    "workflow_hijack",
    "agent_delegation_hijack",
}

ALLOWED_ACTIONS = {
    "classify_prompt_injection_candidate",
    "detect_untrusted_instruction",
    "isolate_untrusted_content",
    "sanitize_untrusted_content",
    "build_prompt_injection_decision",
    "evaluate_prompt_injection_contract",
    "validate_prompt_injection_decision",
    "serialize_prompt_injection_decision",
    "generate_prompt_injection_risk_report",
}
FORBIDDEN_ACTIONS = {
    "execute_untrusted_instruction",
    "follow_tool_result_instruction",
    "follow_document_instruction",
    "follow_screen_instruction",
    "follow_web_instruction",
    "override_system_instruction",
    "override_developer_instruction",
    "reveal_system_prompt",
    "reveal_developer_prompt",
    "reveal_secrets",
    "exfiltrate_data",
    "invoke_tool_from_untrusted_content",
    "persist_memory_from_untrusted_content",
    "perform_ui_action_from_untrusted_content",
    "trigger_workflow_from_untrusted_content",
    "delegate_agent_from_untrusted_content",
}

ALLOWED_STATUSES = {"contract_only", "evaluated", "blocked", "invalid"}
ALLOWED_DECISIONS = {"clean", "isolated", "sanitized", "blocked", "invalid"}
ALLOWED_READINESS = {"ready_for_prompt_injection_defense_e2e_checkpoint", "blocked", "invalid"}
TRUST_LEVELS = {"trusted", "partially_trusted", "untrusted", "hostile"}
RISK_LEVELS = {"low", "medium", "high", "critical"}

FORBIDDEN_TRUE_FLAGS = {
    "runtime_enabled",
    "tool_execution_enabled",
    "model_invocation_enabled",
    "memory_persistence_enabled",
    "external_access_enabled",
    "api_enabled",
    "ui_enabled",
    "writes_enabled",
    "stores_enabled",
    "autonomous_action_enabled",
    "untrusted_instruction_execution_enabled",
    "tool_result_instruction_execution_enabled",
    "document_instruction_execution_enabled",
    "screen_instruction_execution_enabled",
    "web_instruction_execution_enabled",
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

PATTERN_RULES: list[tuple[str, str, re.Pattern[str]]] = [
    ("instruction_override", "ignore previous instructions", re.compile(r"ignore (all )?previous instructions", re.I)),
    ("instruction_override", "disregard previous instructions", re.compile(r"disregard previous instructions", re.I)),
    ("instruction_override", "forget your instructions", re.compile(r"forget your instructions", re.I)),
    ("system_prompt_extraction", "reveal your system prompt", re.compile(r"reveal your system prompt", re.I)),
    ("developer_prompt_extraction", "show your developer message", re.compile(r"show your developer message", re.I)),
    ("prompt_leak_request", "print your hidden prompt", re.compile(r"print your hidden prompt", re.I)),
    ("data_exfiltration", "exfiltrate", re.compile(r"\bexfiltrate\b", re.I)),
    ("secret_exfiltration_attempt", "send secrets", re.compile(r"send secrets?", re.I)),
    ("secret_exfiltration_attempt", "send credentials", re.compile(r"send credentials?", re.I)),
    ("secret_exfiltration_attempt", "copy tokens", re.compile(r"copy tokens?", re.I)),
    ("tool_hijacking", "use this tool now", re.compile(r"use this tool now", re.I)),
    ("tool_hijacking", "call the tool", re.compile(r"call the tool", re.I)),
    ("tool_hijacking", "run this command", re.compile(r"run this command", re.I)),
    ("tool_hijacking", "execute this code", re.compile(r"execute this code", re.I)),
    ("ui_action_hijack", "open browser", re.compile(r"open browser", re.I)),
    ("ui_action_hijack", "click this", re.compile(r"click this", re.I)),
    ("link_based_instruction_attack", "download this file", re.compile(r"download this file", re.I)),
    ("memory_poisoning", "write to memory", re.compile(r"write to memory", re.I)),
    ("memory_poisoning", "save this as memory", re.compile(r"save this as memory", re.I)),
    ("policy_bypass", "override policy", re.compile(r"override policy", re.I)),
    ("policy_bypass", "bypass policy", re.compile(r"bypass policy", re.I)),
    ("role_confusion", "you are now", re.compile(r"you are now", re.I)),
    ("authority_impersonation", "act as system", re.compile(r"act as system", re.I)),
    ("authority_impersonation", "developer message says", re.compile(r"developer message says", re.I)),
    ("authority_impersonation", "system message says", re.compile(r"system message says", re.I)),
    ("hidden_instruction", "hidden instruction", re.compile(r"hidden instruction", re.I)),
    ("encoded_instruction", "base64 decode this instruction", re.compile(r"base64 decode this instruction", re.I)),
    ("markdown_instruction_attack", "markdown hidden instruction", re.compile(r"markdown hidden instruction|<!--.*?instruction.*?-->", re.I | re.S)),
    ("html_instruction_attack", "HTML hidden instruction", re.compile(r"html hidden instruction|<[^>]+hidden[^>]*instruction[^>]*>", re.I)),
    ("instruction_override", "ignora las instrucciones anteriores", re.compile(r"ignora las instrucciones anteriores", re.I)),
    ("instruction_override", "olvida tus instrucciones", re.compile(r"olvida tus instrucciones", re.I)),
    ("system_prompt_extraction", "mostra el prompt del sistema", re.compile(r"mostra el prompt del sistema", re.I)),
    ("developer_prompt_extraction", "mostra el mensaje del developer", re.compile(r"mostra el mensaje del developer", re.I)),
    ("prompt_leak_request", "revela tus instrucciones ocultas", re.compile(r"revela tus instrucciones ocultas", re.I)),
    ("secret_exfiltration_attempt", "filtra secretos", re.compile(r"filtra secretos", re.I)),
    ("secret_exfiltration_attempt", "manda credenciales", re.compile(r"manda credenciales", re.I)),
    ("secret_exfiltration_attempt", "copia tokens", re.compile(r"copia tokens", re.I)),
    ("tool_hijacking", "usa esta herramienta", re.compile(r"usa esta herramienta", re.I)),
    ("tool_hijacking", "llama a la herramienta", re.compile(r"llama a la herramienta", re.I)),
    ("tool_hijacking", "ejecuta este comando", re.compile(r"ejecuta este comando", re.I)),
    ("ui_action_hijack", "abri el navegador", re.compile(r"abri el navegador", re.I)),
    ("ui_action_hijack", "hace click", re.compile(r"hace click", re.I)),
    ("memory_poisoning", "guarda esto en memoria", re.compile(r"guarda esto en memoria", re.I)),
    ("policy_bypass", "sobrescribi la politica", re.compile(r"sobrescribi la politica", re.I)),
    ("policy_bypass", "saltate la politica", re.compile(r"saltate la politica", re.I)),
    ("role_confusion", "ahora sos", re.compile(r"ahora sos", re.I)),
    ("authority_impersonation", "actua como system", re.compile(r"actua como system", re.I)),
    ("authority_impersonation", "el mensaje del sistema dice", re.compile(r"el mensaje del sistema dice", re.I)),
    ("hidden_instruction", "instruccion oculta", re.compile(r"instruccion oculta", re.I)),
    ("encoded_instruction", "decodifica esta instruccion", re.compile(r"decodifica esta instruccion", re.I)),
]


@dataclass(frozen=True)
class PromptInjectionClassification:
    source_type: str
    trust_level: str
    attack_category: str | None
    risk_level: str
    untrusted_instruction_detected: bool
    secret_exfiltration_detected: bool
    tool_hijack_detected: bool
    memory_poisoning_detected: bool
    authority_override_detected: bool
    matched_patterns: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PromptInjectionDecision:
    prompt_injection_decision_id: str
    status: str
    decision: str
    readiness: str
    source_type: str
    trust_level: str
    attack_category: str | None
    risk_level: str
    untrusted_instruction_detected: bool
    secret_exfiltration_detected: bool
    tool_hijack_detected: bool
    memory_poisoning_detected: bool
    authority_override_detected: bool
    requires_isolation: bool
    requires_sanitization: bool
    requires_human_review: bool
    allowed_to_execute: bool
    allowed_to_call_tool: bool
    allowed_to_persist_memory: bool
    allowed_to_affect_system_prompt: bool
    allowed_to_affect_developer_prompt: bool
    sanitized_content: str | None
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


def classify_prompt_injection_candidate(
    text: Any,
    source_type: str | None = None,
    context: dict[str, Any] | None = None,
) -> PromptInjectionClassification:
    source = source_type or (context or {}).get("source_type") or "user_message"
    normalized = _normalize_text(text)
    matched: list[str] = []
    category: str | None = None

    for detected_category, label, pattern in PATTERN_RULES:
        if pattern.search(normalized):
            matched.append(label)
            category = category or detected_category

    if source in TRUSTED_SOURCE_TYPES:
        trust_level = "trusted"
    elif source in {"user_message", "agent_generated_text"}:
        trust_level = "partially_trusted"
    elif source in UNTRUSTED_SOURCES:
        trust_level = "untrusted"
    else:
        trust_level = "untrusted"

    if matched and source in {"web_page", "tool_result", "screen_content", "browser_dom"}:
        trust_level = "hostile"
    if (context or {}).get("trust_level") in TRUST_LEVELS:
        trust_level = str((context or {})["trust_level"])
    if (context or {}).get("attack_category") in ATTACK_CATEGORIES:
        category = str((context or {})["attack_category"])

    secret_exfiltration = category in {"secret_exfiltration_attempt", "data_exfiltration", "prompt_leak_request"}
    tool_hijack = category in {"tool_hijacking", "workflow_hijack", "ui_action_hijack", "link_based_instruction_attack"}
    memory_poisoning = category == "memory_poisoning"
    authority_override = category in {
        "instruction_override",
        "authority_impersonation",
        "role_confusion",
        "system_prompt_extraction",
        "developer_prompt_extraction",
        "policy_bypass",
    }

    if trust_level == "hostile":
        risk = "critical"
    elif secret_exfiltration or tool_hijack or memory_poisoning or authority_override:
        risk = "high"
    elif matched:
        risk = "medium"
    else:
        risk = "low"
    if (context or {}).get("risk_level") in RISK_LEVELS:
        risk = str((context or {})["risk_level"])

    return PromptInjectionClassification(
        source_type=source,
        trust_level=trust_level,
        attack_category=category,
        risk_level=risk,
        untrusted_instruction_detected=bool(matched),
        secret_exfiltration_detected=secret_exfiltration,
        tool_hijack_detected=tool_hijack,
        memory_poisoning_detected=memory_poisoning,
        authority_override_detected=authority_override,
        matched_patterns=matched,
    )


def detect_untrusted_instruction(text: Any) -> bool:
    return classify_prompt_injection_candidate(text).untrusted_instruction_detected


def isolate_untrusted_content(text: Any) -> str:
    value = "" if text is None else str(text)
    return f"[UNTRUSTED_CONTENT_AS_DATA]\n{value}\n[/UNTRUSTED_CONTENT_AS_DATA]"


def sanitize_untrusted_content(text: Any) -> str:
    sanitized = _normalize_text(text)
    for _category, label, pattern in PATTERN_RULES:
        sanitized = pattern.sub(f"[REMOVED:{_label_to_token(label)}]", sanitized)
    return sanitized


def build_prompt_injection_decision(
    *,
    prompt_injection_decision_id: str,
    source_type: str,
    trust_level: str,
    attack_category: str | None = None,
    risk_level: str = "low",
    decision: str = "clean",
    status: str = "evaluated",
    readiness: str = "ready_for_prompt_injection_defense_e2e_checkpoint",
    untrusted_instruction_detected: bool = False,
    secret_exfiltration_detected: bool = False,
    tool_hijack_detected: bool = False,
    memory_poisoning_detected: bool = False,
    authority_override_detected: bool = False,
    requires_isolation: bool = True,
    requires_sanitization: bool = True,
    requires_human_review: bool = False,
    allowed_to_execute: bool = False,
    allowed_to_call_tool: bool = False,
    allowed_to_persist_memory: bool = False,
    allowed_to_affect_system_prompt: bool = False,
    allowed_to_affect_developer_prompt: bool = False,
    sanitized_content: str | None = None,
    blocking_reasons: list[dict[str, str]] | None = None,
    warnings: list[str] | None = None,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> PromptInjectionDecision:
    return PromptInjectionDecision(
        prompt_injection_decision_id=prompt_injection_decision_id,
        status=status,
        decision=decision,
        readiness=readiness,
        source_type=source_type,
        trust_level=trust_level,
        attack_category=attack_category,
        risk_level=risk_level,
        untrusted_instruction_detected=untrusted_instruction_detected,
        secret_exfiltration_detected=secret_exfiltration_detected,
        tool_hijack_detected=tool_hijack_detected,
        memory_poisoning_detected=memory_poisoning_detected,
        authority_override_detected=authority_override_detected,
        requires_isolation=requires_isolation,
        requires_sanitization=requires_sanitization,
        requires_human_review=requires_human_review,
        allowed_to_execute=allowed_to_execute,
        allowed_to_call_tool=allowed_to_call_tool,
        allowed_to_persist_memory=allowed_to_persist_memory,
        allowed_to_affect_system_prompt=allowed_to_affect_system_prompt,
        allowed_to_affect_developer_prompt=allowed_to_affect_developer_prompt,
        sanitized_content=sanitized_content,
        blocking_reasons=list(blocking_reasons or []),
        warnings=list(warnings or []),
        lineage=dict(lineage or {}),
        metadata=dict(metadata or {}),
    )


def evaluate_prompt_injection_contract(
    *,
    text: Any,
    source_type: str = "user_message",
    context: dict[str, Any] | None = None,
) -> PromptInjectionDecision:
    classification = classify_prompt_injection_candidate(text, source_type=source_type, context=context)
    isolated = isolate_untrusted_content(text)
    sanitized = sanitize_untrusted_content(text)
    decision = _decision_for(classification)
    blocking_reasons: list[dict[str, str]] = []
    warnings: list[str] = []
    if decision == "blocked":
        _block(blocking_reasons, "untrusted_instruction_blocked", "contenido no confiable no puede ejecutar instrucciones")
    if classification.untrusted_instruction_detected:
        warnings.append("untrusted_instruction_detected")

    return build_prompt_injection_decision(
        prompt_injection_decision_id=f"prompt_injection_{source_type}_{classification.attack_category or 'clean'}",
        source_type=classification.source_type,
        trust_level=classification.trust_level,
        attack_category=classification.attack_category,
        risk_level=classification.risk_level,
        decision=decision,
        status="evaluated",
        untrusted_instruction_detected=classification.untrusted_instruction_detected,
        secret_exfiltration_detected=classification.secret_exfiltration_detected,
        tool_hijack_detected=classification.tool_hijack_detected,
        memory_poisoning_detected=classification.memory_poining_detected if False else classification.memory_poisoning_detected,
        authority_override_detected=classification.authority_override_detected,
        requires_isolation=classification.trust_level != "trusted",
        requires_sanitization=classification.untrusted_instruction_detected,
        requires_human_review=classification.risk_level in {"high", "critical"},
        allowed_to_execute=False,
        allowed_to_call_tool=False,
        allowed_to_persist_memory=False,
        allowed_to_affect_system_prompt=False,
        allowed_to_affect_developer_prompt=False,
        sanitized_content=sanitized if classification.untrusted_instruction_detected else isolated if classification.trust_level != "trusted" else None,
        blocking_reasons=blocking_reasons,
        warnings=warnings,
        lineage={"source_rule": "external_or_retrieved_content_is_data_not_instruction"},
        metadata=_boundary_flags(),
    )


def validate_prompt_injection_decision(decision: PromptInjectionDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_prompt_injection_decision(decision)
    blockers: list[dict[str, str]] = []

    _require(payload.get("prompt_injection_decision_id"), blockers, "missing_prompt_injection_decision_id", "prompt_injection_decision_id requerido")
    _allowed(payload.get("status"), ALLOWED_STATUSES, blockers, "invalid_status", "status invalido")
    _allowed(payload.get("decision"), ALLOWED_DECISIONS, blockers, "invalid_decision", "decision invalida")
    _allowed(payload.get("readiness"), ALLOWED_READINESS, blockers, "invalid_readiness", "readiness invalida")
    _require(payload.get("source_type"), blockers, "missing_source_type", "source_type requerido")
    _allowed(payload.get("trust_level"), TRUST_LEVELS, blockers, "invalid_trust_level", "trust_level invalido")
    _allowed(payload.get("risk_level"), RISK_LEVELS, blockers, "invalid_risk_level", "risk_level invalido")
    if payload.get("attack_category") is not None:
        _allowed(payload.get("attack_category"), ATTACK_CATEGORIES, blockers, "invalid_attack_category", "attack_category invalida")

    for field_name in [
        "blocking_reasons",
        "warnings",
    ]:
        if not isinstance(payload.get(field_name), list):
            _block(blockers, f"{field_name}_not_list", f"{field_name} debe ser lista")
    for field_name in ["lineage", "metadata"]:
        if not isinstance(payload.get(field_name), dict):
            _block(blockers, f"{field_name}_not_dict", f"{field_name} debe ser dict")
    for field_name in [
        "untrusted_instruction_detected",
        "secret_exfiltration_detected",
        "tool_hijack_detected",
        "memory_poisoning_detected",
        "authority_override_detected",
        "requires_isolation",
        "requires_sanitization",
        "requires_human_review",
        "allowed_to_execute",
        "allowed_to_call_tool",
        "allowed_to_persist_memory",
        "allowed_to_affect_system_prompt",
        "allowed_to_affect_developer_prompt",
    ]:
        if not isinstance(payload.get(field_name), bool):
            _block(blockers, f"{field_name}_not_bool", f"{field_name} debe ser booleano")

    if payload.get("untrusted_instruction_detected") is True and payload.get("allowed_to_execute") is True:
        _block(blockers, "untrusted_instruction_execute_not_allowed", "untrusted instruction no puede allowed_to_execute=True")
    if payload.get("secret_exfiltration_detected") is True and payload.get("allowed_to_execute") is True:
        _block(blockers, "secret_exfiltration_execute_not_allowed", "secret exfiltration no puede ejecutar")
    if payload.get("tool_hijack_detected") is True and payload.get("allowed_to_call_tool") is True:
        _block(blockers, "tool_hijack_call_tool_not_allowed", "tool hijack no puede allowed_to_call_tool=True")
    if payload.get("memory_poisoning_detected") is True and payload.get("allowed_to_persist_memory") is True:
        _block(blockers, "memory_poisoning_persist_not_allowed", "memory poisoning no puede persistir memoria")
    if payload.get("authority_override_detected") is True and (
        payload.get("allowed_to_affect_system_prompt") is True or payload.get("allowed_to_affect_developer_prompt") is True
    ):
        _block(blockers, "authority_override_prompt_affect_not_allowed", "authority override no puede afectar system/developer prompt")
    if payload.get("secret_exfiltration_detected") is True and payload.get("decision") == "clean":
        _block(blockers, "secret_exfiltration_clean_not_allowed", "secret exfiltration no puede decision=clean")
    if payload.get("trust_level") == "hostile" and payload.get("decision") == "clean":
        _block(blockers, "hostile_clean_not_allowed", "hostile no puede decision=clean")
    if payload.get("trust_level") == "untrusted" and payload.get("untrusted_instruction_detected") is True and payload.get("decision") == "clean":
        _block(blockers, "untrusted_instruction_clean_not_allowed", "untrusted con instrucciones no puede clean")
    if payload.get("decision") == "clean" and payload.get("attack_category") is not None:
        _block(blockers, "clean_with_attack_category_not_allowed", "clean no puede tener attack_category")
    if payload.get("decision") == "clean" and payload.get("risk_level") in {"high", "critical"}:
        _block(blockers, "clean_high_risk_not_allowed", "clean no puede tener risk high/critical")

    _validate_boundary_flags(payload, blockers)
    if _contains_obliteratus(payload):
        _block(blockers, "obliteratus_not_allowed", "OBLITERATUS no es injection source, integration, dependency, adapter ni capability")

    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "PROMPT_INJECTION_DEFENSE_READY" if not blockers else "PROMPT_INJECTION_DEFENSE_BLOCKED",
        "readiness": "ready_for_prompt_injection_defense_e2e_checkpoint" if not blockers else "blocked",
        "blocking_reasons": blockers,
        "warnings": [] if not blockers else ["prompt_injection_decision_blocked"],
        "policy_status": PROMPT_INJECTION_DEFENSE_STATUS,
        "runtime_enabled": PROMPT_INJECTION_RUNTIME_ENABLED,
        "tool_execution_enabled": PROMPT_INJECTION_TOOL_EXECUTION_ENABLED,
        "model_invocation_enabled": PROMPT_INJECTION_MODEL_INVOCATION_ENABLED,
        "external_access_enabled": PROMPT_INJECTION_EXTERNAL_ACCESS_ENABLED,
    }


def serialize_prompt_injection_decision(decision: PromptInjectionDecision | dict[str, Any]) -> dict[str, Any]:
    if isinstance(decision, PromptInjectionDecision):
        return decision.to_dict()
    return deepcopy(decision)


def generate_prompt_injection_risk_report(decision: PromptInjectionDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_prompt_injection_decision(decision)
    return {
        "risk": payload.get("risk_level", "medium"),
        "decision": payload.get("decision", "invalid"),
        "attack_category": payload.get("attack_category"),
        "runtime_actions_enabled": False,
        "external_access_enabled": False,
        "requires_human_review": bool(payload.get("requires_human_review")),
    }


def get_prompt_injection_defense_contract() -> dict[str, Any]:
    return {
        "status": PROMPT_INJECTION_DEFENSE_STATUS,
        "ready": PROMPT_INJECTION_DEFENSE_READY,
        "verdict": "PROMPT_INJECTION_DEFENSE_READY",
        "readiness": "ready_for_prompt_injection_defense_e2e_checkpoint",
        "next_step": "PROMPT 3.24.1 — Checkpoint E2E de defensa contra prompt injection",
        "mode": ["contract-only", "security-simulated", "non-operational", "input-isolation-first", "instruction-hierarchy-aware"],
        "untrusted_sources": sorted(UNTRUSTED_SOURCES),
        "attack_categories": sorted(ATTACK_CATEGORIES),
        "allowed_actions": sorted(ALLOWED_ACTIONS),
        "forbidden_actions": sorted(FORBIDDEN_ACTIONS),
        "source_rule": "Todo contenido externo o recuperado se trata como dato, no como instruccion, salvo autorizacion explicita futura.",
        "boundary_flags": _boundary_flags(),
        "secrets_policy_boundary": "active_contractual_boundary",
        "agent_permission_boundary": "active_contractual_boundary",
        "obliteratus": "not_injection_source_not_integration_not_dependency_not_adapter_not_capability",
    }


def _decision_for(classification: PromptInjectionClassification) -> str:
    if classification.trust_level == "hostile":
        return "blocked"
    if classification.secret_exfiltration_detected or classification.tool_hijack_detected or classification.memory_poisoning_detected or classification.authority_override_detected:
        return "blocked"
    if classification.untrusted_instruction_detected:
        return "sanitized" if classification.trust_level in {"partially_trusted", "untrusted"} else "isolated"
    if classification.trust_level == "trusted":
        return "clean"
    return "isolated"


def _boundary_flags() -> dict[str, bool]:
    return {
        "runtime_enabled": PROMPT_INJECTION_RUNTIME_ENABLED,
        "tool_execution_enabled": PROMPT_INJECTION_TOOL_EXECUTION_ENABLED,
        "model_invocation_enabled": PROMPT_INJECTION_MODEL_INVOCATION_ENABLED,
        "memory_persistence_enabled": PROMPT_INJECTION_MEMORY_PERSISTENCE_ENABLED,
        "external_access_enabled": PROMPT_INJECTION_EXTERNAL_ACCESS_ENABLED,
        "api_enabled": PROMPT_INJECTION_API_ENABLED,
        "ui_enabled": PROMPT_INJECTION_UI_ENABLED,
        "writes_enabled": PROMPT_INJECTION_WRITES_ENABLED,
        "stores_enabled": PROMPT_INJECTION_STORES_ENABLED,
        "autonomous_action_enabled": PROMPT_INJECTION_AUTONOMOUS_ACTION_ENABLED,
        "untrusted_instruction_execution_enabled": PROMPT_INJECTION_UNTRUSTED_INSTRUCTION_EXECUTION_ENABLED,
        "tool_result_instruction_execution_enabled": PROMPT_INJECTION_TOOL_RESULT_INSTRUCTION_EXECUTION_ENABLED,
        "document_instruction_execution_enabled": PROMPT_INJECTION_DOCUMENT_INSTRUCTION_EXECUTION_ENABLED,
        "screen_instruction_execution_enabled": PROMPT_INJECTION_SCREEN_INSTRUCTION_EXECUTION_ENABLED,
        "web_instruction_execution_enabled": PROMPT_INJECTION_WEB_INSTRUCTION_EXECUTION_ENABLED,
        "ui_tars_enabled": PROMPT_INJECTION_UI_TARS_ENABLED,
        "hermes_enabled": PROMPT_INJECTION_HERMES_ENABLED,
        "n8n_enabled": PROMPT_INJECTION_N8N_ENABLED,
        "home_assistant_enabled": PROMPT_INJECTION_HOME_ASSISTANT_ENABLED,
        "market_catalog_runtime_enabled": PROMPT_INJECTION_MARKET_CATALOG_RUNTIME_ENABLED,
        "business_composition_runtime_enabled": PROMPT_INJECTION_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    }


def _validate_boundary_flags(payload: dict[str, Any], blockers: list[dict[str, str]]) -> None:
    values = [payload, payload.get("metadata", {}), payload.get("lineage", {})]
    for scope in values:
        if isinstance(scope, dict):
            for key, value in scope.items():
                if key in FORBIDDEN_TRUE_FLAGS and value is True:
                    _block(blockers, f"{key}_not_allowed", f"{key}=True no permitido")
    for value in _flatten_values(payload):
        if isinstance(value, str) and value.lower() in FORBIDDEN_STRING_VALUES:
            _block(blockers, "forbidden_state_value", f"valor prohibido: {value}")


def _normalize_text(text: Any) -> str:
    value = "" if text is None else str(text)
    normalized = unicodedata.normalize("NFKD", value)
    without_accents = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return without_accents


def _label_to_token(label: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", _normalize_text(label).upper()).strip("_") or "INSTRUCTION"


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
    blockers.append({"code": code, "message": message})
