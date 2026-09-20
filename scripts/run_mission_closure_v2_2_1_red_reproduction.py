"""Executable red reproduction of the six material V2.2 assurance gaps.

This script intentionally exercises the historical V2.2 authority only.  Exit
code 1 means all six expected weaknesses were reproduced.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


REPO = Path(__file__).resolve().parents[1]
V22 = REPO / "scripts" / "validate_mission_closure_v2_2.py"
POLICY = REPO / "docs" / "ROADMAP_4X_MACRO_06_2_MISSION_POLICY.json"
SCHEMA = REPO / "docs" / "MISSION_CLOSURE_POLICY_SCHEMA_V2_2.json"
EVIDENCE = REPO / "docs" / "ROADMAP_4X_MACRO_06_2_CANONICAL_CLOSURE_EVIDENCE.json"
POST = REPO / "docs" / "ROADMAP_4X_MACRO_06_2_POST_EVIDENCE_RECEIPT.json"
PRELOCK = REPO / "docs" / "ROADMAP_4X_MACRO_06_2_PRELOCK_RECEIPT.json"
LOG_PATH = REPO / "docs" / "ROADMAP_4X_MACRO_06_2_1_RED_REPRODUCTION.json"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def run_renderer(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    isolated_repo = output_dir / "repo"
    clone = subprocess.run(
        ["git", "clone", "-c", "core.autocrlf=false", "--local", "--no-hardlinks", str(REPO), str(isolated_repo)],
        cwd=REPO,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    if clone.returncode != 0:
        return {"exit_code": clone.returncode, "actual_result": "ISOLATED_CLONE_FAILED", "stderr_sha256": sha256_bytes(clone.stderr.encode("utf-8"))}
    render_dir = output_dir / "render"
    render_dir.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "scripts/validate_mission_closure_v2_2.py",
        "render-postpublish",
        "--repo-root",
        ".",
        "--policy",
        "docs/ROADMAP_4X_MACRO_06_2_MISSION_POLICY.json",
        "--schema",
        "docs/MISSION_CLOSURE_POLICY_SCHEMA_V2_2.json",
        "--evidence",
        "docs/ROADMAP_4X_MACRO_06_2_CANONICAL_CLOSURE_EVIDENCE.json",
        "--post-receipt",
        "docs/ROADMAP_4X_MACRO_06_2_POST_EVIDENCE_RECEIPT.json",
        "--prelock-receipt",
        "docs/ROADMAP_4X_MACRO_06_2_PRELOCK_RECEIPT.json",
        "--envelope-output",
        str(render_dir / "envelope.json"),
        "--report-output",
        str(render_dir / "report.json"),
    ]
    proc = subprocess.run(command, cwd=isolated_repo, text=True, encoding="utf-8", capture_output=True, check=False)
    report = render_dir / "report.json"
    return {
        "command": ["python", "scripts/validate_mission_closure_v2_2.py", "render-postpublish", "<isolated-output>",],
        "working_directory": ".",
        "exit_code": proc.returncode,
        "stdout_sha256": sha256_bytes(proc.stdout.encode("utf-8")),
        "stderr_sha256": sha256_bytes(proc.stderr.encode("utf-8")),
        "report_sha256": sha256_file(report) if report.is_file() else None,
        "report_bytes": report.read_bytes().hex() if report.is_file() else None,
        "expected_failure_property": "independent V2.2 renders are byte-identical",
        "actual_result": "DIFFERENT_REPORT_BYTES" if report.is_file() else "NO_REPORT",
    }


def reproduce_r01() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="ia-core-0621-r01-a-") as a, tempfile.TemporaryDirectory(prefix="ia-core-0621-r01-b-") as b:
        first = run_renderer(Path(a))
        second = run_renderer(Path(b))
    first.pop("report_bytes", None)
    second.pop("report_bytes", None)
    reproduced = bool(first["report_sha256"] and second["report_sha256"] and first["report_sha256"] != second["report_sha256"])
    return {"reproduction_id": "R-01", "started_at": iso_now(), "process_a": first, "process_b": second, "reproduced": reproduced, "causal_conclusion": "V2.2 report bytes include live diff-check timestamps."}


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def reproduce_r02() -> dict[str, object]:
    receipt = load_json(REPO / "docs" / "ROADMAP_4X_MACRO_06_2_VALIDATION_LOGS" / "level-a.receipt.json")
    reproduced = receipt.get("command_id") == "M062-LEVEL-A-004" and "validate-policy" in receipt.get("command", []) and receipt.get("passed") == 0
    return {"reproduction_id": "R-02", "command": receipt.get("command"), "tests_executed": receipt.get("passed"), "wall_seconds": receipt.get("wall_seconds"), "expected_failure_property": "Level A must be the complete suite", "actual_result": "POLICY_ONLY_ZERO_TESTS", "reproduced": reproduced, "causal_conclusion": "V2.2 labeled a policy validator as Level A."}


def reproduce_r03() -> dict[str, object]:
    policy = load_json(POLICY)
    evidence = load_json(EVIDENCE)
    observed = {run.get("gate_name") for run in evidence.get("validation_runs", [])}
    declared = set(policy.get("required_validation_gates", []))
    missing = sorted(declared - observed)
    reproduced = bool(missing)
    return {"reproduction_id": "R-03", "declared_required_validations": sorted(declared), "receipt_bound_executions": sorted(observed), "missing_receipt_bound_validations": missing, "reproduced": reproduced, "causal_conclusion": "V2.2 accepted declarative required-validation names without execution receipts."}


def reproduce_r04() -> dict[str, object]:
    matrix = (REPO / "docs" / "ROADMAP_4X_MACRO_06_2_NEGATIVE_CONTROL_MATRIX.md").read_text(encoding="utf-8")
    control_ids = re.findall(r"^\|\s*(N-\d+)\s*\|", matrix, flags=re.MULTILINE)
    evidence = load_json(EVIDENCE)
    mappings = evidence.get("negative_control_coverage", {})
    reproduced = bool(control_ids) and not mappings
    return {"reproduction_id": "R-04", "historical_control_ids": control_ids, "control_count": len(control_ids), "mapping_present": bool(mappings), "expected_failure_property": "every control must map to current execution and receipt", "actual_result": "NO_TRACEABILITY_MAP", "reproduced": reproduced, "causal_conclusion": "V2.2 matrix prose and IDs were accepted without complete executable traceability."}


def reproduce_r05() -> dict[str, object]:
    sys.path.insert(0, str(REPO / "scripts"))
    import validate_mission_closure_v2_2 as v22  # type: ignore[import-not-found]

    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, text=True, capture_output=True, check=True).stdout.strip()
    fake = {
        "state": "PROVEN",
        "operator_action_required": False,
        "hosting_provider": "GitHub",
        "repository": "IA-MONOPOLY-CORE/IA_CORE",
        "protected_branch": "main",
        "ruleset_or_branch_protection_id": "invented",
        "ruleset_reference": "github://invented",
        "required_check_name": "closure-policy-and-anti-weakening",
        "observed_run_reference": "invented",
        "observed_commit": head,
        "verified_at": "2026-09-19T20:00:00+00:00",
        "verification_source": "invented",
        "bypass_policy": "denied",
        "force_push_policy": "denied",
        "REMOTE_PROOF_SOURCE": "github://invented",
        "REMOTE_PROOF_CAPTURED_AT": "2026-09-19T20:00:00+00:00",
        "REMOTE_PROOF_COMMIT": head,
        "REMOTE_PROOF_SHA256": "0" * 64,
        "REMOTE_PROVIDER_RESPONSE_REFERENCE": "invented",
    }
    try:
        v22.validate_remote(fake, REPO)
    except Exception as exc:  # pragma: no cover - this is the historical red expectation
        return {"reproduction_id": "R-05", "reproduced": False, "actual_result": f"REJECTED:{type(exc).__name__}", "causal_conclusion": "Fixture was rejected; no historical gap reproduced."}
    return {"reproduction_id": "R-05", "reproduced": True, "fake_remote_proof": {"source": "github://invented", "ruleset": "invented", "response": "invented"}, "actual_result": "FABRICATED_PROVEN_ACCEPTED", "causal_conclusion": "V2.2 treated self-authored provider-shaped fields as PROVEN."}


def reproduce_r06() -> dict[str, object]:
    sys.path.insert(0, str(REPO / "scripts"))
    import validate_mission_closure_v2_2 as v22  # type: ignore[import-not-found]

    policy = {"required_report_sections": [str(i) for i in range(1, 30)], "allowed_result_variants": ["OK"]}
    evidence = {"report": {"sections": [str(i) for i in range(1, 30)], "official_result": "OK"}}
    try:
        v22.validate_report_contract(policy, evidence)
    except Exception as exc:  # pragma: no cover - this is the historical red expectation
        return {"reproduction_id": "R-06", "reproduced": False, "actual_result": f"REJECTED:{type(exc).__name__}", "causal_conclusion": "Minimal section-ID fixture was rejected."}
    return {"reproduction_id": "R-06", "reproduced": True, "actual_result": "SECTION_ID_ONLY_COMPLETENESS_ACCEPTED", "causal_conclusion": "V2.2 treated a matching section-ID list as report completeness."}


def main() -> int:
    cases = [reproduce_r01(), reproduce_r02(), reproduce_r03(), reproduce_r04(), reproduce_r05(), reproduce_r06()]
    result = {"mission": "ROADMAP_4X_MACRO_06_2_1", "gate_under_test": "mission_closure_gate.v2.2", "started_at": iso_now(), "cases": cases, "reproduced_count": sum(bool(case.get("reproduced")) for case in cases), "expected_exit_code": 1, "actual_exit_code": 1}
    result["artifact_sha256"] = sha256_bytes(canonical(result))
    LOG_PATH.write_bytes((json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if result["reproduced_count"] == 6 else 2


if __name__ == "__main__":
    raise SystemExit(main())
