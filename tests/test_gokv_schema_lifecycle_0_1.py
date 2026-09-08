"""N2 schema and lifecycle tests for GOKV 0.1."""

from pathlib import Path

import pytest

from gokv.schema import (
    SCHEMA_VERSION,
    build_knowledge_item,
    compare_versions,
    transition_knowledge_item,
    validate_knowledge_item,
)


ROOT = Path(__file__).resolve().parents[1]


def evidence():
    return [{"evidence_id": "test_evidence", "kind": "test", "ref": "tests/example.py", "claim": "test passed"}]


def item(**overrides):
    values = {
        "knowledge_id": "example_rule",
        "kind": "PRINCIPLE",
        "title": "Example rule",
        "summary": "A rule with explicit evidence.",
        "evidence_refs": evidence(),
        "source_commits": ["7cb7134"],
        "source_checkpoints": ["checkpoint_0_1"],
        "confidence": {"level": "HIGH", "rationale": "repeated test evidence"},
    }
    values.update(overrides)
    return build_knowledge_item(**values)


def test_n2_machine_readable_schema_exists_and_builder_is_versioned():
    schema = ROOT / "knowledge/global_operational/schema/knowledge_item.schema.json"
    lifecycle = ROOT / "knowledge/global_operational/schema/lifecycle.schema.json"
    assert schema.is_file() and lifecycle.is_file()
    assert item()["schema_version"] == SCHEMA_VERSION
    assert item()["knowledge_version"] == "0.1.0"


def test_n2_required_lifecycle_transitions_are_explicit():
    observed = item(status="OBSERVED")
    candidate = transition_knowledge_item(observed, "CANDIDATE")
    validated = transition_knowledge_item(candidate, "VALIDATED")
    promoted = transition_knowledge_item(validated, "PROMOTED")
    revised = transition_knowledge_item(promoted, "REVISED", supersedes=["example_rule"])
    deprecated = transition_knowledge_item(revised, "DEPRECATED")
    replaced = transition_knowledge_item(deprecated, "REPLACED", superseded_by=["replacement_rule"])
    assert [candidate["status"], validated["status"], promoted["status"], revised["status"], deprecated["status"], replaced["status"]] == [
        "CANDIDATE", "VALIDATED", "PROMOTED", "REVISED", "DEPRECATED", "REPLACED"
    ]


def test_n2_promotion_and_replacement_require_evidence_and_references():
    with pytest.raises(ValueError, match="PROMOTED requiere evidence_refs"):
        item(status="PROMOTED", evidence_refs=[])
    with pytest.raises(ValueError, match="REPLACED requiere superseded_by"):
        item(status="REPLACED", superseded_by=[])
    with pytest.raises(ValueError, match="REVISED requiere supersedes"):
        item(status="REVISED", supersedes=[])


def test_n2_invalid_transition_version_scope_and_privacy_are_rejected():
    with pytest.raises(ValueError, match="transicion invalida"):
        transition_knowledge_item(item(status="OBSERVED"), "PROMOTED")
    with pytest.raises(ValueError, match="knowledge_version debe avanzar"):
        transition_knowledge_item(item(status="PROMOTED"), "REVISED", knowledge_version="0.1.0", supersedes=["example_rule"])
    with pytest.raises(ValueError, match="incompatible"):
        item(scope="GLOBAL", privacy_class="ia_core_internal")
    assert compare_versions("1.0.0", "0.9.9") == 1
