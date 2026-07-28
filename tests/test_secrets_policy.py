from pathlib import Path

import core.secrets_policy as secrets


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SECRETS_AND_SENSITIVE_DATA_POLICY.md"
FAKE_API_KEY = "API_KEY=fake_api_key_123"
FAKE_BEARER = "Authorization: Bearer fake.token.value"
FAKE_PASSWORD = "PASSWORD=fake_password_123"
FAKE_PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----fake-----END PRIVATE KEY-----"
FAKE_DATABASE_URL = "DATABASE_URL=postgres://fake_user:fake_pass@example.invalid/db"
FAKE_JWT = "JWT=fake.header.payload"


def _decision(**kwargs):
    return secrets.build_secret_policy_decision(
        secret_policy_decision_id="secret_policy_test",
        input_type=kwargs.pop("input_type", "prompt"),
        sensitivity=kwargs.pop("sensitivity", "public"),
        category=kwargs.pop("category", "personal_data"),
        **kwargs,
    )


def test_secrets_policy_module_and_boundaries_exist():
    assert (ROOT / "core" / "secrets_policy.py").exists()
    assert secrets.SECRETS_POLICY_STATUS == "contract_only"
    assert secrets.SECRETS_POLICY_READY is True
    assert secrets.SECRETS_POLICY_RUNTIME_ENABLED is False
    assert secrets.SECRETS_POLICY_SECRET_MANAGER_ENABLED is False
    assert secrets.SECRETS_POLICY_SECRET_READ_ENABLED is False
    assert secrets.SECRETS_POLICY_SECRET_WRITE_ENABLED is False
    assert secrets.SECRETS_POLICY_ENV_SCAN_ENABLED is False
    assert secrets.SECRETS_POLICY_VALUE_EXPOSURE_ENABLED is False
    assert secrets.SECRETS_POLICY_LOGGING_RAW_SECRETS_ENABLED is False
    assert secrets.SECRETS_POLICY_PROMPT_SECRET_INJECTION_ENABLED is False
    assert secrets.SECRETS_POLICY_OUTPUT_SECRET_LEAK_ENABLED is False
    assert secrets.SECRETS_POLICY_MEMORY_PERSISTENCE_ENABLED is False
    assert secrets.SECRETS_POLICY_EXTERNAL_ACCESS_ENABLED is False
    assert secrets.SECRETS_POLICY_API_ENABLED is False
    assert secrets.SECRETS_POLICY_UI_ENABLED is False
    assert secrets.SECRETS_POLICY_WRITES_ENABLED is False
    assert secrets.SECRETS_POLICY_STORES_ENABLED is False
    assert secrets.SECRETS_POLICY_UI_TARS_ENABLED is False
    assert secrets.SECRETS_POLICY_HERMES_ENABLED is False
    assert secrets.SECRETS_POLICY_N8N_ENABLED is False
    assert secrets.SECRETS_POLICY_HOME_ASSISTANT_ENABLED is False
    assert secrets.SECRETS_POLICY_MARKET_CATALOG_RUNTIME_ENABLED is False
    assert secrets.SECRETS_POLICY_BUSINESS_COMPOSITION_RUNTIME_ENABLED is False


def test_classification_detects_public_internal_and_secret_candidates():
    assert secrets.classify_secret_candidate("hello world").sensitivity == "public"
    assert secrets.classify_secret_candidate("internal note", {"internal": True}).sensitivity == "internal"
    for text, category in [
        (FAKE_API_KEY, "api_key"),
        ("ACCESS_TOKEN=fake_access_token", "access_token"),
        ("BEARER_TOKEN=fake_bearer_token", "bearer_token"),
        (FAKE_PASSWORD, "password"),
        (FAKE_PRIVATE_KEY, "private_key"),
        (FAKE_DATABASE_URL, "database_url"),
        (FAKE_JWT, "jwt"),
    ]:
        classification = secrets.classify_secret_candidate(text)
        assert classification.raw_value_present is True
        assert classification.category == category


