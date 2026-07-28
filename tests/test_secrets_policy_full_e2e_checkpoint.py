from pathlib import Path

import core.secrets_policy as secrets


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SECRETS_POLICY_FULL_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def _decision(**kwargs):
    return secrets.build_secret_policy_decision(
        secret_policy_decision_id="secrets_policy_full_e2e_test",
        input_type=kwargs.pop("input_type", "prompt"),
        sensitivity=kwargs.pop("sensitivity", "public"),
        category=kwargs.pop("category", "personal_data"),
        **kwargs,
    )


def test_full_e2e_checkpoint_doc_exists_and_declares_status():
    text = _text()
    assert DOC.exists()
    for phrase in [
        "SECRETS_POLICY_FULL_E2E_PASSED",
        "SECRETS_POLICY_CHAIN_READY",
        "ready_for_prompt_injection_defense_planning",
        "PROMPT 3.24 — Defensa contra prompt injection",
    ]:
        assert phrase in text


def test_full_e2e_checkpoint_contains_required_chain_and_explanation():
    text = _text()
    for phrase in [
        "Security Surface Audit",
        "Agent Permission Contract",
        "Agent Permission Full E2E",
        "Secrets and Sensitive Data Policy",
        "Secret classification",
        "Secret redaction",
        "Secret policy decision",
        "allowed/redacted/blocked/invalid",
        "no raw secret exposure",
        "no secret reads reales",
        "no secret writes reales",
        "no env scan con valores",
        "no secret manager runtime",
        "no memory persistence",
        "no external access",
        "no API/UI",
        "no future integrations active",
        "El agente puede tener permiso para preparar o leer documentación",
        "Pero eso no le permite exponer secretos",
        "La política de secretos clasifica, redacta o bloquea",
        "allowed no expone secretos",
        "redacted oculta valores sensibles",
        "blocked impide exposición o persistencia",
        "invalid rechaza decisiones inseguras",
        "Nada lee secretos reales",
        "Nada escribe secretos reales",
        "Nada activa runtime",
    ]:
        assert phrase in text


def test_full_e2e_checkpoint_contains_verifications_and_scenarios():
    text = _text()
    for phrase in [
        "Secrets Policy E2E",
        "contract_only",
        "redaction-first",
        "secret manager runtime",
        "secret reads reales",
        "secret writes reales",
        "env scan con valores",
        "raw secret logging",
        "prompt secret injection",
        "output secret leak",
        "memory persistence",
        "external access",
        "API/UI",
        "writes/stores operativos",
        "texto público",
        "texto interno",
        "API_KEY",
        "token",
        "password",
        "private key",
        "database URL",
        "redacta texto sensible fake",
        "redacta mapping",
        "raw secret simulado",
        "decisión allowed",
        "decisión redacted",
        "decisión blocked",
        "decisión invalid",
        "allowed_to_display=True",
        "allowed_to_prompt=True",
        "allowed_to_persist=True",
        "decision=allowed con secret",
        "raw_value_present=True",
        "serialización no contiene raw secret values",
        "valores fake",
        "docs no contienen claves reales",
        "Market Catalog sigue `planned_not_active`",
        "Business Composition Layer sigue futura/no operativa",
        "OBLITERATUS no es secret source/integration/dependency/adapter/capability",
    ]:
        assert phrase in text

    for scenario in [
        "texto público sin secreto",
        "texto interno sin secreto",
        "texto con API_KEY fake",
        "texto con ACCESS_TOKEN fake",
        "texto con BEARER_TOKEN fake",
        "texto con PASSWORD fake",
        "texto con PRIVATE_KEY fake",
        "texto con DATABASE_URL fake",
        "texto con JWT fake",
        "mapping con valores sensibles fake",
        "prompt con secret fake",
        "log con secret fake",
        "output con secret fake",
        "memory con confidential",
        "memory con secret",
        "env/config con secret",
        "document con sensitive data",
        "screen con sensitive data",
        "tool_result con sensitive data",
        "secret con allowed_to_display True forzado",
        "restricted con allowed_to_display True forzado",
        "secret con allowed_to_prompt True forzado",
        "restricted con allowed_to_prompt True forzado",
        "confidential con allowed_to_persist True forzado",
        "secret con allowed_to_persist True forzado",
        "decision allowed con secret forzado",
        "raw_value_present secret allowed forzado",
        "runtime_enabled true forzado",
        "secret_read_enabled true forzado",
        "secret_write_enabled true forzado",
        "value_exposure_enabled true forzado",
        "logging_raw_secrets_enabled true forzado",
        "prompt_secret_injection_enabled true forzado",
        "output_secret_leak_enabled true forzado",
        "memory_persistence_enabled true forzado",
        "external_access_enabled true forzado",
        "ui_tars_enabled true forzado",
        "hermes_enabled true forzado",
        "n8n_enabled true forzado",
        "home_assistant_enabled true forzado",
        "market_catalog_active forzado",
        "business_composition_enabled true forzado",
        "OBLITERATUS como source/integration",
    ]:
        assert scenario in text


