"""Focal contract-surface mapping guard for UI/UX 1.198 N4."""

from collections import Counter
from pathlib import Path

from ui_ux_panel_maestro_microcopy_1_198_support import (
    contract_surface_maps,
    corpus_items,
    protected_files_match_baseline,
)


EXPECTED_BINDINGS = {
    "DIRECT_CONTRACT_BINDING": 831,
    "INDIRECT_CONTRACT_CONTEXT": 159,
    "PRESENTATIONAL_ONLY": 130,
    "EDITORIAL_ONLY": 408,
    "UNKNOWN_BINDING": 0,
    "DIRECTION_REQUIRED_BINDING": 96,
}


def test_n4_document_has_binding_categories_and_contract_boundaries():
    doc = Path(__file__).resolve().parents[1] / "docs" / "UI_UX_PANEL_MAESTRO_MICROCOPY_CONTRACT_SURFACE_MAP_1_198.md"
    content = doc.read_text(encoding="utf-8").casefold()
    for marker in (
        "n4_microcopy_contract_surface_map_passed",
        "direct_contract_binding",
        "indirect_contract_context",
        "presentational_only",
        "editorial_only",
        "unknown_binding",
        "direction_required_binding",
        "fsc-co-01",
        "fsc-bf-02",
        "fsc-vr-03",
        "fsc-rcp-04",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "deny-by-default",
    ):
        assert marker in content, marker


def test_n4_every_record_has_surface_contract_authority_and_owner():
    items = corpus_items()
    mappings = contract_surface_maps(items)
    assert len(mappings) == len(items)
    fields = {
        "microcopy_id", "surface", "contract_anchor", "binding_type", "contract",
        "authority", "payload_or_source", "owner", "state", "risk", "dependency",
        "future_change",
    }
    for mapping in mappings:
        assert fields <= mapping.__dict__.keys()
        assert mapping.microcopy_id and mapping.surface and mapping.contract_anchor
        assert mapping.contract and mapping.authority and mapping.owner
        assert mapping.binding_type in EXPECTED_BINDINGS
    assert len({mapping.microcopy_id for mapping in mappings}) == len(mappings)


def test_n4_binding_counts_and_required_surface_anchors_are_frozen():
    mappings = contract_surface_maps()
    assert Counter(item.binding_type for item in mappings) == Counter(EXPECTED_BINDINGS)
    assert Counter(item.surface for item in mappings)["REQUEST_DRAFT_PANEL"] == 167
    assert Counter(item.surface for item in mappings)["CONTRACT_AWARE_WIDGETS"] == 256
    assert Counter(item.surface for item in mappings)["P2_P3_MATRIX_CLOSURE"] == 120
    assert Counter(item.surface for item in mappings)["P1_VALIDATION_READINESS"] == 100
    assert not any(item.binding_type == "UNKNOWN_BINDING" for item in mappings)
    assert protected_files_match_baseline() == []
