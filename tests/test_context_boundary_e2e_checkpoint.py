from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "CONTEXT_BOUNDARY_E2E_CHECKPOINT.md"


def test_context_boundary_e2e_checkpoint_exists():
    assert DOC.exists()


def test_context_boundary_e2e_checkpoint_contains_chain_and_next_step():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "CONTEXT_BOUNDARY_E2E_PASSED",
        "PROMPT 3.21 - Auditoria de superficie de ataque de IA_CORE",
        "PROMPT 3.22 - Contrato de permisos por agente",
        "PROMPT 3.23 - Politica de secretos y datos sensibles",
        "PROMPT 3.24 - Defensa contra prompt injection",
        "PROMPT 3.25 - Sandbox boundary y aislamiento pre-runtime",
        "PROMPT 3.26 - Tool boundary y politica de herramientas pre-runtime",
        "PROMPT 3.27 - Model invocation boundary pre-runtime",
        "PROMPT 3.27.1 - Checkpoint E2E de model invocation boundary",
        "PROMPT 3.28 - Context boundary y politica de contexto pre-runtime",
        "PROMPT 3.28.1 - Checkpoint E2E de context boundary",
    ]:
        assert phrase in text


def test_context_boundary_e2e_checkpoint_contains_required_statuses():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "IA_CORE_SECURITY_SURFACE_AUDIT_COMPLETED",
        "AGENT_PERMISSION_CONTRACT_READY",
        "SECRETS_POLICY_READY",
        "PROMPT_INJECTION_DEFENSE_READY",
        "SANDBOX_BOUNDARY_READY",
        "TOOL_BOUNDARY_READY",
        "MODEL_INVOCATION_BOUNDARY_READY",
        "MODEL_INVOCATION_BOUNDARY_FULL_E2E_PASSED",
        "ready_for_context_boundary_planning",
        "CONTEXT_BOUNDARY_READY",
        "CONTEXT_BOUNDARY_E2E_PASSED",
        "ready_for_context_boundary_e2e_checkpoint",
    ]:
        assert phrase in text


def test_context_boundary_e2e_checkpoint_confirms_boundaries():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
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
        "no context builder",
        "no prompt assembly",
        "no retrieval",
        "no RAG",
        "no memory expansion",
        "no filesystem expansion",
        "no web expansion",
        "no tool result expansion",
        "no model output expansion",
        "no screen expansion",
        "no document instruction execution",
        "no untrusted instruction execution",
        "no raw context logging",
        "no raw prompt assembly",
        "no real model invocation",
        "no tool execution",
        "no tool adapters",
        "no tool calls",
        "no API calls",
        "no network",
        "no browser",
        "no command execution",
        "no shell",
        "no process spawn",
        "no real filesystem reads",
        "no real filesystem writes",
        "no env access",
        "no secret access",
        "no memory persistence",
        "no writes reales",
        "no stores operativos",
        "no UI control",
        "no device control",
        "no UI-TARS runtime",
        "no Hermes runtime",
        "no n8n real workflows",
        "no Home Assistant real actions",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
        "OBLITERATUS is not an IA_CORE integration",
    ]:
        assert phrase in text


def test_context_boundary_e2e_checkpoint_has_no_contradictory_states():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "runtime_enabled = true",
        "context_builder_enabled = true",
        "context_injection_enabled = true",
        "context_assembly_enabled = true",
        "context_retrieval_enabled = true",
        "context_rag_enabled = true",
        "memory_expansion_enabled = true",
        "filesystem_expansion_enabled = true",
        "web_expansion_enabled = true",
        "tool_result_expansion_enabled = true",
        "model_output_expansion_enabled = true",
        "screen_expansion_enabled = true",
        "document_execution_enabled = true",
        "untrusted_instruction_execution_enabled = true",
        "raw_context_logging_enabled = true",
        "raw_prompt_assembly_enabled = true",
        "model_invocation_enabled = true",
        "tool_execution_enabled = true",
        "secret_access_enabled = true",
        "memory_persistence_enabled = true",
        "writes_enabled = true",
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
        assert phrase not in text
