from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "IA_CORE_SECURITY_SURFACE_AUDIT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_security_surface_audit_exists_and_declares_status():
    text = _text()
    assert DOC.exists()
    for phrase in [
        "IA_CORE Security Layer — Attack Surface Audit",
        "IA_CORE_SECURITY_SURFACE_AUDIT_COMPLETED",
        "SECURITY_SURFACE_REQUIRES_PERMISSION_CONTRACT",
        "ready_for_agent_permission_contract",
        "PROMPT 3.22 — Contrato de permisos por agente",
    ]:
        assert phrase in text


def test_security_surface_audit_is_defensive_only():
    text = _text()
    for phrase in [
        "Esta auditoría identifica la superficie de ataque actual y futura de IA_CORE",
        "La auditoría es defensiva",
        "No implementa capacidades ofensivas",
        "No habilita ejecución real",
        "No prueba targets externos",
        "No incorpora repos externos",
        "No activa conectores",
    ]:
        assert phrase in text


def test_security_surface_audit_contains_current_surface():
    text = _text()
    for phrase in [
        "ExecutionIntent",
        "attempt factory contract",
        "ExecutionAttempt en memoria",
        "ExecutionAttempt state machine",
        "attempt store write-safe contract",
        "lifecycle writer contract",
        "OperationalReadinessGate contract-only",
        "ExecutionResult contract",
        "execution result projection",
        "execution history view",
        "internal backend read model",
        "attempt_store",
        "lifecycle_store",
        "dry_run_store",
        "Market Catalog planned_not_active",
        "Business Composition Layer futura/no operativa",
        "propósito actual",
        "estado actual",
        "superficie de ataque",
        "riesgo si se activa antes de tiempo",
        "boundary actual",
        "controles necesarios antes de runtime",
    ]:
        assert phrase in text


def test_security_surface_audit_contains_future_surface():
    text = _text()
    for phrase in [
        "runtime runner",
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
        "agent teams",
        "agent presets",
        "professional library",
        "Business Composition Layer runtime",
        "Market Catalog runtime",
        "document ingestion",
        "web ingestion",
        "image/screenshot ingestion",
        "prompt templates",
        "approval flows",
        "human-in-the-loop actions",
        "secrets/config/env",
        "logs/audit trail",
        "rollback/compensation",
        "kill switch",
        "rol futuro",
        "riesgo principal",
        "ataque posible",
        "impacto",
        "controles mínimos requeridos",
        "estado actual",
    ]:
        assert phrase in text


def test_security_surface_audit_contains_threat_categories():
    text = _text()
    for phrase in [
        "Threat categories",
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
        "scheduler misuse",
        "worker misuse",
        "queue misuse",
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
        "descripción",
        "superficie afectada",
        "ejemplo defensivo/controlado",
        "impacto potencial",
        "control mínimo requerido",
        "requiere permiso explícito",
    ]:
        assert phrase in text


def test_security_surface_audit_contains_risk_matrix():
    text = _text()
    for phrase in [
        "Superficie",
        "Estado actual",
        "Amenaza principal",
        "Impacto",
        "Probabilidad",
        "Riesgo",
        "Controles mínimos",
        "Próximo contrato necesario",
        "low",
        "medium",
        "high",
        "critical",
        "documents/web/images/screenshots",
        "secrets/config/env",
        "audit trail/logs",
    ]:
        assert phrase in text


def test_security_surface_audit_contains_minimum_controls():
    text = _text()
    for phrase in [
        "permission contract",
        "capability registry",
        "default deny policy",
        "least privilege policy",
        "agent identity",
        "agent role/specialization binding",
        "approval gate",
        "human-in-the-loop policy",
        "sandbox policy",
        "tool allowlist",
        "tool denylist",
        "secret redaction",
        "secret storage policy",
        "prompt injection filter",
        "input provenance tracking",
        "document trust level",
        "web trust level",
        "screenshot trust level",
        "lineage validation",
        "idempotency validation",
        "write policy",
        "rollback/compensation policy",
        "immutable audit trail",
        "runtime gate",
        "external access gate",
        "kill switch",
        "risk report",
        "security E2E checkpoint",
    ]:
        assert phrase in text


