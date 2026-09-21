"""Official public API and CLI for Micro-Mission 06.2.4-A."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.closure_assurance_v2_2_4_a import (  # noqa: E402
    MISSION_ID,
    MICRO_PROPERTY,
    _AuthorityResolutionFailure,
    _authorize_component,
    _canonical_bytes,
    _error_document,
    _sha256_bytes,
)


__all__ = ("authorize_component",)


def authorize_component(logical_artifact_id: str, semantic_role: str) -> bytes:
    """Authorize and return exact bytes for only the requested ID and role."""
    raw, _trace = _authorize_component(logical_artifact_id, semantic_role)
    return raw


def _main(argv: list[str]) -> int:
    root_flags = {"--repository-root", "--repo-root", "--commit", "--ref", "--branch"}
    authority_flags = {"--manifest", "--authority-set", "--authority-set-path", "--authority-manifest"}
    component_flags = {"--expected-sha", "--expected-sha256", "--loader", "--resolver", "--raw-bytes", "--component-path"}
    tokens = {token.split("=", 1)[0] for token in argv}
    try:
        if tokens & root_flags:
            raise _AuthorityResolutionFailure("REJECTED_CALLER_REPOSITORY_ROOT_SELECTION", "CLI cannot select root, commit, ref, or branch")
        if tokens & authority_flags:
            raise _AuthorityResolutionFailure("REJECTED_CALLER_AUTHORITY_SET_SELECTION", "CLI cannot select the authority manifest")
        if tokens & component_flags:
            raise _AuthorityResolutionFailure("REJECTED_CALLER_COMPONENT_SUBSTITUTE", "CLI cannot select a component, expected hash, loader, or resolver")
        if len(argv) != 3 or argv[0] != "resolve":
            raise _AuthorityResolutionFailure("REJECTED_UNSUPPORTED_CLI_ARGUMENT", "official CLI accepts only resolve logical_artifact_id semantic_role")
        logical_artifact_id, semantic_role = argv[1], argv[2]
        raw, trace = _authorize_component(logical_artifact_id, semantic_role)
        payload = {
            "mission_id": MISSION_ID,
            "micro_property": MICRO_PROPERTY,
            "result": "AUTHORIZED_BYTES_RELEASED",
            "logical_artifact_id": logical_artifact_id,
            "semantic_role": semantic_role,
            "released_byte_length": len(raw),
            "released_sha256": _sha256_bytes(raw),
            "authorization_trace": trace,
        }
        print(_canonical_bytes(payload).decode("utf-8"), end="")
        return 0
    except _AuthorityResolutionFailure as error:
        print(_canonical_bytes(_error_document(error)).decode("utf-8"), end="", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
