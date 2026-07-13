import pytest

from core.artifact_state import (
    ArtifactState,
    STATE_DESCRIPTIONS,
    VALID_TRANSITIONS,
    can_activate,
    can_materialize,
    coerce_artifact_state,
    is_derived,
    is_materialized,
    is_operational,
    is_valid_transition,
    is_visible_as_usable,
    must_not_be_used_as_operational,
    require_valid_transition,
)


def test_all_states_have_descriptions():
    assert set(STATE_DESCRIPTIONS) == set(ArtifactState)
    assert all(description.strip() for description in STATE_DESCRIPTIONS.values())


def test_derived_preview_is_not_operational():
    assert is_derived(ArtifactState.DERIVED_PREVIEW)
    assert not is_materialized(ArtifactState.DERIVED_PREVIEW)
    assert not is_operational(ArtifactState.DERIVED_PREVIEW)
    assert not is_visible_as_usable(ArtifactState.DERIVED_PREVIEW)
    assert must_not_be_used_as_operational(ArtifactState.DERIVED_PREVIEW)


def test_ready_to_materialize_is_not_operational():
    assert is_derived(ArtifactState.READY_TO_MATERIALIZE)
    assert can_materialize(ArtifactState.READY_TO_MATERIALIZE)
    assert not is_operational(ArtifactState.READY_TO_MATERIALIZE)
    assert not is_visible_as_usable(ArtifactState.READY_TO_MATERIALIZE)


def test_materialized_does_not_automatically_mean_active():
    assert is_materialized(ArtifactState.MATERIALIZED)
    assert can_activate(ArtifactState.MATERIALIZED)
    assert not is_operational(ArtifactState.MATERIALIZED)
    assert not is_visible_as_usable(ArtifactState.MATERIALIZED)


def test_active_is_operational_passed_only_with_traceability():
    assert is_materialized(ArtifactState.ACTIVE)
    assert is_operational(ArtifactState.ACTIVE, has_traceability=True)
    assert is_visible_as_usable(ArtifactState.ACTIVE, has_traceability=True)
    assert not is_operational(ArtifactState.ACTIVE, has_traceability=False)
    assert not is_visible_as_usable(ArtifactState.ACTIVE, has_traceability=False)


@pytest.mark.parametrize(
    "state",
    [ArtifactState.ARCHIVED, ArtifactState.LEGACY, ArtifactState.BROKEN],
)
def test_non_operational_terminal_or_historical_states_are_not_usable(state):
    assert not is_operational(state)
    assert not is_visible_as_usable(state)
    assert must_not_be_used_as_operational(state)


def test_valid_transitions_are_defined():
    expected = {
        (ArtifactState.DERIVED_PREVIEW, ArtifactState.READY_TO_MATERIALIZE),
        (ArtifactState.READY_TO_MATERIALIZE, ArtifactState.MATERIALIZED),
        (ArtifactState.MATERIALIZED, ArtifactState.ACTIVE),
        (ArtifactState.ACTIVE, ArtifactState.ARCHIVED),
        (ArtifactState.MATERIALIZED, ArtifactState.ARCHIVED),
        (ArtifactState.LEGACY, ArtifactState.READY_TO_MATERIALIZE),
        (ArtifactState.DERIVED_PREVIEW, ArtifactState.BROKEN),
        (ArtifactState.BROKEN, ArtifactState.DERIVED_PREVIEW),
        (ArtifactState.BROKEN, ArtifactState.READY_TO_MATERIALIZE),
    }

    for from_state, to_state in expected:
        assert to_state in VALID_TRANSITIONS[from_state]
        assert is_valid_transition(from_state, to_state)
        assert require_valid_transition(from_state, to_state) is to_state


@pytest.mark.parametrize(
    ("from_state", "to_state"),
    [
        (ArtifactState.DERIVED_PREVIEW, ArtifactState.ACTIVE),
        (ArtifactState.READY_TO_MATERIALIZE, ArtifactState.ACTIVE),
        (ArtifactState.LEGACY, ArtifactState.ACTIVE),
        (ArtifactState.BROKEN, ArtifactState.ACTIVE),
        (ArtifactState.ARCHIVED, ArtifactState.ACTIVE),
    ],
)
def test_invalid_transitions_are_rejected(from_state, to_state):
    assert not is_valid_transition(from_state, to_state)
    with pytest.raises(ValueError, match="Transicion de artefacto invalida"):
        require_valid_transition(from_state, to_state)


def test_unknown_states_never_pass_as_operational():
    unknown = "proposed"

    assert coerce_artifact_state(unknown) is None
    assert not is_derived(unknown)
    assert not is_materialized(unknown)
    assert not is_operational(unknown)
    assert not is_visible_as_usable(unknown)
    assert must_not_be_used_as_operational(unknown)
    assert not is_valid_transition(unknown, ArtifactState.ACTIVE)
    with pytest.raises(ValueError, match="desconocido"):
        require_valid_transition(unknown, ArtifactState.ACTIVE)
