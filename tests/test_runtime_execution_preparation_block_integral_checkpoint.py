import ast
import importlib
import json
from pathlib import Path

import core.runtime_execution_preparation_contract as preparation_contract
import core.runtime_execution_preparation_package as package_contract
import core.runtime_execution_preparation_read_model as read_model_contract
import core.runtime_execution_preparation_projection as projection_contract


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RUNTIME_EXECUTION_PREPARATION_BLOCK_INTEGRAL_CHECKPOINT.md"

MAIN_MODULES = (
    "core.runtime_execution_preparation_contract",
    "core.runtime_execution_preparation_package",
    "core.runtime_execution_preparation_read_model",
    "core.runtime_execution_preparation_projection",
)
PREVIOUS_CONTRACTS_AND_BOUNDARIES = (
    "core.runtime_governance_contract",
    "core.runtime_state_contract",
    "core.observability_contract",
    "core.runtime_activation_gate",
    "core.dry_run_execution_contract",
    "core.kill_switch_rollback_contract",
    "core.output_boundary",
    "core.context_boundary",
    "core.model_invocation_boundary",
    "core.tool_boundary",
    "core.sandbox_boundary",
    "core.prompt_injection_defense",
    "core.secrets_policy",
    "core.agent_permission_contract",
)
BLOCK_DOCS = (
    "docs/RUNTIME_EXECUTION_PREPARATION_AUDIT.md",
    "docs/RUNTIME_EXECUTION_PREPARATION_CONTRACT.md",
    "docs/RUNTIME_EXECUTION_PREPARATION_CONTRACT_FULL_E2E_CHECKPOINT.md",
    "docs/RUNTIME_EXECUTION_PREPARATION_PACKAGE_AUDIT.md",
    "docs/RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT.md",
    "docs/RUNTIME_EXECUTION_PREPARATION_PACKAGE_CONTRACT_FULL_E2E_CHECKPOINT.md",
    "docs/RUNTIME_EXECUTION_PREPARATION_READ_MODEL_AUDIT.md",
    "docs/RUNTIME_EXECUTION_PREPARATION_READ_MODEL_CONTRACT.md",
    "docs/RUNTIME_EXECUTION_PREPARATION_READ_MODEL_CONTRACT_FULL_E2E_CHECKPOINT.md",
    "docs/RUNTIME_EXECUTION_PREPARATION_PROJECTION_AUDIT.md",
    "docs/RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTRACT.md",
    "docs/RUNTIME_EXECUTION_PREPARATION_PROJECTION_CONTRACT_FULL_E2E_CHECKPOINT.md",
)
BLOCK_TESTS = (
    "tests/test_runtime_execution_preparation_audit.py",
    "tests/test_runtime_execution_preparation_contract.py",
    "tests/test_runtime_execution_preparation_contract_full_e2e_checkpoint.py",
    "tests/test_runtime_execution_preparation_package_audit.py",
    "tests/test_runtime_execution_preparation_package_contract.py",
    "tests/test_runtime_execution_preparation_package_contract_full_e2e_checkpoint.py",
    "tests/test_runtime_execution_preparation_read_model_audit.py",
    "tests/test_runtime_execution_preparation_read_model_contract.py",
    "tests/test_runtime_execution_preparation_read_model_contract_full_e2e_checkpoint.py",
    "tests/test_runtime_execution_preparation_projection_audit.py",
    "tests/test_runtime_execution_preparation_projection_contract.py",
    "tests/test_runtime_execution_preparation_projection_contract_full_e2e_checkpoint.py",
)
FORBIDDEN_MODULES = (
    "core/runtime_execution_preparation_store.py",
    "core/runtime_execution_preparation_writer.py",
    "core/runtime_execution_preparation_reader.py",
    "core/runtime_execution_preparation_api.py",
    "core/runtime_execution_preparation_ui.py",
    "core/runtime_execution.py",
    "core/runtime_runner.py",
    "core/runtime_scheduler.py",
    "core/runtime_worker.py",
    "core/runtime_queue.py",
    "core/runtime_orchestrator.py",
    "core/runtime_dispatcher.py",
    "core/dry_run_executor.py",
    "core/tool_executor.py",
    "core/model_invoker.py",
    "core/context_injector.py",
    "core/output_delivery.py",
    "core/output_publisher.py",
    "core/browser_operator.py",
    "core/ui_tars_adapter.py",
    "core/hermes_adapter.py",
    "core/n8n_adapter.py",
    "core/home_assistant_adapter.py",
)
FORBIDDEN_DATA_KEYS = (
    "secret",
    "secrets",
    "api_key",
    "apikey",
    "token",
    "access_token",
    "refresh_token",
    "password",
    "passwd",
    "credential",
    "credentials",
    "private_key",
    "raw_payload",
    "payload",
    "raw_output",
    "output",
    "file_content",
    "env",
    "environment",
    "cookie",
    "authorization",
    "bearer",
    "raw_prompt",
    "prompt",
    "raw_completion",
    "completion",
    "model_response",
    "tool_response",
    "external_response",
    "browser_content",
    "filesystem_content",
    "personal_data_unsanitized",
    "master_panel_internal_capability",
    "admin_secret",
    "permission_bypass",
    "raw_master_panel_view",
    "raw_user_panel_view",
    "raw_internal_audit_view",
)
DANGEROUS_IMPORTS = {"subprocess", "socket", "requests", "httpx", "selenium", "playwright", "browser"}


