"""Surgical continuity audit checks for commits after UI/UX 1.175."""

from ui_ux_1_192_scope import historical_paths, assert_current_scope
HISTORICAL_COMMIT = 'd98e999'

from pathlib import Path
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_POST_1_175_COMMITS_SURGICAL_AUDIT_1_177_1.md"
README = ROOT / "README.md"
WEB_README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
PAYLOAD_SOURCE = ROOT / "core" / "backend_internal_ui_payloads.py"
FIX_177 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_RESPONSIVE_DEBT_FIX_1_177.md"

RANGE = "fdc2b7d..4403489"
ALLOWED_DIFF = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_POST_1_175_COMMITS_SURGICAL_AUDIT_1_177_1.md",
    "tests/test_ui_ux_post_1_175_commits_surgical_audit_1_177_1.py",
}

CONTINUITY_1_180 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/index.html",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_FIRST_PASS_1_180.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_1_180.py",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_audit_1_179.py",
    "tests/test_ui_ux_panel_maestro_responsive_visual_checkpoint_1_178.py",
    "tests/test_ui_ux_post_1_175_commits_surgical_audit_1_177_1.py",
    "tests/test_ui_ux_panel_maestro_responsive_debt_fix_1_177.py",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_176.py",
    "tests/test_ui_ux_panel_maestro_widgets_contract_aware_checkpoint_1_175.py",
}

ALLOWED_DIFF |= CONTINUITY_1_180

CONTINUITY_1_181 = {
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_FIRST_PASS_CHECKPOINT_1_181.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_checkpoint_1_181.py",
}

ALLOWED_DIFF |= CONTINUITY_1_181

CONTINUITY_1_182 = {
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_SECOND_PASS_SELECTION_1_182.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_second_pass_selection_1_182.py",
}

ALLOWED_DIFF |= CONTINUITY_1_182

CONTINUITY_1_183 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/index.html",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_1_183.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_p1_contractual_second_pass_1_183.py",
}

# CONTINUITY_1_181 remains preserved; CONTINUITY_1_183 is additive.
ALLOWED_DIFF |= CONTINUITY_1_183

CONTINUITY_1_184 = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_P1_CONTRACTUAL_SECOND_PASS_CHECKPOINT_1_184.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_p1_contractual_second_pass_checkpoint_1_184.py",
}

# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1,
# CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181,
# CONTINUITY_1_182 and CONTINUITY_1_183 remain preserved; CONTINUITY_1_184 is additive.
ALLOWED_DIFF |= CONTINUITY_1_184

CONTINUITY_1_185 = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_SELECTION_1_185.md",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_185.py",
}

# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1,
# CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181,
# CONTINUITY_1_182, CONTINUITY_1_183 and CONTINUITY_1_184 remain preserved;
# CONTINUITY_1_185 is additive.
ALLOWED_DIFF |= CONTINUITY_1_185

CONTINUITY_1_186 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_MATRIX_VISUAL_HIERARCHY_DEMOTION_1_186.md",
    "tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_1_186.py",
}

# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184 and CONTINUITY_1_185 remain preserved; CONTINUITY_1_186 is additive and scoped to the matrix visual demotion.
ALLOWED_DIFF |= CONTINUITY_1_186

CONTINUITY_1_187 = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_MATRIX_VISUAL_HIERARCHY_DEMOTION_CHECKPOINT_1_187.md",
    "tests/test_ui_ux_panel_maestro_matrix_visual_hierarchy_demotion_checkpoint_1_187.py",
}

# CONTINUITY_1_175 through CONTINUITY_1_186 remain preserved; CONTINUITY_1_187 is additive.
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185 and CONTINUITY_1_186 remain preserved.
ALLOWED_DIFF |= CONTINUITY_1_187

CONTINUITY_1_188 = {
    "README.md",
    "ui/web/README.md",
    "docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_SELECTION_1_188.md",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_188.py",
}

# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186 and CONTINUITY_1_187 remain preserved; CONTINUITY_1_188 is additive.
ALLOWED_DIFF |= CONTINUITY_1_188
CONTINUITY_1_189 = {
    "README.md",
    "ui/web/README.md",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_1_189.md",
    "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_1_189.py",
}

# CONTINUITY_1_175 through CONTINUITY_1_188 remain preserved; CONTINUITY_1_189 is additive.
ALLOWED_DIFF |= CONTINUITY_1_189
CONTINUITY_1_189_A = {"README.md", "ui/web/README.md", "docs/UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_FIX_1_189_A.md", "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_fix_1_189_A.py"}
# CONTINUITY_1_175 through CONTINUITY_1_189 remain preserved; CONTINUITY_1_189_A is additive.
ALLOWED_DIFF |= CONTINUITY_1_189_A
CONTINUITY_1_190 = {"README.md", "ui/web/README.md", "docs/UI_UX_PANEL_MAESTRO_REQUEST_DRAFT_PANEL_VISUAL_DEMOTION_CHECKPOINT_1_190.md", "tests/test_ui_ux_panel_maestro_request_draft_panel_visual_demotion_checkpoint_1_190.py"}
ALLOWED_DIFF |= CONTINUITY_1_190
CONTINUITY_1_191 = {"README.md", "ui/web/README.md", "docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_OR_CONTROLLED_SCOPE_SELECTION_1_191.md", "tests/test_ui_ux_panel_maestro_next_visual_block_or_controlled_scope_selection_1_191.py"}
ALLOWED_DIFF |= CONTINUITY_1_191
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186, CONTINUITY_1_187, CONTINUITY_1_188, CONTINUITY_1_189, CONTINUITY_1_189_A and CONTINUITY_1_190 remain preserved; CONTINUITY_1_191 is additive.
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186, CONTINUITY_1_187, CONTINUITY_1_188, CONTINUITY_1_189 and CONTINUITY_1_189_A remain preserved; CONTINUITY_1_190 is additive.
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186, CONTINUITY_1_187, CONTINUITY_1_188 and CONTINUITY_1_189 remain preserved; CONTINUITY_1_189_A is additive.
# CONTINUITY_1_175, CONTINUITY_1_176, CONTINUITY_1_177, CONTINUITY_1_177_1, CONTINUITY_1_178, CONTINUITY_1_179, CONTINUITY_1_180, CONTINUITY_1_181, CONTINUITY_1_182, CONTINUITY_1_183, CONTINUITY_1_184, CONTINUITY_1_185, CONTINUITY_1_186, CONTINUITY_1_187 and CONTINUITY_1_188 remain preserved; CONTINUITY_1_189 is additive.

APPROVED_1_180_ACTIVE_UI = {"ui/web/index.html", "ui/web/styles.css"}
REQUIRED_1_180 = {
    "ui/web/index.html",
    "ui/web/styles.css",
    "docs/UI_UX_PANEL_MAESTRO_VISUAL_HIERARCHY_FIRST_PASS_1_180.md",
    "tests/test_ui_ux_panel_maestro_visual_hierarchy_first_pass_1_180.py",
}

# The complete 1.183 artifact set is the current authorized active-UI gate.
REQUIRED_1_183 = CONTINUITY_1_183
REQUIRED_1_180 = REQUIRED_1_183

