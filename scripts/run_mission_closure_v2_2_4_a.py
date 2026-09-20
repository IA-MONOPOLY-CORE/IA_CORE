"""Real successor entrypoint for Roadmap 4.x Macro-Mission 06.2.4-A."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.closure_assurance_v2_2_4_a import (
    AuthorityResolutionFailure,
    MISSION_ID,
    MICRO_PROPERTY,
    build_authoritative_resolver,
    canonical_bytes,
    rejection_document,
    sha256_bytes,
)


def authorize_component(logical_artifact_id: str, semantic_role: str) -> bytes:
    """The successor path accepts only a logical id and semantic role."""
    resolver = build_authoritative_resolver()
    return resolver.resolve(logical_artifact_id, semantic_role)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="run_mission_closure_v2_2_4_a.py")
    subparsers = parser.add_subparsers(dest="command", required=True)
    resolve = subparsers.add_parser("resolve")
    resolve.add_argument("logical_artifact_id")
    resolve.add_argument("semantic_role")
    return parser


def _render_success(logical_artifact_id: str, semantic_role: str, raw: bytes, trace: dict) -> dict:
    return {
        "mission_id": MISSION_ID,
        "micro_property": MICRO_PROPERTY,
        "result": "AUTHORIZED_BYTES_RELEASED",
        "logical_artifact_id": logical_artifact_id,
        "semantic_role": semantic_role,
        "released_byte_length": len(raw),
        "released_sha256": sha256_bytes(raw),
        "authorization_trace": trace,
    }


def main(argv: list[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    try:
        # Reject common caller-controlled authority selectors before argparse.
        root_overrides = {"--repo-root", "--repository-root"}
        authority_overrides = {"--authority-set", "--authority-set-path", "--authority-manifest"}
        component_overrides = {"--expected-sha256", "--component-path", "--raw-bytes", "--loader", "--resolver"}
        tokens = {token.split("=", 1)[0] for token in raw_argv}
        if tokens & root_overrides:
            raise AuthorityResolutionFailure("REJECTED_CALLER_REPOSITORY_ROOT_SELECTION", "caller cannot select the authority repository root")
        if tokens & authority_overrides:
            raise AuthorityResolutionFailure("REJECTED_CALLER_AUTHORITY_SET_SELECTION", "caller cannot select the authority set")
        if tokens & component_overrides:
            raise AuthorityResolutionFailure("REJECTED_CALLER_COMPONENT_SUBSTITUTE", "caller cannot select a component, hash, loader, or resolver")
        args = _parser().parse_args(raw_argv)
        if args.command != "resolve":
            raise AuthorityResolutionFailure("REJECTED_CALLER_COMPONENT_SUBSTITUTE", "unsupported successor command")
        resolver = build_authoritative_resolver()
        raw = resolver.resolve(args.logical_artifact_id, args.semantic_role)
        print(canonical_bytes(_render_success(args.logical_artifact_id, args.semantic_role, raw, resolver.authorization_trace())).decode("utf-8"), end="")
        return 0
    except AuthorityResolutionFailure as error:
        print(canonical_bytes(rejection_document(error)).decode("utf-8"), end="", file=sys.stderr)
        return 1
    except SystemExit:
        # argparse rejects unsupported caller-selected arguments without opening any component.
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
