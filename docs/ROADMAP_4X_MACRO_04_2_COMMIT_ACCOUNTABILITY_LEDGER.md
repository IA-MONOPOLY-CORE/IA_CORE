# Roadmap 4.x Macro-Mission 04.2

## Commit accountability ledger

Baseline: `01c45650ad8a5a3322a3326e7f6d4c5d90d796df` on `main`.

| Station | Commit | Responsibility | State |
| --- | --- | --- | --- |
| Owner/security direction and future contracts | `f3c1884d78d175252880e050aa1cec609d5c8a0a` | Reconcile native security, offensive ingestion and IA_CORE OS direction | published |
| E2E assurance and security G0 | `cae6d4695c668442c8e278d1a642a4a07e7c1129` | Extend graph, schema and validator | published |
| Adversarial assurance guards | `42b22f5981075a148e7c74bd41be75b0cd4a2f87` | Add Macro 04.2 tests and exact continuity allowlists | published |
| Metrics and truth matrix | `2e81ca35c0f017d8603a66e54d81dbd5cf9b96a1` | Reuse GOKV metric schema and record evidence contract | published provisional |
| Provisional validation basis | `dfb120a49d9ff159574c6bd11cf1198b620739b0` | Initial pre-suite marker | superseded after 3 nominal historical allowlist failures |
| Historical exact guard continuity | `2fdb5b54e694ab966d39006dc79402d006be8cab` | Add only the two exact missing paths to three historical guards | published |
| Validation basis | `7f18aa14d2245f4d26aa86963f946e7a0e2b73b7` | Official pre-suite commit after all functional changes | `LEVEL_A_AND_LEVEL_B_PASS` |
| Final checkpoint evidence | self-referential final HEAD | Final docs, evidence and ledger; exact containing hash is intentionally not copied into its own evidence | prepared for publication |

## Accountability rules

The validation basis is an intentional marker commit after all content changes.
Historical assertions remain intact; every guard change is nominal and
path-specific. No product, runtime, provider,
tenant, payload, offensive or model-training surface is in scope.

The final evidence deliberately does not chase its own containing commit hash.
The post-fetch HEAD, remote equality and `0/0` state are confirmed by the final
report.
