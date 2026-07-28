"""Contract-only secrets and sensitive data policy for IA_CORE.

This module is redaction-first, security-simulated and non-operational. It
classifies and redacts values explicitly passed by callers, but it never reads
real secrets, environment variables, .env files, secret managers, external
services, stores, runtime, API or UI.
"""

from __future__ import annotations

import re
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any


SECRETS_POLICY_STATUS = "contract_only"
SECRETS_POLICY_READY = True

SECRETS_POLICY_RUNTIME_ENABLED = False
SECRETS_POLICY_SECRET_MANAGER_ENABLED = False
SECRETS_POLICY_SECRET_READ_ENABLED = False
SECRETS_POLICY_SECRET_WRITE_ENABLED = False
SECRETS_POLICY_ENV_SCAN_ENABLED = False
SECRETS_POLICY_VALUE_EXPOSURE_ENABLED = False
SECRETS_POLICY_LOGGING_RAW_SECRETS_ENABLED = False
SECRETS_POLICY_PROMPT_SECRET_INJECTION_ENABLED = False
SECRETS_POLICY_OUTPUT_SECRET_LEAK_ENABLED = False
SECRETS_POLICY_MEMORY_PERSISTENCE_ENABLED = False
SECRETS_POLICY_EXTERNAL_ACCESS_ENABLED = False
SECRETS_POLICY_API_ENABLED = False
SECRETS_POLICY_UI_ENABLED = False
SECRETS_POLICY_WRITES_ENABLED = False
SECRETS_POLICY_STORES_ENABLED = False

SECRETS_POLICY_UI_TARS_ENABLED = False
SECRETS_POLICY_HERMES_ENABLED = False
SECRETS_POLICY_N8N_ENABLED = False
SECRETS_POLICY_HOME_ASSISTANT_ENABLED = False

SECRETS_POLICY_MARKET_CATALOG_RUNTIME_ENABLED = False
SECRETS_POLICY_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False

SECRET_CATEGORIES = {
    "api_key",
    "access_token",
    "refresh_token",
    "bearer_token",
    "password",
    "private_key",
    "ssh_key",
    "jwt",
    "cookie",
    "session_id",
    "database_url",
    "connection_string",
    "webhook_secret",
    "oauth_client_secret",
    "env_var_sensitive",
    "config_secret",
    "credential_file",
    "personal_data",
    "business_sensitive_data",
    "financial_data",
    "legal_data",
    "health_data",
    "location_data",
    "internal_prompt",
    "system_prompt",
    "developer_prompt",
    "agent_instruction",
    "tool_result_sensitive",
    "screen_sensitive_data",
    "document_sensitive_data",
}
SENSITIVITY_LEVELS = {"public", "internal", "confidential", "secret", "restricted"}
INPUT_TYPES = {"prompt", "log", "output", "memory", "config", "env", "document", "screen", "tool_result", "report"}
ALLOWED_STATUSES = {"contract_only", "evaluated", "blocked", "invalid"}
ALLOWED_DECISIONS = {"allowed", "redacted", "blocked", "invalid"}
ALLOWED_READINESS = {"ready_for_secrets_policy_e2e_checkpoint", "blocked", "invalid"}

ALLOWED_ACTIONS = {
    "classify_secret_candidate",
    "redact_text",
    "redact_mapping_values",
    "detect_placeholder_only",
    "build_secret_policy_decision",
    "validate_secret_policy_decision",
    "serialize_secret_policy_decision",
    "generate_secret_risk_report",
}
FORBIDDEN_ACTIONS = {
    "read_real_secret",
    "write_real_secret",
    "print_secret_value",
    "log_secret_value",
    "persist_secret_value",
    "inject_secret_into_prompt",
    "send_secret_to_external_service",
    "store_secret_in_memory",
    "store_secret_in_history",
    "store_secret_in_read_model",
    "expose_secret_in_output",
    "scan_env_values_operationally",
    "connect_secret_manager",
    "decrypt_secret",
    "rotate_secret_real",
}