def test_redaction_removes_fake_sensitive_values_from_text_and_mapping():
    assert "fake_api_key_123" not in secrets.redact_text(FAKE_API_KEY)
    assert "fake.token.value" not in secrets.redact_text(FAKE_BEARER)
    assert "fake_password_123" not in secrets.redact_text(FAKE_PASSWORD)
    assert "-----BEGIN PRIVATE KEY-----" not in secrets.redact_text(FAKE_PRIVATE_KEY)
    mapping = secrets.redact_mapping_values({"DATABASE_URL": FAKE_DATABASE_URL, "safe": "hello"})
    assert mapping["DATABASE_URL"] == "[REDACTED:DATABASE_URL]"
    assert mapping["safe"] == "hello"


def test_secret_policy_decisions_for_public_redacted_and_blocked_cases():
    public = secrets.evaluate_secret_policy_contract(value="hello world", input_type="prompt")
    assert public.decision == "allowed"
    assert public.allowed_to_display is True
    assert secrets.validate_secret_policy_decision(public)["status"] == "validated"

    redacted = secrets.evaluate_secret_policy_contract(value=FAKE_API_KEY, input_type="prompt")
    assert redacted.decision in {"redacted", "blocked"}
    assert "fake_api_key_123" not in (redacted.redacted_value or "")
    assert secrets.validate_secret_policy_decision(redacted)["status"] == "validated"

    blocked = secrets.evaluate_secret_policy_contract(value=FAKE_API_KEY, input_type="memory")
    assert blocked.decision == "blocked"
    assert blocked.allowed_to_persist is False
    assert secrets.validate_secret_policy_decision(blocked)["status"] == "validated"

    invalid = _decision(sensitivity="invalid")
    assert secrets.validate_secret_policy_decision(invalid)["status"] == "blocked"


def test_validation_rejects_sensitive_exposure_and_persistence():
    cases = [
        _decision(sensitivity="secret", category="api_key", allowed_to_display=True),
        _decision(sensitivity="restricted", category="private_key", allowed_to_display=True),
        _decision(sensitivity="secret", category="api_key", allowed_to_prompt=True),
        _decision(sensitivity="restricted", category="private_key", allowed_to_prompt=True),
        _decision(sensitivity="confidential", category="personal_data", allowed_to_persist=True),
        _decision(sensitivity="secret", category="api_key", allowed_to_persist=True),
        _decision(sensitivity="restricted", category="private_key", allowed_to_persist=True),
        _decision(sensitivity="secret", category="api_key", decision="allowed"),
        _decision(sensitivity="secret", category="api_key", raw_value_present=True, decision="allowed"),
    ]
    for decision in cases:
        assert secrets.validate_secret_policy_decision(decision)["status"] == "blocked"


def test_validation_rejects_forbidden_enabled_flags():
    for key in [
        "runtime_enabled",
        "secret_read_enabled",
        "secret_write_enabled",
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
        "market_catalog_active",
        "business_composition_enabled",
    ]:
        payload = secrets.serialize_secret_policy_decision(_decision())
        payload["metadata"][key] = True
        assert secrets.validate_secret_policy_decision(payload)["status"] == "blocked", key


def test_obliteratus_is_not_secret_source_integration_dependency_adapter_or_capability():
    payload = secrets.serialize_secret_policy_decision(_decision())
    payload["metadata"]["source"] = "OBLITERATUS"
    assert secrets.validate_secret_policy_decision(payload)["status"] == "blocked"
    contract = secrets.get_secrets_policy_contract()
    assert contract["obliteratus"] == "not_secret_source_not_integration_not_dependency_not_adapter_not_capability"


def test_policy_document_contains_required_status():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "SECRETS_POLICY_READY",
        "ready_for_secrets_policy_e2e_checkpoint",
        "PROMPT 3.23.1 — Checkpoint E2E de política de secretos",
        "contract-only",
        "security-simulated",
        "non-operational",
        "redaction-first",
        "no secret manager runtime",
        "no secret reads",
        "no secret writes",
        "no environment scanning with values",
        "no raw secret logging",
        "no prompt secret injection",
        "no output secret leaks",
        "no memory persistence",
        "no external access",
        "no API",
        "no UI",
        "no UI-TARS runtime",
        "no Hermes runtime",
        "no n8n real workflows",
        "no Home Assistant real actions",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
        "OBLITERATUS is not an IA_CORE integration",
    ]:
        assert phrase in text