def _doc_text() -> str:
    return DOC.read_text(encoding="utf-8")


def _assert_ready_and_blocked(module_name: str) -> None:
    module = importlib.import_module(module_name)
    ready_flags = [
        getattr(module, name)
        for name in dir(module)
        if name.isupper() and isinstance(getattr(module, name), bool) and name.endswith("CONTRACT_READY")
    ]
    if module_name in MAIN_MODULES:
        assert ready_flags == [True], module_name
    for name in dir(module):
        value = getattr(module, name)
        if not name.isupper() or not isinstance(value, bool) or name.endswith("_READY"):
            continue
        if name.endswith(("_OPERATIONAL", "_ACTIVE", "_ENABLED", "_ALLOWED")):
            assert value is False, f"{module_name}.{name}"


def _package_chain():
    dependency_set = package_contract.build_runtime_execution_preparation_package_dependency_set(
        preparation_id="prep_1",
        intent_ref="intent_1",
        attempt_ref="attempt_1",
        runtime_governance_ref="core.runtime_governance_contract",
        runtime_state_ref="core.runtime_state_contract",
        observability_ref="core.observability_contract",
        runtime_activation_gate_ref="core.runtime_activation_gate",
        security_baseline_ref="security_baseline",
        agent_permission_ref="core.agent_permission_contract",
        sandbox_boundary_ref="core.sandbox_boundary",
        tool_boundary_ref="core.tool_boundary",
        model_boundary_ref="core.model_invocation_boundary",
        context_boundary_ref="core.context_boundary",
        output_boundary_ref="core.output_boundary",
        secrets_policy_ref="core.secrets_policy",
        prompt_injection_defense_ref="core.prompt_injection_defense",
    )
    boundary_set = package_contract.build_runtime_execution_preparation_package_boundary_set(
        security_baseline_ok=True,
        agent_permission_ok=True,
        sandbox_boundary_ok=True,
        tool_boundary_ok=True,
        model_boundary_ok=True,
        context_boundary_ok=True,
        output_boundary_ok=True,
        secrets_policy_ok=True,
        prompt_injection_defense_ok=True,
        runtime_governance_ok=True,
        runtime_state_ok=True,
        observability_ok=True,
        runtime_activation_gate_ok=True,
    )
    package = package_contract.build_runtime_execution_preparation_package(
        package_id="package_1",
        dependency_set=dependency_set,
        boundary_set=boundary_set,
        execution_scope="integral_checkpoint",
        execution_mode="contract_only",
        execution_risk_level="low",
        metadata={"package_reason": "integral checkpoint", "tags": ("safe",)},
    )
    validation = package_contract.validate_runtime_execution_preparation_package_contract(package)
    decision = package_contract.decide_runtime_execution_preparation_package(validation)
    safe_view = package_contract.build_runtime_execution_preparation_package_safe_view(
        package,
        validation,
        package_contract.RuntimeExecutionPreparationPackageVisibility.USER_PANEL_SAFE,
    )
    snapshot = package_contract.build_runtime_execution_preparation_package_contract_snapshot(
        package=package,
        validation=validation,
        decision=decision,
        safe_view=safe_view,
    )
    return package, validation, decision, safe_view, snapshot