SENSITIVE_CATEGORIES = SECRET_CATEGORIES - {"business_sensitive_data"}
SECRET_REPLACEMENTS = {
    "api_key": "[REDACTED:API_KEY]",
    "access_token": "[REDACTED:TOKEN]",
    "refresh_token": "[REDACTED:TOKEN]",
    "bearer_token": "[REDACTED:TOKEN]",
    "password": "[REDACTED:PASSWORD]",
    "private_key": "[REDACTED:PRIVATE_KEY]",
    "ssh_key": "[REDACTED:PRIVATE_KEY]",
    "database_url": "[REDACTED:DATABASE_URL]",
    "connection_string": "[REDACTED:DATABASE_URL]",
    "webhook_secret": "[REDACTED:SECRET]",
    "oauth_client_secret": "[REDACTED:SECRET]",
    "jwt": "[REDACTED:TOKEN]",
    "cookie": "[REDACTED:SECRET]",
    "session_id": "[REDACTED:SECRET]",
    "personal_data": "[REDACTED:PERSONAL_DATA]",
}

PATTERN_RULES: list[tuple[str, str, re.Pattern[str]]] = [
    ("api_key", "[REDACTED:API_KEY]", re.compile(r"\bAPI[_-]?KEY\b\s*[:=]\s*['\"]?[^'\"\s]+", re.I)),
    ("access_token", "[REDACTED:TOKEN]", re.compile(r"\bACCESS[_-]?TOKEN\b\s*[:=]\s*['\"]?[^'\"\s]+", re.I)),
    ("refresh_token", "[REDACTED:TOKEN]", re.compile(r"\bREFRESH[_-]?TOKEN\b\s*[:=]\s*['\"]?[^'\"\s]+", re.I)),
    ("bearer_token", "[REDACTED:TOKEN]", re.compile(r"Authorization:\s*Bearer\s+[A-Za-z0-9._~+\-/=]+", re.I)),
    ("bearer_token", "[REDACTED:TOKEN]", re.compile(r"\bBEARER[_-]?TOKEN\b\s*[:=]\s*['\"]?[^'\"\s]+", re.I)),
    ("password", "[REDACTED:PASSWORD]", re.compile(r"\bPASSWORD\b\s*[:=]\s*['\"]?[^'\"\s]+", re.I)),
    ("private_key", "[REDACTED:PRIVATE_KEY]", re.compile(r"-----BEGIN PRIVATE KEY-----.*?-----END PRIVATE KEY-----", re.I | re.S)),
    ("private_key", "[REDACTED:PRIVATE_KEY]", re.compile(r"\bPRIVATE[_-]?KEY\b\s*[:=]\s*['\"]?[^'\"\s]+", re.I)),
    ("ssh_key", "[REDACTED:PRIVATE_KEY]", re.compile(r"\bSSH[_-]?KEY\b\s*[:=]\s*['\"]?[^'\"\s]+", re.I)),
    ("database_url", "[REDACTED:DATABASE_URL]", re.compile(r"\bDATABASE[_-]?URL\b\s*[:=]\s*['\"]?[^'\"\s]+", re.I)),
    ("connection_string", "[REDACTED:DATABASE_URL]", re.compile(r"\bCONNECTION[_-]?STRING\b\s*[:=]\s*['\"]?[^'\"\s]+", re.I)),
    ("webhook_secret", "[REDACTED:SECRET]", re.compile(r"\bWEBHOOK[_-]?SECRET\b\s*[:=]\s*['\"]?[^'\"\s]+", re.I)),
    ("oauth_client_secret", "[REDACTED:SECRET]", re.compile(r"\bOAUTH[_-]?CLIENT[_-]?SECRET\b\s*[:=]\s*['\"]?[^'\"\s]+", re.I)),
    ("session_id", "[REDACTED:SECRET]", re.compile(r"\bSESSION[_-]?ID\b\s*[:=]\s*['\"]?[^'\"\s]+", re.I)),
    ("cookie", "[REDACTED:SECRET]", re.compile(r"\bCOOKIE\b\s*[:=]\s*['\"]?[^'\"\s]+", re.I)),
    ("jwt", "[REDACTED:TOKEN]", re.compile(r"\bJWT\b\s*[:=]\s*['\"]?[^'\"\s]+", re.I)),
    ("config_secret", "[REDACTED:SECRET]", re.compile(r"\bSECRET\b\s*[:=]\s*['\"]?[^'\"\s]+", re.I)),
    ("env_var_sensitive", "[REDACTED:SECRET]", re.compile(r"\.env", re.I)),
]
FORBIDDEN_TRUE_FLAGS = {
    "runtime_enabled",
    "secret_manager_enabled",
    "secret_read_enabled",
    "secret_write_enabled",
    "env_scan_enabled",
    "value_exposure_enabled",
    "logging_raw_secrets_enabled",
    "prompt_secret_injection_enabled",
    "output_secret_leak_enabled",
    "memory_persistence_enabled",
    "external_access_enabled",
    "api_enabled",
    "ui_enabled",
    "ui_tars_enabled",
    "hermes_enabled",
    "n8n_enabled",
    "home_assistant_enabled",
    "writes_enabled",
    "stores_enabled",
    "market_catalog_active",
    "business_composition_enabled",
    "gate_open",
    "operations_enabled",
}
FORBIDDEN_STRING_VALUES = {"ready_for_runtime", "market_catalog_active", "gate_open", "operations_enabled"}
OBLITERATUS_TOKEN = "obliteratus"