def test_full_e2e_checkpoint_contains_boundaries_and_no_contradictions():
    text = _text()
    for phrase in [
        "SECRETS_POLICY_STATUS = contract_only",
        "SECRETS_POLICY_RUNTIME_ENABLED = False",
        "SECRETS_POLICY_SECRET_MANAGER_ENABLED = False",
        "SECRETS_POLICY_SECRET_READ_ENABLED = False",
        "SECRETS_POLICY_SECRET_WRITE_ENABLED = False",
        "SECRETS_POLICY_ENV_SCAN_ENABLED = False",
        "SECRETS_POLICY_VALUE_EXPOSURE_ENABLED = False",
        "SECRETS_POLICY_LOGGING_RAW_SECRETS_ENABLED = False",
        "SECRETS_POLICY_PROMPT_SECRET_INJECTION_ENABLED = False",
        "SECRETS_POLICY_OUTPUT_SECRET_LEAK_ENABLED = False",
        "SECRETS_POLICY_MEMORY_PERSISTENCE_ENABLED = False",
        "SECRETS_POLICY_EXTERNAL_ACCESS_ENABLED = False",
        "SECRETS_POLICY_API_ENABLED = False",
        "SECRETS_POLICY_UI_ENABLED = False",
        "SECRETS_POLICY_WRITES_ENABLED = False",
        "SECRETS_POLICY_STORES_ENABLED = False",
        "SECRETS_POLICY_UI_TARS_ENABLED = False",
        "SECRETS_POLICY_HERMES_ENABLED = False",
        "SECRETS_POLICY_N8N_ENABLED = False",
        "SECRETS_POLICY_HOME_ASSISTANT_ENABLED = False",
        "SECRETS_POLICY_MARKET_CATALOG_RUNTIME_ENABLED = False",
        "SECRETS_POLICY_BUSINESS_COMPOSITION_RUNTIME_ENABLED = False",
        "no writes reales",
        "no stores operativos",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
        "OBLITERATUS is not an IA_CORE integration",
    ]:
        assert phrase in text

    for forbidden in [
        "runtime_enabled = true",
        "secret_manager_enabled = true",
        "secret_read_enabled = true",
        "secret_write_enabled = true",
        "value_exposure_enabled = true",
        "logging_raw_secrets_enabled = true",
        "prompt_secret_injection_enabled = true",
        "output_secret_leak_enabled = true",
        "memory_persistence_enabled = true",
        "external_access_enabled = true",
        "api_enabled = true",
        "ui_enabled = true",
        "ui_tars_enabled = true",
        "hermes_enabled = true",
        "n8n_enabled = true",
        "home_assistant_enabled = true",
        "business_composition_enabled = true",
        "gate_open",
        "operations_enabled",
        "ready_for_runtime",
    ]:
        assert forbidden not in text