def _read_model_chain():
    source = read_model_contract.build_runtime_execution_preparation_read_model_source_ref(
        package_id="package_1",
        preparation_id="prep_1",
        intent_ref="intent_1",
        attempt_ref="attempt_1",
        source_package_ref="core.runtime_execution_preparation_package",
        source_contract_ref="core.runtime_execution_preparation_contract",
        safe_view_ref="package_safe_view",
    )
    read_model = read_model_contract.build_runtime_execution_preparation_read_model(
        read_model_id="read_model_1",
        source_ref=source,
        execution_scope="integral_checkpoint",
        metadata={"read_model_reason": "integral checkpoint", "tags": ("safe",)},
    )
    master = read_model_contract.build_runtime_execution_preparation_master_panel_view(
        read_model,
        technical_refs=("source_package_ref", "source_contract_ref"),
    )
    user = read_model_contract.build_runtime_execution_preparation_user_panel_view(read_model)
    audit = read_model_contract.build_runtime_execution_preparation_internal_audit_view(
        read_model,
        sanitized_refs=("source_package_ref", "source_contract_ref"),
    )
    validation = read_model_contract.validate_runtime_execution_preparation_read_model(
        read_model,
        master_view=master,
        user_view=user,
        audit_view=audit,
    )
    decision = read_model_contract.decide_runtime_execution_preparation_read_model(validation)
    snapshot = read_model_contract.build_runtime_execution_preparation_read_model_contract_snapshot(
        read_model=read_model,
        master_panel_view=master,
        user_panel_view=user,
        internal_audit_view=audit,
        validation=validation,
        decision=decision,
        source_refs=source,
    )
    return read_model, (master, user, audit), validation, decision, snapshot


def _projection_chain():
    source = projection_contract.build_runtime_execution_preparation_projection_source_ref(
        projection_id="projection_1",
        read_model_id="read_model_1",
        package_id="package_1",
        preparation_id="prep_1",
        intent_ref="intent_1",
        attempt_ref="attempt_1",
        source_read_model_ref="core.runtime_execution_preparation_read_model",
        source_package_ref="core.runtime_execution_preparation_package",
        source_contract_refs=(
            "core.runtime_execution_preparation_projection",
            "core.runtime_execution_preparation_read_model",
            "core.runtime_execution_preparation_package",
            "core.runtime_execution_preparation_contract",
        ),
        parent_read_model_contract_ref="core.runtime_execution_preparation_read_model",
        parent_package_contract_ref="core.runtime_execution_preparation_package",
        parent_preparation_contract_ref="core.runtime_execution_preparation_contract",
    )
    projection = projection_contract.build_runtime_execution_preparation_projection(
        source_ref=source,
        projection_kind="summary_projection",
        projection_readiness="ready_for_runtime_execution_preparation_projection_contract_e2e",
        visibility="internal_only",
        metadata={"projection_reason": "integral checkpoint", "tags": ("safe",)},
    )
    master = projection_contract.build_runtime_execution_preparation_master_panel_projection(
        projection,
        technical_refs=("source_read_model_ref", "source_package_ref"),
    )
    user = projection_contract.build_runtime_execution_preparation_user_panel_projection(projection)
    audit = projection_contract.build_runtime_execution_preparation_internal_audit_projection(
        projection,
        sanitized_refs=("source_read_model_ref", "source_package_ref"),
    )
    summary = projection_contract.build_runtime_execution_preparation_summary_projection(projection)
    status_only = projection_contract.build_runtime_execution_preparation_status_only_projection(projection)
    blocked = projection_contract.build_runtime_execution_preparation_blocked_projection(projection, "contract_only")
    validation = projection_contract.validate_runtime_execution_preparation_projection(
        projection,
        master_projection=master,
        user_projection=user,
        internal_audit_projection=audit,
        summary_projection=summary,
        status_only_projection=status_only,
        blocked_projection=blocked,
    )
    decision = projection_contract.decide_runtime_execution_preparation_projection(validation)
    snapshot = projection_contract.build_runtime_execution_preparation_projection_contract_snapshot(
        projection=projection,
        master_panel_projection=master,
        user_panel_projection=user,
        internal_audit_projection=audit,
        summary_projection=summary,
        status_only_projection=status_only,
        blocked_projection=blocked,
        validation=validation,
        decision=decision,
        source_refs=source,
    )
    return projection, (master, user, audit, summary, status_only, blocked), validation, decision, snapshot