@dataclass(frozen=True)
class SecretClassification:
    sensitivity: str
    category: str
    raw_value_present: bool
    matched_patterns: list[str] = field(default_factory=list)
    placeholder_only: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SecretPolicyDecision:
    secret_policy_decision_id: str
    status: str
    decision: str
    readiness: str
    input_type: str
    sensitivity: str
    category: str
    raw_value_present: bool
    redacted_value: str | None
    allowed_to_display: bool
    allowed_to_persist: bool
    allowed_to_prompt: bool
    requires_redaction: bool
    requires_audit: bool
    requires_human_review: bool
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


def classify_secret_candidate(text_or_key: Any, context: dict[str, Any] | None = None) -> SecretClassification:
    text = "" if text_or_key is None else str(text_or_key)
    matched: list[str] = []
    category = "business_sensitive_data" if (context or {}).get("internal") else "personal_data"
    sensitivity = "internal" if (context or {}).get("internal") else "public"

    for detected_category, _replacement, pattern in PATTERN_RULES:
        if pattern.search(text):
            matched.append(detected_category)
            category = detected_category
            sensitivity = "secret"
            break

    if category in {"private_key", "ssh_key", "database_url", "connection_string"}:
        sensitivity = "restricted"
    if (context or {}).get("sensitivity") in SENSITIVITY_LEVELS:
        sensitivity = str((context or {})["sensitivity"])
    if (context or {}).get("category") in SECRET_CATEGORIES:
        category = str((context or {})["category"])

    return SecretClassification(
        sensitivity=sensitivity,
        category=category,
        raw_value_present=bool(matched),
        matched_patterns=matched,
        placeholder_only=detect_placeholder_only(text),
    )


def detect_placeholder_only(text: Any) -> bool:
    value = "" if text is None else str(text)
    return bool(re.fullmatch(r"\s*(\[REDACTED(?::[A-Z_]+)?\]|<[^>]+>|\$\{[A-Z0-9_]+\})\s*", value))


def redact_text(text: Any, replacement: str = "[REDACTED]") -> str:
    redacted = "" if text is None else str(text)
    for _category, category_replacement, pattern in PATTERN_RULES:
        redacted = pattern.sub(category_replacement or replacement, redacted)
    return redacted


