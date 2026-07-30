from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "IA_CORE_SECURITY_LAYER_PLAN.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_security_layer_plan_exists_and_declares_ready_state():
    text = _text()

    assert DOC.exists()
    for phrase in [
        "IA_CORE Security Layer — Planning Document",
        "IA_CORE_SECURITY_LAYER_PLAN_READY",
        "SECURITY_LAYER_REQUIRED_BEFORE_RUNTIME",
        "ready_for_security_surface_audit",
        "PROMPT 3.21 — Auditoría de superficie de ataque de IA_CORE",
    ]:
        assert phrase in text


def test_security_layer_plan_contains_strategic_decision():
    text = _text()

    for phrase in [
        "IA_CORE no activa runtime real sin Security Layer previa",
        "seguridad antes de runtime",
    ]:
        assert phrase in text


def test_security_layer_plan_contains_ten_mandatory_blocks():
    text = _text()

    for phrase in [
        "Auditoría de superficie de ataque",
        "Contrato de permisos por agente",
        "Política de secretos",
        "Defensa contra prompt injection",
        "Sandbox obligatorio para tools",
        "Logs/audit trail inmutables",
        "Kill switch",
        "Simulaciones internas controladas",
        "Reportes de riesgo",
        "Checkpoint E2E de seguridad antes de activar runtime",
    ]:
        assert phrase in text


def test_security_layer_plan_contains_future_prompt_sequence():
    text = _text()

    for phrase in [
        "PROMPT 3.21 — Auditoría de superficie de ataque de IA_CORE",
        "PROMPT 3.22 — Contrato de permisos por agente",
        "PROMPT 3.23 — Política de secretos y datos sensibles",
        "PROMPT 3.24 — Defensa contra prompt injection",
        "PROMPT 3.25 — Sandbox obligatorio para tools",
        "PROMPT 3.26 — Audit trail / logs inmutables",
        "PROMPT 3.27 — Kill switch contract",
        "PROMPT 3.28 — Simulaciones internas controladas",
        "PROMPT 3.29 — Reportes de riesgo de Security Layer",
        "PROMPT 3.30 — Checkpoint E2E Security Layer before runtime",
    ]:
        assert phrase in text


def test_security_layer_plan_documents_future_integrations_and_obliteratus_boundary():
    text = _text()

    for phrase in [
        "UI-TARS",
        "Hermes",
        "n8n",
        "Home Assistant",
        "OBLITERATUS",
        "OBLITERATUS no es integración de IA_CORE",
        "no debe incorporarse como dependencia",
        "no debe formar parte del roadmap operativo",
    ]:
        assert phrase in text


def test_security_layer_plan_contains_conceptual_hierarchy():
    text = _text()

    for phrase in [
        "Santi = dueño/director humano",
        "IA_CORE = gobierno del sistema",
        "Security Layer = control, riesgo y seguridad",
        "UI-TARS = futura autoridad operativa GUI",
        "Hermes = futura herramienta/orquestador operativo subordinado",
        "n8n = futura herramienta de workflows",
        "Home Assistant = futura capa física/local",
    ]:
        assert phrase in text


def test_security_layer_plan_contains_initial_threat_model():
    text = _text()

    for phrase in [
        "prompt injection",
        "jailbreak attempts",
        "tool abuse",
        "permission bypass",
        "secret leakage",
        "memory poisoning",
        "document injection",
        "webpage/UI injection",
        "malicious screenshots",
        "malicious external content",
        "unsafe writes",
        "store corruption",
        "lineage tampering",
        "audit trail tampering",
        "runtime activation bypass",
        "scheduler/worker/queue misuse",
        "model invocation misuse",
        "tool execution outside permissions",
        "external access outside permissions",
        "UI-TARS unauthorized actions",
        "Hermes unauthorized orchestration",
        "n8n workflow abuse",
        "Home Assistant physical-world unsafe actions",
        "approval bypass",
        "human-in-the-loop bypass",
        "rollback failure",
        "kill switch failure",
        "Market Catalog activation bypass",
        "Business Composition Layer activation bypass",
    ]:
        assert phrase in text