def test_integral_checkpoint_document_exists_and_contains_required_tokens():
    text = _doc_text()
    for token in (
        "Runtime Execution Preparation Block Integral Checkpoint",
        "RUNTIME_EXECUTION_PREPARATION_BLOCK_INTEGRAL_CHECKPOINT_PASSED",
        "RUNTIME_EXECUTION_PREPARATION_BLOCK_CHAIN_READY",
        "ready_for_next_architecture_block_planning",
        "PROMPT 4.9 — Planificación del siguiente bloque arquitectónico",
        "4.0 Runtime Execution Preparation Audit",
        "4.7.1 Runtime Execution Preparation Projection Contract E2E",
        "Ninguna readiness de este bloque habilita runtime real",
        "Datos Prohibidos",
        "Vistas Y Proyecciones",
        "Serialización Y Determinismo",
        "OBLITERATUS queda excluido",
        "Gaps Esperados Para Siguiente Bloque",
    ):
        assert token in text
    matrix_rows = [line for line in text.splitlines() if line.startswith("| ") and line.split("|")[1].strip().isdigit()]
    assert len(matrix_rows) == 65


def test_integral_readiness_chain_is_complete_and_non_operational():
    text = _doc_text()
    for readiness in (
        "ready_for_runtime_execution_preparation_contract",
        "ready_for_runtime_execution_preparation_contract_e2e",
        "ready_for_runtime_execution_preparation_package_audit",
        "ready_for_runtime_execution_preparation_package_contract",
        "ready_for_runtime_execution_preparation_package_contract_e2e",
        "ready_for_runtime_execution_preparation_read_model_audit",
        "ready_for_runtime_execution_preparation_read_model_contract",
        "ready_for_runtime_execution_preparation_read_model_contract_e2e",
        "ready_for_runtime_execution_preparation_projection_audit",
        "ready_for_runtime_execution_preparation_projection_contract",
        "ready_for_runtime_execution_preparation_projection_contract_e2e",
        "ready_for_runtime_execution_preparation_block_integral_checkpoint",
        "ready_for_next_architecture_block_planning",
    ):
        assert readiness in text
    assert "habilita runtime real" in text
    assert "API, UI, UI-device ni integraciones" in text


def test_integral_main_modules_are_ready_and_operational_flags_are_false():
    for module_name in MAIN_MODULES:
        _assert_ready_and_blocked(module_name)


def test_integral_previous_contracts_and_boundaries_remain_blocked():
    for module_name in PREVIOUS_CONTRACTS_AND_BOUNDARIES:
        importlib.import_module(module_name)
        _assert_ready_and_blocked(module_name)


def test_integral_forbidden_operational_modules_are_absent_and_runtime_executor_is_prepare_only():
    for relative in FORBIDDEN_MODULES:
        assert not (ROOT / relative).exists(), relative
    runtime_executor = ROOT / "core" / "runtime_executor.py"
    if runtime_executor.exists():
        assert "prepare-only" in runtime_executor.read_text(encoding="utf-8").lower()


def test_integral_forbidden_metadata_keys_are_covered_by_the_chain():
    base_keys = set(FORBIDDEN_DATA_KEYS) - {
        "master_panel_internal_capability",
        "admin_secret",
        "permission_bypass",
        "raw_master_panel_view",
        "raw_user_panel_view",
        "raw_internal_audit_view",
    }
    assert base_keys.issubset(set(package_contract.FORBIDDEN_METADATA_KEYS))
    assert base_keys.union({"master_panel_internal_capability", "admin_secret", "permission_bypass"}).issubset(
        set(read_model_contract.FORBIDDEN_METADATA_KEYS)
    )
    assert set(FORBIDDEN_DATA_KEYS).issubset(set(projection_contract.FORBIDDEN_METADATA_KEYS))


