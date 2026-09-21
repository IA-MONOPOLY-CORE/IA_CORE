"""Official CLI for the fixed-profile Macro-Mission 06.2.4-B derivation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.closure_semantic_derivation_v2_2_4_b import (  # noqa: E402
    SemanticDerivationError,
    derive_semantic_facts,
)

__all__ = ("derive_semantic_facts",)


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] != "derive":
        result = {
            "result": "REJECTED_B_CALLER_PROVENANCE_SELECTION",
            "derivation_execution_state": "NOT_EVALUATED",
            "aggregate_semantic_result": "INDETERMINATE",
            "errors": [
                {
                    "code": "REJECTED_B_CALLER_PROVENANCE_SELECTION",
                    "message": "official B CLI accepts only: derive",
                }
            ],
        }
        print(json.dumps(result, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 2
    try:
        bundle = derive_semantic_facts()
    except SemanticDerivationError as exc:
        print(json.dumps(exc.as_result(), ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 1
    print(json.dumps(bundle.to_dict(), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
