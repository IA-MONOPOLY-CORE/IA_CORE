# Roadmap 4.x Macro 05.1 Historical Impact Manifest

The cohort is frozen before Level B and contains the four P1 suites, API admin
panels, Macro 05 E2E and closure guards, Macro 05.1 reconciliation and closure-gate
tests, Method Santi 3.2.4 and 3.2.5, affected historical guards, UI P1 consumers,
and any shared P4 precedent discovered by inspection.

`tests/historical_test_context.py` receives only exact nominal mappings for the
new mission artifacts. It does not use a broad glob, skip, xfail, snapshot
replacement, current-working-tree substitution, or removed assertion. New
documentary files are enumerated individually so old checkpoints continue to test
their own contracts.
