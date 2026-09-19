# Roadmap 4.x Macro 05.1 Execution Journal

The canonical JSON is the authoritative machine-readable journal. This document
records the station order and the invariants that must be maintained.

1. Preflight: main, expected Macro 05 HEAD, fetched origin, clean tree, 0/0, forecast.
2. Inspection: five Macro 05 commits and historical artifacts reconstructed.
3. Gate implementation: standard-library validator and negative controls added.
4. Assurance: additive P1 identity, source, isolation and side-effect claims added.
5. Basis: one real validation-basis commit established before Level B.
6. Readiness: focal, historical, Level A and readiness gate green.
7. Level B: full suite executed on the unchanged executable basis.
8. Evidence finalization: only documentary/evidence bytes changed after Level B.
9. Prelock: final evidence and post-evidence targeted gate green at lock parent.
10. Publication: one documentary lock, fetch, normal push, fetch, postpublish render.

No retry, rollback, or repair is silently omitted. Every attempt is represented in
`validation_runs`, including red attempts when they occur.