def redact_mapping_values(mapping: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in (mapping or {}).items():
        classification = classify_secret_candidate(key, context={"internal": True})
        value_classification = classify_secret_candidate(value)
        if classification.raw_value_present or value_classification.raw_value_present or _key_looks_sensitive(str(key)):
            result[key] = SECRET_REPLACEMENTS.get(classification.category, SECRET_REPLACEMENTS.get(value_classification.category, "[REDACTED:SECRET]"))
        elif isinstance(value, dict):
            result[key] = redact_mapping_values(value)
        else:
            result[key] = value
    return result


def build_secret_policy_decision(
    *,
    secret_policy_decision_id: str,
    input_type: str,
    sensitivity: str,
    category: str,
    raw_value_present: bool = False,
    redacted_value: str | None = None,
    allowed_to_display: bool = False,
    allowed_to_persist: bool = False,
    allowed_to_prompt: bool = False,
    requires_redaction: bool = True,
    requires_audit: bool = True,
    requires_human_review: bool = False,
    decision: str | None = None,
    status: str = "evaluated",
    readiness: str = "ready_for_secrets_policy_e2e_checkpoint",
    blocking_reasons: list[dict[str, str]] | None = None,
    warnings: list[str] | None = None,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> SecretPolicyDecision:
    resolved_decision = decision or _decision_for(
        input_type=input_type,
        sensitivity=sensitivity,
        raw_value_present=raw_value_present,
        category=category,
    )
    return SecretPolicyDecision(
        secret_policy_decision_id=secret_policy_decision_id,
        status=status,
        decision=resolved_decision,
        readiness=readiness,
        input_type=input_type,
        sensitivity=sensitivity,
        category=category,
        raw_value_present=raw_value_present,
        redacted_value=redacted_value,
        allowed_to_display=allowed_to_display,
        allowed_to_persist=allowed_to_persist,
        allowed_to_prompt=allowed_to_prompt,
        requires_redaction=requires_redaction,
        requires_audit=requires_audit,
        requires_human_review=requires_human_review,
        blocking_reasons=deepcopy(blocking_reasons or []),
        warnings=deepcopy(warnings or []),
        lineage=deepcopy(lineage or {}),
        metadata=deepcopy(metadata or {}),
    )


def evaluate_secret_policy_contract(
    *,
    value: Any,
    input_type: str,
    context: dict[str, Any] | None = None,
    lineage: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> SecretPolicyDecision:
    classification = classify_secret_candidate(value, context=context)
    redacted_value = redact_text(value) if classification.raw_value_present or classification.sensitivity in {"confidential", "secret", "restricted"} else None
    decision = _decision_for(
        input_type=input_type,
        sensitivity=classification.sensitivity,
        raw_value_present=classification.raw_value_present,
        category=classification.category,
    )
    return build_secret_policy_decision(
        secret_policy_decision_id=f"secrets_policy_{input_type}_{classification.category}",
        input_type=input_type,
        sensitivity=classification.sensitivity,
        category=classification.category,
        raw_value_present=classification.raw_value_present,
        redacted_value=redacted_value,
        allowed_to_display=decision == "allowed",
        allowed_to_persist=False,
        allowed_to_prompt=decision == "allowed" and input_type == "prompt",
        requires_redaction=decision in {"redacted", "blocked"},
        requires_audit=True,
        requires_human_review=classification.sensitivity in {"secret", "restricted"},
        decision=decision,
        lineage=deepcopy(lineage or {}),
        metadata={**deepcopy(metadata or {}), "classification": classification.to_dict()},
    )


def validate_secret_policy_decision(decision: SecretPolicyDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_secret_policy_decision(decision)
    blockers: list[dict[str, str]] = []

    _require(payload.get("secret_policy_decision_id"), blockers, "missing_secret_policy_decision_id", "secret_policy_decision_id requerido")
    _allowed(payload.get("status"), ALLOWED_STATUSES, blockers, "invalid_status", "status no permitido")
    _allowed(payload.get("decision"), ALLOWED_DECISIONS, blockers, "invalid_decision", "decision no permitida")
    _allowed(payload.get("readiness"), ALLOWED_READINESS, blockers, "invalid_readiness", "readiness no permitida")
    _allowed(payload.get("input_type"), INPUT_TYPES, blockers, "invalid_input_type", "input_type no permitido")
    _allowed(payload.get("sensitivity"), SENSITIVITY_LEVELS, blockers, "invalid_sensitivity", "sensitivity no permitida")
    _require(payload.get("category"), blockers, "missing_category", "category requerida")
    if payload.get("category") and payload.get("category") not in SECRET_CATEGORIES:
        _block(blockers, "invalid_category", "category no permitida")
    for field_name in ["raw_value_present", "allowed_to_display", "allowed_to_persist", "allowed_to_prompt", "requires_redaction", "requires_audit", "requires_human_review"]:
        if not isinstance(payload.get(field_name), bool):
            _block(blockers, f"invalid_{field_name}", f"{field_name} debe ser booleano")
    if payload.get("requires_audit") is not True:
        _block(blockers, "audit_required", "requires_audit debe ser True")
    for field_name in ["blocking_reasons", "warnings"]:
        if not isinstance(payload.get(field_name), list):
            _block(blockers, f"invalid_{field_name}", f"{field_name} debe ser lista")
    for field_name in ["lineage", "metadata"]:
        if not isinstance(payload.get(field_name), dict):
            _block(blockers, f"invalid_{field_name}", f"{field_name} debe ser dict")

    sensitivity = payload.get("sensitivity")
    category = payload.get("category")
    if sensitivity in {"secret", "restricted"} and payload.get("allowed_to_display") is True:
        _block(blockers, "secret_display_not_allowed", "secret/restricted no puede allowed_to_display=True")
    if sensitivity in {"secret", "restricted"} and payload.get("allowed_to_prompt") is True:
        _block(blockers, "secret_prompt_not_allowed", "secret/restricted no puede allowed_to_prompt=True")
    if sensitivity in {"confidential", "secret", "restricted"} and payload.get("allowed_to_persist") is True:
        _block(blockers, "sensitive_persist_not_allowed", "confidential/secret/restricted no puede persistir")
    if sensitivity in {"secret", "restricted"} and payload.get("raw_value_present") is True and payload.get("decision") not in {"redacted", "blocked"}:
        _block(blockers, "raw_secret_must_be_redacted_or_blocked", "raw secret debe redacted o blocked")
    if sensitivity in {"secret", "restricted"} and payload.get("decision") == "allowed":
        _block(blockers, "secret_allowed_not_allowed", "decision=allowed no permitido para secret/restricted")
    if payload.get("decision") == "allowed" and payload.get("raw_value_present") is True and category in SENSITIVE_CATEGORIES:
        _block(blockers, "raw_sensitive_allowed_not_allowed", "raw sensitive no puede allowed")
    redacted_value = payload.get("redacted_value")
    if isinstance(redacted_value, str):
        redacted_classification = classify_secret_candidate(redacted_value)
        if redacted_classification.raw_value_present:
            _block(blockers, "redacted_value_contains_secret", "redacted_value contiene secreto simulado")

    _scan_forbidden_values(payload, blockers)
    if _contains_obliteratus(payload):
        _block(blockers, "obliteratus_not_allowed", "OBLITERATUS no es secret source, integration, dependency, adapter ni capability")
    _validate_boundary_flags(blockers)
    return {
        "status": "validated" if not blockers else "blocked",
        "verdict": "SECRETS_POLICY_READY" if not blockers else "SECRETS_POLICY_BLOCKED",
        "readiness": "ready_for_secrets_policy_e2e_checkpoint" if not blockers else "blocked",
        "blockers": blockers,
        "warnings": [] if not blockers else ["secret_policy_decision_blocked"],
        "decision": payload,
        "policy_status": SECRETS_POLICY_STATUS,
        "runtime_enabled": SECRETS_POLICY_RUNTIME_ENABLED,
        "secret_read_enabled": SECRETS_POLICY_SECRET_READ_ENABLED,
        "secret_write_enabled": SECRETS_POLICY_SECRET_WRITE_ENABLED,
        "external_access_enabled": SECRETS_POLICY_EXTERNAL_ACCESS_ENABLED,
    }


def serialize_secret_policy_decision(decision: SecretPolicyDecision | dict[str, Any]) -> dict[str, Any]:
    if isinstance(decision, SecretPolicyDecision):
        return decision.to_dict()
    return deepcopy(decision)


def generate_secret_risk_report(decision: SecretPolicyDecision | dict[str, Any]) -> dict[str, Any]:
    payload = serialize_secret_policy_decision(decision)
    return {
        "risk": "high" if payload.get("sensitivity") in {"secret", "restricted"} else "medium",
        "category": payload.get("category"),
        "redaction_required": payload.get("requires_redaction") is True,
        "raw_values_included": False,
    }


def get_secrets_policy_contract() -> dict[str, Any]:
    return {
        "status": SECRETS_POLICY_STATUS,
        "ready": SECRETS_POLICY_READY,
        "verdict": "SECRETS_POLICY_READY",
        "readiness": "ready_for_secrets_policy_e2e_checkpoint",
        "next_step": "PROMPT 3.23.1 — Checkpoint E2E de política de secretos",
        "mode": ["contract-only", "security-simulated", "non-operational", "redaction-first"],
        "categories": sorted(SECRET_CATEGORIES),
        "sensitivity_levels": sorted(SENSITIVITY_LEVELS),
        "allowed_actions": sorted(ALLOWED_ACTIONS),
        "forbidden_actions": sorted(FORBIDDEN_ACTIONS),
        "boundaries": _boundary_flags(),
        "obliteratus": "not_secret_source_not_integration_not_dependency_not_adapter_not_capability",
    }


def _decision_for(*, input_type: str, sensitivity: str, raw_value_present: bool, category: str) -> str:
    if sensitivity in {"secret", "restricted"}:
        return "blocked" if input_type in {"memory", "env", "config"} else "redacted"
    if sensitivity == "confidential":
        return "blocked" if input_type == "memory" else "redacted"
    if raw_value_present and category in SENSITIVE_CATEGORIES:
        return "redacted"
    return "allowed"


def _key_looks_sensitive(key: str) -> bool:
    return any(token in key.upper() for token in ["KEY", "TOKEN", "PASSWORD", "SECRET", "PRIVATE", "DATABASE_URL", "COOKIE", "SESSION"])


def _validate_boundary_flags(blockers: list[dict[str, str]]) -> None:
    for name, value in _boundary_flags().items():
        if value is not False:
            _block(blockers, f"{name}_not_allowed", f"{name} debe ser false")


def _boundary_flags() -> dict[str, bool]:
    return {
        "runtime_enabled": SECRETS_POLICY_RUNTIME_ENABLED,
        "secret_manager_enabled": SECRETS_POLICY_SECRET_MANAGER_ENABLED,
        "secret_read_enabled": SECRETS_POLICY_SECRET_READ_ENABLED,
        "secret_write_enabled": SECRETS_POLICY_SECRET_WRITE_ENABLED,
        "env_scan_enabled": SECRETS_POLICY_ENV_SCAN_ENABLED,
        "value_exposure_enabled": SECRETS_POLICY_VALUE_EXPOSURE_ENABLED,
        "logging_raw_secrets_enabled": SECRETS_POLICY_LOGGING_RAW_SECRETS_ENABLED,
        "prompt_secret_injection_enabled": SECRETS_POLICY_PROMPT_SECRET_INJECTION_ENABLED,
        "output_secret_leak_enabled": SECRETS_POLICY_OUTPUT_SECRET_LEAK_ENABLED,
        "memory_persistence_enabled": SECRETS_POLICY_MEMORY_PERSISTENCE_ENABLED,
        "external_access_enabled": SECRETS_POLICY_EXTERNAL_ACCESS_ENABLED,
        "api_enabled": SECRETS_POLICY_API_ENABLED,
        "ui_enabled": SECRETS_POLICY_UI_ENABLED,
        "writes_enabled": SECRETS_POLICY_WRITES_ENABLED,
        "stores_enabled": SECRETS_POLICY_STORES_ENABLED,
        "ui_tars_enabled": SECRETS_POLICY_UI_TARS_ENABLED,
        "hermes_enabled": SECRETS_POLICY_HERMES_ENABLED,
        "n8n_enabled": SECRETS_POLICY_N8N_ENABLED,
        "home_assistant_enabled": SECRETS_POLICY_HOME_ASSISTANT_ENABLED,
        "market_catalog_runtime_enabled": SECRETS_POLICY_MARKET_CATALOG_RUNTIME_ENABLED,
        "business_composition_runtime_enabled": SECRETS_POLICY_BUSINESS_COMPOSITION_RUNTIME_ENABLED,
    }


def _scan_forbidden_values(value: Any, blockers: list[dict[str, str]]) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in FORBIDDEN_TRUE_FLAGS and item is True:
                _block(blockers, f"{key}_not_allowed", f"{key}=true no permitido")
            _scan_forbidden_values(item, blockers)
    elif isinstance(value, list):
        for item in value:
            _scan_forbidden_values(item, blockers)
    elif isinstance(value, str) and value in FORBIDDEN_STRING_VALUES:
        _block(blockers, f"{value}_not_allowed", f"{value} no permitido")


def _contains_obliteratus(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_obliteratus(k) or _contains_obliteratus(v) for k, v in value.items())
    if isinstance(value, list | tuple | set):
        return any(_contains_obliteratus(item) for item in value)
    return isinstance(value, str) and OBLITERATUS_TOKEN in value.lower()


def _require(value: Any, blockers: list[dict[str, str]], code: str, message: str) -> None:
    if value in (None, "", {}, []):
        _block(blockers, code, message)


def _allowed(value: Any, allowed: set[str], blockers: list[dict[str, str]], code: str, message: str) -> None:
    if value not in allowed:
        _block(blockers, code, message)


def _block(blockers: list[dict[str, str]], code: str, message: str) -> None:
    blocker = {"code": code, "message": message, "severity": "error"}
    if blocker not in blockers:
        blockers.append(blocker)
