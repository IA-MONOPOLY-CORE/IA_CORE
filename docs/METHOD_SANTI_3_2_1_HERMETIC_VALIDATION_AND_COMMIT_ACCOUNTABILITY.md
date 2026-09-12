# Method Santi 3.2.1 - Hermetic Validation and Commit Accountability

## Relationship to Method Santi 3.2

Method Santi 3.2.1 is an additive evolution of
`docs/METHOD_SANTI_3_2_GOVERNED_CAPABILITY_EXPANSION.md`. It preserves the
known-map, governed-surface, station, ambiguity, frontier, learning, capability,
human-authority, and maturity rules of 3.2. It does not replace the method,
rewrite its history, or create runtime authority.

## Mandatory rules

1. **TEST_SAFETY_MUST_BE_ENFORCED_NOT_ASSUMED**: a green end state does not
   prove that a test was safe. The boundary must reject unsafe operations.
2. **COLLECTION_MUST_BE_SIDE_EFFECT_FREE**: import and collection cannot start
   providers, network, credentials, runtime, persistence, or hidden execution.
3. **NO_PHANTOM_TEST_WRITES**: test writes must use `tmp_path`, a temporary
   sandbox, or an injected root. Tracked and product persistence paths fail
   immediately.
4. **RESTORE_IS_NOT_HERMETICITY**: restoring a repository after a test is
   recovery evidence only; it is not evidence that no side effect occurred.
5. **ONE_STATION_ONE_COMMIT**: every new coherent station contains its own
   implementation or correction, tests, documentation, evidence, and green
   result in one commit.
6. **EVERY_COMMIT_IS_ACCOUNTABLE**: inherited ranges are inspected by real
   diff, full hash, parent, paths, tests, dependencies, rollback, side effects,
   and verdict. Commit subjects are never sufficient evidence.
7. **REPAIR_PARITY_IS_EXPLICIT**: a historical repair lacking a full station is
   recorded as a parity deviation; it is not silently grouped or relabeled.
8. **LEARNING_OR_REUSE_IS_MANDATORY**: every relevant observation is either
   mapped to an existing knowledge ID with evidence or stored as a candidate.
   Promotion remains governed and non-automatic.
9. **VALIDATE_BEFORE_SCALING**: collection, side-effect, focal, historical,
   compile, diff, secret, and boundary checks pass before another surface is
   opened.

## Enforcement pattern

The test root guard loads before test modules, disables external egress by
default, and offers only the explicit `IA_CORE_ALLOW_EXTERNAL_TESTS=1` opt-in
for external probes. The test fixture injects temporary persistence roots. A
filesystem audit guard rejects protected writes immediately, and a session
status comparison detects tracked-state changes at the end of the run.

## Station gate

The next station may start only when the current station records exact commands,
counts, warnings, exclusions, and boundary results. A baseline failure may be
carried only when it is independently classified as out of scope, does not
invalidate the current station, and is not hidden as a pass.

## Stop conditions

Stop and report if a test requires product modification, a real provider,
network, credential value, runtime, payload, endpoint, integration, or an
unresolved human/contract decision. Do not use destructive reset, history rewrite,
broad guard relaxation, or silent skips to force closure.