EXPECTED_ADDED_FILES = {
    "docs/FUTURE_CORPORATE_AREAS_AND_SUBAREAS_MODEL.md",
    "docs/FUTURE_IA_CORE_OS_AND_DEVICE_ECOSYSTEM.md",
    "docs/FUTURE_INSTITUTIONAL_INTELLIGENCE_LAYER.md",
    "docs/FUTURE_ROOT_CONTROL_PLANE_OWNER_NODES_AND_CONTINUITY_MODEL.md",
    "docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_SELECTION_1_176.md",
    "docs/UI_UX_PANEL_MAESTRO_RESPONSIVE_DEBT_FIX_1_177.md",
    "tests/test_strategic_docs_corporate_areas_and_institutional_intelligence_1_1.py",
    "tests/test_strategic_docs_ia_core_os_and_device_ecosystem_1_2.py",
    "tests/test_strategic_docs_root_control_plane_owner_nodes_and_continuity_1_3.py",
    "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_176.py",
    "tests/test_ui_ux_panel_maestro_responsive_debt_fix_1_177.py",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def assert_markers(path: Path, markers: list[str]) -> None:
    text = normalized(read(path))
    missing = [marker for marker in markers if normalized(marker) not in text]
    assert not missing, f"{path.name}: missing {missing}"


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def lines(value: str) -> set[str]:
    return set(filter(None, value.splitlines()))


def changed_paths() -> set[str]:
    """Paths in this closed checkpoint, never the current worktree."""
    return historical_paths(ROOT, HISTORICAL_COMMIT)


def commit_paths(commit: str) -> set[str]:
    return lines(git("show", "--pretty=format:", "--name-only", commit))


def blob(commit: str, path: str) -> str:
    return git("rev-parse", f"{commit}:{path}")


def test_audit_document_exists_and_records_full_chain():
    assert DOC.is_file()
    assert_markers(
        DOC,
        [
            "UI/UX Post 1.175 Commits Surgical Audit 1.177.1",
            "fdc2b7d..4403489",
            "fdc2b7d",
            "ae1a462",
            "a20c6be",
            "dffe36e",
            "e9f5b94",
            "4403489",
            "UI_UX_WIDGETS_CONTRACT_AWARE_CHECKPOINTED",
            "STRATEGIC_CORPORATE_AREAS_AND_INSTITUTIONAL_INTELLIGENCE_DOCUMENTED",
            "STRATEGIC_IA_CORE_OS_AND_DEVICE_ECOSYSTEM_DOCUMENTED",
            "STRATEGIC_ROOT_CONTROL_PLANE_OWNER_NODES_AND_CONTINUITY_DOCUMENTED",
            "UI_UX_NEXT_VISUAL_BLOCK_SELECTED_POST_STRATEGIC_DOCS",
            "UI_UX_RESPONSIVE_DEBT_PANEL_MAESTRO_RESOLVED",
        ],
    )


def test_document_contains_every_required_audit_section():
    assert_markers(
        DOC,
        [
            "Auditoría por commit",
            "Auditoría de archivos sensibles",
            "Auditoría de documentación futura",
            "Auditoría de frases prohibidas",
            "Auditoría de payloads y contratos",
            "Auditoría de README y cursor",
            "Auditoría de archivos nuevos inesperados",
            "Riesgos detectados",
            "Blockers detectados",
            "Correcciones aplicadas",
        ],
    )


def test_verdict_readiness_and_next_prompt_are_consistent():
    text = read(DOC)
    verdicts = [
        "UI_UX_POST_1_175_SURGICAL_AUDIT_PASSED",
        "UI_UX_POST_1_175_SURGICAL_AUDIT_PENDING_MINOR_FIX",
        "UI_UX_POST_1_175_SURGICAL_AUDIT_BLOCKED",
    ]
    present = [verdict for verdict in verdicts if verdict in text]
    assert present == ["UI_UX_POST_1_175_SURGICAL_AUDIT_PASSED"]
    assert "ready_for_ui_ux_1_178_responsive_visual_checkpoint" in text
    assert (
        "PROMPT UI/UX 1.178 — Checkpoint responsive visual post fix 1.177 "
        "del Panel Maestro IA_CORE"
    ) in text


def test_each_commit_has_the_expected_scope_by_path():
    strategic_1_1 = commit_paths("ae1a462")
    strategic_1_2 = commit_paths("a20c6be")
    strategic_1_3 = commit_paths("dffe36e")
    selection_176 = commit_paths("e9f5b94")
    fix_177 = commit_paths("4403489")

    for paths in (strategic_1_1, strategic_1_2, strategic_1_3):
        assert all(
            path == "README.md" or path.startswith(("docs/", "tests/"))
            for path in paths
        )
        assert "ui/web/index.html" not in paths

    assert selection_176 == {
        "README.md",
        "docs/UI_UX_PANEL_MAESTRO_NEXT_VISUAL_BLOCK_SELECTION_1_176.md",
        "tests/test_ui_ux_panel_maestro_next_visual_block_selection_1_176.py",
        "ui/web/README.md",
    }
    assert fix_177 == {
        "README.md",
        "docs/UI_UX_PANEL_MAESTRO_RESPONSIVE_DEBT_FIX_1_177.md",
        "tests/test_ui_ux_panel_maestro_responsive_debt_fix_1_177.py",
        "ui/web/README.md",
        "ui/web/index.html",
    }


def test_sensitive_backend_runtime_integration_and_secret_paths_are_unchanged():
    changed = git(
        "diff",
        "--name-only",
        RANGE,
        "--",
        "api.py",
        "core",
        "domains",
        "providers",
        "tools",
        "scripts",
        "integrations",
        "runtime",
        "execution",
        ".env",
        "env",
        "secrets",
    )
    assert changed == ""
    assert not (ROOT / "core" / "api.py").exists()
    assert (ROOT / "api.py").is_file()
    assert blob("fdc2b7d", "api.py") == blob("4403489", "api.py")
    assert blob("fdc2b7d", "core/backend_internal_ui_payloads.py") == blob(
        "4403489", "core/backend_internal_ui_payloads.py"
    )


def test_active_ui_changes_are_limited_to_the_scoped_1_177_fix():
    active_ui = lines(
        git(
            "diff",
            "--name-only",
            RANGE,
            "--",
            "ui/web/index.html",
            "ui/web/backend-contract-widgets.js",
            "ui/web/i18n_es.json",
            "ui/web/admin-panels.js",
            "ui/web/console-interactions.js",
            "ui/web/domains.js",
            "ui/web/styles.css",
        )
    )
    assert active_ui == {"ui/web/index.html"}
    assert blob("fdc2b7d", "ui/web/backend-contract-widgets.js") == blob(
        "4403489", "ui/web/backend-contract-widgets.js"
    )
    added = "\n".join(
        line[1:]
        for line in git(
            "show", "--format=", "--unified=0", "4403489", "--", "ui/web/index.html"
        ).splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ).casefold()
    for marker in [
        "fetch(",
        "/api/",
        "preview-and-run",
        "ready to run",
        "running",
        "executing",
        "dispatching",
        "submitted",
        "processing request",
        "capability active",
        "localstorage",
        "location.hash",
    ]:
        assert marker not in added


def test_current_index_contains_no_prohibited_operational_actions():
    html = read(INDEX).casefold()
    for marker in [
        "preview-and-run",
        "ready to run",
        "running",
        "executing",
        "dispatching",
        "submitted",
        "processing request",
        "capability active",
    ]:
        assert marker not in html


def test_payload_v1_and_contract_widget_guards_are_preserved_without_v2():
    tracked = git("ls-tree", "-r", "--name-only", "4403489").casefold()
    assert "backend_internal_ui_payload.v2" not in tracked
    source = read(PAYLOAD_SOURCE)
    script = read(WIDGETS)
    active_contract = source + script + read(INDEX)
    assert "backend_internal_ui_payload.v2" not in active_contract
    for marker in [
        "backend_internal_ui_payload.v1",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "no_payload",
        "not_available",
        "source",
        "status",
        "fallback",
        "deny-by-default",
    ]:
        assert marker in active_contract
    assert "fetch(" not in script


def test_all_new_files_in_the_range_are_expected_and_classified():
    added = lines(git("diff", "--diff-filter=A", "--name-only", RANGE))
    assert added == EXPECTED_ADDED_FILES
    assert_markers(
        DOC,
        [
            "cuatro documentos estratégicos permitidos",
            "tres tests documentales permitidos",
            "dos documentos UI/UX permitidos",
            "dos tests UI/UX permitidos",
            "Archivos potencialmente inesperados: ninguno",
            "Duplicados documentales o contractuales: ninguno detectado",
        ],
    )


def test_strategic_docs_1_1_to_1_3_are_explicitly_future_only():
    strategic_docs = [
        ROOT / "docs" / "FUTURE_CORPORATE_AREAS_AND_SUBAREAS_MODEL.md",
        ROOT / "docs" / "FUTURE_INSTITUTIONAL_INTELLIGENCE_LAYER.md",
        ROOT / "docs" / "FUTURE_IA_CORE_OS_AND_DEVICE_ECOSYSTEM.md",
        ROOT / "docs" / "FUTURE_ROOT_CONTROL_PLANE_OWNER_NODES_AND_CONTINUITY_MODEL.md",
    ]
    for path in strategic_docs:
        text = normalized(read(path))
        assert "estado: futuro" in text
        assert "no implementado" in text
        assert "sin runtime" in text
        assert "sin execution" in text
        assert "sin endpoints" in text
        assert "sin integraciones reales" in text
        assert "sin credenciales" in text


def test_forbidden_phrase_matches_in_added_markdown_are_only_negative_or_future():
    diff = git("diff", "--unified=0", RANGE, "--", "*.md")
    added_lines = [
        line[1:].casefold()
        for line in diff.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]
    phrases = [
        "está operativo",
        "esta operativo",
        "está activo",
        "esta activo",
        "funciona actualmente",
        "ya funciona",
        "runtime activo",
        "ejecución real habilitada",
        "ejecucion real habilitada",
        "integraciones activas",
        "owner nodes funcionando",
        "inteligencia institucional activa",
        "paneles corporativos operativos",
        "failover automático activo",
        "failover automatico activo",
        "cloud conectado",
        "backups reales configurados",
        "clientes reales conectados",
    ]
    for line in added_lines:
        if any(phrase in line for phrase in phrases):
            assert any(
                guard in line
                for guard in ("no ", "sin ", "futuro", "futura", "prohib")
            ), line


def test_readmes_record_the_audit_and_readiness_briefly():
    assert_markers(
        README,
        [
            "Cursor vigente UI/UX 1.177.1",
            "fdc2b7d..4403489",
            "STRATEGIC DOCS 1.1-1.3",
            "UI/UX 1.176",
            "UI/UX 1.177",
            "sin desviar backend, runtime, payload ni UI activa",
            "listo para el checkpoint visual UI/UX 1.178",
        ],
    )
    assert_markers(
        WEB_README,
        [
            "Nota UI/UX 1.177.1",
            "fdc2b7d..4403489",
            "STRATEGIC DOCS 1.1-1.3",
            "UI/UX 1.176-1.177",
            "no desviaron backend, runtime, payload ni UI activa",
            "readiness confirmado hacia UI/UX 1.178",
        ],
    )


def test_1_177_fix_document_keeps_the_expected_decision():
    assert FIX_177.is_file()
    assert "UI_UX_RESPONSIVE_DEBT_PANEL_MAESTRO_RESOLVED" in read(FIX_177)


def test_current_prompt_diff_is_documentation_test_only():
    paths = changed_paths()
    assert paths <= ALLOWED_DIFF
    approved_active_ui = (
        APPROVED_1_180_ACTIVE_UI if REQUIRED_1_180 <= paths else set()
    )
    if CONTINUITY_1_186 <= paths:
        approved_active_ui |= {"ui/web/styles.css"}
    if CONTINUITY_1_189 <= paths:
        approved_active_ui |= {"ui/web/styles.css"}
    protected = {
        "ui/web/index.html",
        "ui/web/backend-contract-widgets.js",
        "ui/web/i18n_es.json",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
        "ui/web/styles.css",
        "api.py",
        "core/backend_internal_ui_payloads.py",
    }
    assert not (paths.intersection(protected) - approved_active_ui)
    assert not any(
        path.startswith(
            (
                "core/",
                "domains/",
                "providers/",
                "tools/",
                "scripts/",
                "integrations/",
                "runtime/",
                "execution/",
            )
        )
        for path in paths
    )


def test_current_scope_is_strict_1_192():
    assert_current_scope(ROOT)