def test_integral_views_and_projections_do_not_expose_internals_or_raw_data():
    _, package_validation, _, package_safe_view, _ = _package_chain()
    assert package_validation.is_valid is True
    package_dump = json.dumps(package_contract.runtime_execution_preparation_package_to_dict(package_safe_view), sort_keys=True).lower()
    _, (_, user_view, audit_view), read_validation, _, _ = _read_model_chain()
    assert read_validation.is_valid is True
    user_view_dict = read_model_contract.runtime_execution_preparation_read_model_to_dict(user_view)
    assert "technical_refs" not in user_view_dict
    assert "metadata" not in user_view_dict
    assert audit_view.blocked_keys == ()
    _, (_, user_projection, audit_projection, summary, status_only, blocked), projection_validation, _, _ = _projection_chain()
    assert projection_validation.is_valid is True
    user_projection_dict = projection_contract.runtime_execution_preparation_projection_to_dict(user_projection)
    assert "technical_refs" not in user_projection_dict
    assert "metadata" not in user_projection_dict
    assert "raw_package_contract" not in json.dumps(user_projection_dict, sort_keys=True).lower()
    assert "raw_read_model_contract" not in json.dumps(user_projection_dict, sort_keys=True).lower()
    assert audit_projection.blocked_keys == ()
    assert set(projection_contract.runtime_execution_preparation_projection_to_dict(summary)) == {
        "projection_id",
        "package_id",
        "status",
        "readiness",
        "risk_level",
        "safe_summary",
        "visibility",
    }
    assert set(projection_contract.runtime_execution_preparation_projection_to_dict(status_only)) == {
        "projection_id",
        "package_id",
        "status",
        "readiness",
        "risk_level",
        "visibility",
    }
    assert not any(key.startswith("allowed") for key in projection_contract.runtime_execution_preparation_projection_to_dict(blocked))
    for dumped in (package_dump, json.dumps(user_view_dict, sort_keys=True).lower(), json.dumps(user_projection_dict, sort_keys=True).lower()):
        for fragment in ("raw_payload", "raw_prompt", "raw_output", "model_response", "tool_response"):
            assert fragment not in dumped
    assert projection_contract.build_runtime_execution_preparation_projection_policy().raw_package_to_user_projection_enabled is False


def test_integral_snapshots_are_json_safe_and_deterministic():
    contract_snapshot = preparation_contract.build_runtime_execution_preparation_contract_snapshot()
    _, _, _, _, package_snapshot = _package_chain()
    _, _, _, _, read_snapshot = _read_model_chain()
    _, _, _, _, projection_snapshot = _projection_chain()
    pairs = (
        (contract_snapshot, preparation_contract.runtime_execution_preparation_to_dict),
        (package_snapshot, package_contract.runtime_execution_preparation_package_to_dict),
        (read_snapshot, read_model_contract.runtime_execution_preparation_read_model_to_dict),
        (projection_snapshot, projection_contract.runtime_execution_preparation_projection_to_dict),
    )
    for snapshot, serializer in pairs:
        first = serializer(snapshot)
        second = serializer(snapshot)
        json.dumps(first, sort_keys=True)
        assert first == second


def test_integral_main_modules_do_not_access_env_or_import_execution_runtime_tools():
    for relative in (
        "core/runtime_execution_preparation_contract.py",
        "core/runtime_execution_preparation_package.py",
        "core/runtime_execution_preparation_read_model.py",
        "core/runtime_execution_preparation_projection.py",
    ):
        source = (ROOT / relative).read_text(encoding="utf-8")
        assert "os.environ" not in source
        tree = ast.parse(source)
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        assert DANGEROUS_IMPORTS.isdisjoint(imports), (relative, imports & DANGEROUS_IMPORTS)


def test_integral_obliteratus_is_excluded():
    text = _doc_text()
    assert "OBLITERATUS queda excluido del bloque Runtime Execution Preparation" in text
    for module in (preparation_contract, package_contract, read_model_contract, projection_contract):
        joined = "\n".join(getattr(module, "OBLITERATUS_EXCLUSION_STATEMENTS", ())).lower()
        assert "obliteratus" in joined
        assert "not an integration" in joined or "no es integration" in text
        assert "not a runtime" in joined or "no es runtime" in text


def test_integral_previous_docs_and_tests_exist():
    for relative in BLOCK_DOCS:
        assert (ROOT / relative).exists(), relative
    for relative in BLOCK_TESTS:
        assert (ROOT / relative).exists(), relative
