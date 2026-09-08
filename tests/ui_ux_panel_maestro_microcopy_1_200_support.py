"""Allowlist and preservation support for UI/UX 1.200.

This module is test-only. It compiles the 1.199 corpus into an explicit,
machine-readable decision surface and keeps all non-authorized categories
visible to focused guards.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import subprocess

from ui_ux_panel_maestro_microcopy_1_198_support import (
    contract_surface_maps,
    corpus_items,
    decision_package_rows,
    semantic_classifications,
)
from ui_ux_panel_maestro_microcopy_1_199_support import (
    decision_unit_membership,
    decision_units,
    determinism_boundary,
    direction_packages,
)


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "4618c59"
ALLOWLIST_PATH = ROOT / "tests" / "fixtures" / "ui_ux_1_200_microcopy_direction_allowlist.json"

DECISIONS = {
    "PKG_B_EDITORIAL_STYLE": "B",
    "PKG_B_CONSISTENCY_RULE": "A",
    "PKG_B_GEOMETRY_REMEDIATION": "B",
    "PKG_C_CONTEXTUAL_VARIANTS": "A",
    "PKG_C_CONTRACT_SENSITIVE": "A",
    "PKG_C_ACTION_PERMISSION": "A",
    "PKG_C_AMBIGUOUS_ROLE": "A",
    "PKG_D_CONTRACT_VOCABULARY": "A",
}

CHANGE_CLASSES = (
    "ALLOWED_EDITORIAL_CHANGE",
    "ALLOWED_GEOMETRY_CHANGE",
    "KEEP_EXACT",
    "KEEP_CONTEXTUAL",
    "KEEP_CONTRACT",
    "KEEP_ACTION_PERMISSION",
    "KEEP_AMBIGUOUS_ROLE",
    "KEEP_LEVEL_D",
    "KEEP_NO_DECISION",
)

PACKAGE_CLASSES = {
    "PKG_B_EDITORIAL_STYLE": "ALLOWED_EDITORIAL_CHANGE",
    "PKG_B_CONSISTENCY_RULE": "KEEP_CONTEXTUAL",
    "PKG_B_GEOMETRY_REMEDIATION": "ALLOWED_GEOMETRY_CHANGE",
    "PKG_C_CONTEXTUAL_VARIANTS": "KEEP_CONTEXTUAL",
    "PKG_C_CONTRACT_SENSITIVE": "KEEP_CONTRACT",
    "PKG_C_ACTION_PERMISSION": "KEEP_ACTION_PERMISSION",
    "PKG_C_AMBIGUOUS_ROLE": "KEEP_AMBIGUOUS_ROLE",
    "PKG_D_CONTRACT_VOCABULARY": "KEEP_LEVEL_D",
}

PACKAGE_REASONS = {
    "ALLOWED_EDITORIAL_CHANGE": "Decision 1 B: scoped editorial pattern only; preserve meaning, authority, semantics and context.",
    "ALLOWED_GEOMETRY_CHANGE": "Decision 3 B: scoped CSS/layout remediation for demonstrated geometry only.",
    "KEEP_EXACT": "Inherited contract-preservation outcome; no wording change is implied.",
    "KEEP_CONTEXTUAL": "Decision 2/4 A: preserve each context and reject broad canonization.",
    "KEEP_CONTRACT": "Decision 5 A: keep contract-sensitive blockers, warnings, errors, limits and evidence exact.",
    "KEEP_ACTION_PERMISSION": "Decision 6 A: keep declared action/permission data as read-only boundary.",
    "KEEP_AMBIGUOUS_ROLE": "Decision 7 A: keep the current formulation; do not reinterpret the role.",
    "KEEP_LEVEL_D": "Decision 8 A: keep the active contract; no vocabulary or payload version change.",
    "KEEP_NO_DECISION": "N2 KEEP_NO_DECISION ledger: preserve the current record without inference.",
}

EXPECTED_GEOMETRY_CSS = """\n/* UI/UX 1.200 N5: remediate only the measured local geometry risks. */\nbody .ia-core-shell[data-visual-hierarchy-first-pass=\"1.180\"] [data-main-console-zone=\"readiness\"] .readiness-card,\nbody .ia-core-shell[data-visual-hierarchy-first-pass=\"1.180\"] [data-main-console-zone=\"readiness\"] .readiness-card .layout-value {\n    min-width: 0;\n}\n\nbody .ia-core-shell[data-visual-hierarchy-first-pass=\"1.180\"] [data-main-console-zone=\"readiness\"] .readiness-card .layout-value {\n    overflow-wrap: anywhere;\n    word-break: break-word;\n}\n\nbody .ia-core-shell[data-visual-hierarchy-first-pass=\"1.180\"] .state-guidance-card strong,\nbody .ia-core-shell[data-visual-hierarchy-first-pass=\"1.180\"] .state-guidance-card span {\n    min-width: 0;\n    overflow-wrap: anywhere;\n}\n\n/* Keep the existing read-only disclosure tab fully inside the viewport. */\nbody #request-draft-panel.request-draft-panel.collapsed {\n    width: 44px !important;\n    max-width: 44px !important;\n    transform: none !important;\n    overflow: hidden;\n}\n"""
EXPECTED_GEOMETRY_CSS += """\nbody #request-draft-panel.request-draft-panel.collapsed .request-draft-toggle {\n    width: 43px !important;\n    min-width: 43px !important;\n}\n"""
EXPECTED_GEOMETRY_CSS = EXPECTED_GEOMETRY_CSS.replace(
    "    max-width: 44px !important;\n",
    "    max-width: 44px !important;\n    right: 1px !important;\n",
)


def _context() -> tuple[list, dict, dict, dict, dict, dict]:
    items = corpus_items()
    units = decision_units(items)
    membership = decision_unit_membership(units)
    boundaries = {row.decision_unit_id: row for row in determinism_boundary(units)}
    packages = direction_packages(units)
    package_by_unit = {
        unit_id: package.direction_package_id
        for package in packages
        for unit_id in package.unit_ids
    }
    classifications = {row.microcopy_id: row for row in semantic_classifications(items)}
    mappings = {row.microcopy_id: row for row in contract_surface_maps(items)}
    rows = {row.microcopy_id: row for row in decision_package_rows(items)}
    return items, membership, boundaries, package_by_unit, classifications, mappings | {"__rows__": rows}


def expected_allowlist() -> list[dict[str, object]]:
    items, membership, boundaries, package_by_unit, classifications, mappings = _context()
    rows = mappings.pop("__rows__")
    result: list[dict[str, object]] = []
    for item in items:
        unit_id = membership[item.microcopy_id]
        package_id = package_by_unit.get(unit_id)
        boundary = boundaries[unit_id]
        if package_id is None:
            change_class = "KEEP_NO_DECISION" if boundary.resolution == "KEEP_NO_DECISION" else "KEEP_EXACT"
            direction = "INHERITED_KEEP"
            package_id = "LEVEL_A_INHERITED"
        else:
            change_class = PACKAGE_CLASSES[package_id]
            direction = DECISIONS[package_id]
        mapping = mappings[item.microcopy_id]
        package_row = rows[item.microcopy_id]
        result.append({
            "direction_package": package_id,
            "decision_unit_id": unit_id,
            "microcopy_id": item.microcopy_id,
            "text": item.text,
            "source": item.source,
            "file": item.file,
            "location": item.location,
            "surface": mapping.surface,
            "authority": mapping.authority,
            "classification": classifications[item.microcopy_id].classification,
            "decision_category": package_row.decision_category,
            "approved_decision": direction,
            "change_class": change_class,
            "current_text_is_preserved": change_class not in {"ALLOWED_EDITORIAL_CHANGE", "ALLOWED_GEOMETRY_CHANGE"},
            "reason": PACKAGE_REASONS[change_class],
        })
    return result


def load_allowlist() -> dict[str, object]:
    return json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))


def allowlist_items() -> list[dict[str, object]]:
    return list(load_allowlist()["items"])


def allowlist_counts(items: list[dict[str, object]] | None = None) -> Counter[str]:
    entries = items if items is not None else allowlist_items()
    return Counter(str(item["change_class"]) for item in entries)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def baseline_bytes(relative_path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{BASELINE}:{relative_path}"], cwd=ROOT)


def protected_product_paths() -> tuple[str, ...]:
    return (
        "ui/web/index.html",
        "ui/web/i18n_es.json",
        "ui/web/backend-contract-widgets.js",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
        "core/backend_internal_ui_payloads.py",
        "api.py",
    )


def protected_files_match_baseline() -> list[str]:
    return [
        path for path in protected_product_paths()
        if (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
        != baseline_bytes(path).replace(b"\r\n", b"\n")
    ]