def test_security_surface_audit_justifies_next_permission_contract():
    text = _text()
    for phrase in [
        "Contrato de permisos por agente",
        "quién puede hacer qué",
        "El contrato de permisos por agente es el primer contrato de Security Layer",
    ]:
        assert phrase in text


def test_security_surface_audit_contains_future_integrations_risk_map():
    text = _text()
    for phrase in [
        "Future integrations risk map",
        "UI-TARS",
        "operador visual / GUI operator",
        "acciones no autorizadas sobre pantalla",
        "prompt injection visual",
        "Hermes",
        "herramienta/orquestador operativo subordinado a IA_CORE",
        "orquestación no autorizada",
        "n8n",
        "automatizador de workflows/conectores",
        "abuso de webhooks",
        "Home Assistant",
        "puente físico/local",
        "acciones físicas inseguras",
        "OBLITERATUS",
        "no es integración de IA_CORE",
        "no es dependencia",
        "no forma parte del roadmap operativo",
    ]:
        assert phrase in text


def test_security_surface_audit_contains_defensive_red_team_scope():
    text = _text()
    for phrase in [
        "Defensive Red Team",
        "Adversarial Lab",
        "solo contra agentes propios",
        "solo en sandbox",
        "fines de hardening",
        "jailbreak regression tests",
        "prompt injection regression tests",
        "permission bypass tests",
        "secret leakage tests",
        "tool abuse tests",
        "memory poisoning tests",
        "malicious document tests",
        "malicious webpage/UI tests",
        "malicious screenshot tests",
        "agent boundary regression tests",
        "approval bypass tests",
        "runtime activation bypass tests",
    ]:
        assert phrase in text


def test_security_surface_audit_contains_red_team_prohibitions():
    text = _text()
    for phrase in [
        "ataques contra terceros",
        "exfiltración real",
        "bypass operativo sobre servicios externos",
        "uso ofensivo fuera de sandbox",
        "uso para romper restricciones de modelos con fines dañinos",
    ]:
        assert phrase in text


def test_security_surface_audit_contains_security_invariants():
    text = _text()
    for phrase in [
        "default deny",
        "least privilege",
        "explicit permission required",
        "no runtime without Security Layer",
        "no tool execution without permission contract",
        "no model invocation without permission contract",
        "no memory persistence without permission contract",
        "no external access without permission contract",
        "no UI operator without sandbox and approval",
        "no physical-world action without approval and safety policy",
        "no secrets in prompts",
        "no secrets in logs",
        "every action must have lineage",
        "every sensitive action must have idempotency",
        "every write must have rollback or compensation policy",
        "every external action must have audit trail",
        "kill switch must remain available",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
    ]:
        assert phrase in text


def test_security_surface_audit_declares_blocked_boundaries():
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


def test_security_surface_audit_did_not_create_operational_modules():
    for relative in [
        "core/security_layer.py",
        "core/permission_contract.py",
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


def test_security_surface_audit_has_no_contradictory_enabled_states():
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
        "ready_for_runtime",
    ]:
        assert forbidden not in text


def test_prior_docs_reference_security_surface_audit_result():
    for relative in [
        "docs/IA_CORE_SECURITY_LAYER_PLAN.md",
        "docs/NEXT_OPERATIONAL_BLOCK_PLAN.md",
        "docs/BACKEND_INTERNAL_PHASE_3_TRANSITION_PLAN.md",
        "docs/BACKEND_INTERNAL_BOOK_DESIGN.md",
    ]:
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "PROMPT 3.21" in text
        assert "IA_CORE_SECURITY_SURFACE_AUDIT_COMPLETED" in text
        assert "SECURITY_SURFACE_REQUIRES_PERMISSION_CONTRACT" in text
        assert "ready_for_agent_permission_contract" in text