def test_security_layer_plan_contains_security_principles():
    text = _text()

    for phrase in [
        "default deny",
        "least privilege",
        "explicit permissions",
        "contract-first",
        "sandbox-first",
        "human approval for irreversible actions",
        "no secrets in prompts",
        "no secrets in logs",
        "immutable audit trail",
        "idempotency for sensitive actions",
        "rollback or compensation policy",
        "kill switch always available",
        "separation between planning and execution",
        "no runtime without Security Layer",
        "no external access without Security Layer",
        "no UI operator without sandbox and approval",
        "no physical action without approval and safety policy",
    ]:
        assert phrase in text


def test_security_layer_plan_connects_to_foundation():
    text = _text()

    for phrase in [
        "ExecutionIntent",
        "Attempt factory",
        "Attempt store write-safe",
        "Lifecycle writer",
        "OperationalReadinessGate",
        "contract-only/cerrado",
        "La Security Layer no reemplaza la foundation",
    ]:
        assert phrase in text


def test_security_layer_plan_contains_defensive_red_team_scope():
    text = _text()

    for phrase in [
        "Defensive Red Team",
        "Adversarial Lab",
        "jailbreak tests",
        "prompt injection tests",
        "permission bypass tests",
        "secret leakage tests",
        "tool abuse tests",
        "memory poisoning tests",
        "malicious document tests",
        "malicious webpage/UI tests",
        "agent boundary regression tests",
    ]:
        assert phrase in text


def test_security_layer_plan_contains_explicit_red_team_prohibitions():
    text = _text()

    for phrase in [
        "ataques contra terceros",
        "exfiltración real",
        "bypass operativo sobre servicios externos",
        "uso ofensivo fuera de sandbox",
        "uso para romper restricciones de modelos con fines dañinos",
    ]:
        assert phrase in text


def test_security_layer_plan_declares_blocked_boundaries():
    text = _text()

    for phrase in [
        "runtime execution",
        "scheduler",
        "worker",
        "queue",
        "model invocation",
        "tool execution",
        "memory persistence",
        "external access",
        "API",
        "UI",
        "UI-TARS runtime",
        "Hermes runtime",
        "n8n workflows reales",
        "Home Assistant actions reales",
        "attempt store writes reales",
        "lifecycle events reales",
        "lifecycle_store writes",
        "result store writes",
        "history writes",
        "read model writes",
        "projection writes",
        "Market Catalog runtime",
        "Business Composition Layer runtime",
    ]:
        assert phrase in text


def test_security_layer_plan_did_not_create_operational_modules():
    for relative in [
        "core/security_layer.py",
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


def test_security_layer_plan_has_no_contradictory_enabled_states():
    text = _text()

    for forbidden in [
        "runtime_enabled = true",
        "security_layer_enabled = true",
        "tools_enabled = true",
        "memory_persistence_enabled = true",
        "external_access_enabled = true",
        "ui_tars_enabled = true",
        "hermes_enabled = true",
        "n8n_enabled = true",
        "home_assistant_enabled = true",
        "market_catalog_active",
        "business_composition_enabled = true",
        "gate_open",
        "operations_enabled",
        "ready_for_runtime`",
    ]:
        assert forbidden not in text


def test_prior_docs_reference_security_layer_planning_result():
    for relative in [
        "docs/OPERATIONAL_BLOCK_FOUNDATION_E2E_CHECKPOINT.md",
        "docs/NEXT_OPERATIONAL_BLOCK_PLAN.md",
        "docs/BACKEND_INTERNAL_PHASE_3_TRANSITION_PLAN.md",
        "docs/BACKEND_INTERNAL_BOOK_DESIGN.md",
    ]:
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "PROMPT 3.20" in text
        assert "IA_CORE_SECURITY_LAYER_PLAN_READY" in text
        assert "SECURITY_LAYER_REQUIRED_BEFORE_RUNTIME" in text
        assert "ready_for_security_surface_audit" in text
