"""Strict snapshot and station-group helpers for UI/UX 1.196."""

from dataclasses import dataclass
from pathlib import Path
import subprocess

import ui_ux_1_196_continuity as continuity


ROOT = Path(__file__).resolve().parents[1]
CSS = continuity.CSS


@dataclass(frozen=True)
class SnapshotRef:
    commit: str
    path: str


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def known_commit(commit: str) -> bool:
    return subprocess.run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=ROOT).returncode == 0


def assert_known_commit(commit: str) -> None:
    if not known_commit(commit):
        raise AssertionError(f"unknown snapshot commit: {commit}")


def snapshot(ref: SnapshotRef) -> str:
    assert_known_commit(ref.commit)
    if not ref.path or ref.path.startswith("/") or ".." in Path(ref.path).parts:
        raise AssertionError(f"snapshot path outside repository: {ref.path}")
    return git("show", f"{ref.commit}:{ref.path}")


def compare_snapshots(before: SnapshotRef, after: SnapshotRef) -> tuple[str, str]:
    return snapshot(before), snapshot(after)


def assert_exact_group(station: str, paths: set[str]) -> None:
    expected = continuity.exact_station_paths(station)
    unexpected = set(paths) - expected
    if unexpected:
        raise AssertionError(f"station {station} contains unregistered paths: {sorted(unexpected)}")


def assert_allowed_paths(paths: set[str]) -> None:
    continuity.assert_rejects_paths(set(paths))


def assert_product_unchanged(base: str = continuity.BASELINE, head: str = "HEAD") -> None:
    continuity.assert_protected_product_unchanged(base, head)


def assert_no_selector_outside_scope(selector: str, allowed_selectors: set[str]) -> None:
    if selector not in allowed_selectors:
        raise AssertionError(f"selector outside station scope: {selector}")


def assert_historical_guard_preserved(original: str, revised: str) -> None:
    if revised.count("assert ") < original.count("assert "):
        raise AssertionError("historical assertions were removed")
    for marker in ("subprocess", "git", "HEAD", "BASE"):
        if marker in original and marker not in revised:
            raise AssertionError(f"historical guard marker removed: {marker}")


def assert_no_contract_modification(before: str, after: str) -> None:
    protected = (
        "allowed_actions", "forbidden_actions", "blocked_capabilities", "backend_internal_ui_payload.v1",
        "no_payload", "not_available", "data-contract-blocked", "aria-disabled", "data-no-runtime",
        "data-no-execution", "data-no-mutation",
    )
    for marker in protected:
        if marker in before and marker not in after:
            raise AssertionError(f"contract marker disappeared: {marker}")


def assert_no_weakening(source: str) -> None:
    forbidden = (
        "except " + "AssertionError" + ": pass",
        "return " + "True  # bypass",
        "assert " + "False or",
        "allow " + "all",
    )
    for marker in forbidden:
        if marker.casefold() in source.casefold():
            raise AssertionError(f"guard weakening marker: {marker}")