def test_secrets_policy_import_boundaries_remain_disabled():
    assert secrets.SECRETS_POLICY_STATUS == "contract_only"
    for name in [
        "SECRETS_POLICY_RUNTIME_ENABLED",
        "SECRETS_POLICY_SECRET_MANAGER_ENABLED",
        "SECRETS_POLICY_SECRET_READ_ENABLED",
        "SECRETS_POLICY_SECRET_WRITE_ENABLED",
        "SECRETS_POLICY_ENV_SCAN_ENABLED",
        "SECRETS_POLICY_VALUE_EXPOSURE_ENABLED",
        "SECRETS_POLICY_LOGGING_RAW_SECRETS_ENABLED",
        "SECRETS_POLICY_PROMPT_SECRET_INJECTION_ENABLED",
        "SECRETS_POLICY_OUTPUT_SECRET_LEAK_ENABLED",
        "SECRETS_POLICY_MEMORY_PERSISTENCE_ENABLED",
        "SECRETS_POLICY_EXTERNAL_ACCESS_ENABLED",
        "SECRETS_POLICY_API_ENABLED",
        "SECRETS_POLICY_UI_ENABLED",
        "SECRETS_POLICY_WRITES_ENABLED",
        "SECRETS_POLICY_STORES_ENABLED",
        "SECRETS_POLICY_UI_TARS_ENABLED",
        "SECRETS_POLICY_HERMES_ENABLED",
        "SECRETS_POLICY_N8N_ENABLED",
        "SECRETS_POLICY_HOME_ASSISTANT_ENABLED",
        "SECRETS_POLICY_MARKET_CATALOG_RUNTIME_ENABLED",
        "SECRETS_POLICY_BUSINESS_COMPOSITION_RUNTIME_ENABLED",
    ]:
        assert getattr(secrets, name) is False


def test_safe_and_sensitive_decisions_do_not_enable_runtime_or_expose_raw_values():
    safe = secrets.evaluate_secret_policy_contract(value="texto público sin secreto", input_type="prompt")
    assert safe.decision == "allowed"
    assert safe.allowed_to_display is True
    assert safe.allowed_to_persist is False
    validation = secrets.validate_secret_policy_decision(safe)
    assert validation["runtime_enabled"] is False
    assert validation["external_access_enabled"] is False

    fake_values = [
        ("API_KEY=fake_api_key_full_e2e", "fake_api_key_full_e2e"),
        ("PASSWORD=fake_password_full_e2e", "fake_password_full_e2e"),
        ("-----BEGIN PRIVATE KEY-----fake-private-----END PRIVATE KEY-----", "fake-private"),
    ]
    for raw, needle in fake_values:
        decision = secrets.evaluate_secret_policy_contract(value=raw, input_type="prompt")
        assert decision.decision in {"redacted", "blocked"}
        assert needle not in (decision.redacted_value or "")
        assert decision.allowed_to_persist is False
        if decision.sensitivity in {"secret", "restricted"}:
            assert decision.allowed_to_display is False
            assert decision.allowed_to_prompt is False
        payload = secrets.serialize_secret_policy_decision(decision)
        assert needle not in str(payload)
        validation = secrets.validate_secret_policy_decision(payload)
        assert validation["status"] == "validated"
        assert validation["runtime_enabled"] is False
        assert validation["external_access_enabled"] is False


def test_rejects_insecure_secret_decisions_and_forbidden_flags():
    rejected_decisions = [
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
    for decision in rejected_decisions:
        assert secrets.validate_secret_policy_decision(decision)["status"] == "blocked"

    for key in [
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
        "market_catalog_active",
        "business_composition_enabled",
    ]:
        payload = secrets.serialize_secret_policy_decision(_decision())
        payload["metadata"][key] = True
        assert secrets.validate_secret_policy_decision(payload)["status"] == "blocked", key

    payload = secrets.serialize_secret_policy_decision(_decision())
    payload["metadata"]["source"] = "OBLITERATUS"
    assert secrets.validate_secret_policy_decision(payload)["status"] == "blocked"


def test_no_new_operational_security_or_integration_modules_exist():
    for relative in [
        "core/security_layer.py",
        "core/secret_manager.py",
        "core/vault.py",
        "core/runtime_runner.py",
        "core/scheduler.py",
        "core/worker.py",
        "core/queue.py",
        "core/tool_executor.py",
        "core/model_invoker.py",
        "core/ui_tars_adapter.py",
        "core/hermes_adapter.py",
        "core/n8n_adapter.py",
        "core/home_assistant_adapter.py",
    ]:
        assert not (ROOT / relative).exists(), relative
