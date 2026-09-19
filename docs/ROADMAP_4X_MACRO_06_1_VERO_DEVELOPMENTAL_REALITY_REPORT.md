# Roadmap 4.x Macro-Mission 06.1 - VERO Developmental Reality Report

Status: `DEVELOPMENTAL_DOCUMENTARY_ONLY`.

This is the first bounded VERO exercise. It records repository reality and
the limits of the record. It does not implement a VERO runtime and does not
re-adjudicate Macro 06.

## Reality answers

### What actually happened

The Macro 06 V2 authority was reproduced as insufficient in five executable
areas: real-diff scope enforcement, computed protected-diff enforcement,
causal chronology, CI job identity, and evolvable remote state. The red
reproduction was preserved in commit `a4a9fb9fc8ee166fcac24b9c3bb3371d186da8de`.
Its corrected fixture run recorded `5 failed, 1 warning`, exit `1`, start
`2026-09-19T14:45:43.5140354-03:00`, end
`2026-09-19T14:46:27.0338614-03:00`, wall `43.519826 s`.

V2.1 then added Git-derived scope, path classification, protected-diff
calculation, causal clocks, receipts, an independent CI job contract and
three-state remote enforcement. The final Level A and Level B runs were
green without product changes.

### What was claimed

The predecessor audit reported that V2 policy fields and protected surfaces
were declared but not fully adjudicated against live Git state; that a CI
step was being treated as a required check; and that the remote state model
was rigid. These are recorded as `REPORTED` facts with the attached mission
prompt as source, not as an attribution of intent.

### What was machine enforced

V2.1 enforces exact policy paths, real Git manifests, normalized paths,
classification precedence, no rename/copy evasion, no protected/product
paths, post-basis category restrictions, causal clocks, actual receipt
hashes, report sections, historical bytes, CI job identity, and remote-state
field requirements.

### What remained only declared

The host-side required status check, branch protection and external ruleset
remain `NOT_PROVEN`. Local workflow text and local tests cannot establish
that external fact.

## Structured assertions

Each assertion uses one of `OBSERVED`, `REPORTED` or `INFERRED`.

| assertion_id | type | subject | predicate | value | source_reference | confidence | limitations |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VERO-061-001 | OBSERVED | repository | HEAD before mission | `d0f400eb89bc21a867a1c124136575a3436f593b` | mission preflight log | high | local repository only |
| VERO-061-002 | OBSERVED | red reproduction | commit exists | `a4a9fb9fc8ee166fcac24b9c3bb3371d186da8de` | Git object and execution journal | high | reproduces audited V2 path |
| VERO-061-003 | OBSERVED | V2.1 implementation | executable basis | `16cf06b9262bdef0b0e2a14baa7b351a33b639ba` | Git commit and Level B receipt | high | no host-side proof |
| VERO-061-004 | OBSERVED | Level A | result | `7266 passed, 6 skipped, 6 warnings` | Level A receipt | high | process CPU unavailable |
| VERO-061-005 | OBSERVED | Level B | result | `122 passed, 0 failed, 5 warnings` | Level B receipt | high | focused final cohort |
| VERO-061-006 | OBSERVED | CI workflow | required job identity | `closure-policy-and-anti-weakening` | `.github/workflows/ci.yml` and CI contract test | high | local text does not prove hosting ruleset |
| VERO-061-007 | REPORTED | Macro 06 V2 | scope fields fully enforced | false in audited behavior | attached prompt section 3.2 | high | predecessor audit input |
| VERO-061-008 | REPORTED | Macro 06 V2 | protected diff computed | false in audited behavior | attached prompt section 3.2 | high | predecessor audit input |
| VERO-061-009 | REPORTED | Macro 06 V2 | CI check is a real job | false in audited behavior | attached prompt section 3.3 | high | predecessor audit input |
| VERO-061-010 | INFERRED | uncomputed policy field | false assurance risk | possible | FIRE-061-001 | medium | impact is a bounded risk inference |
| VERO-061-011 | OBSERVED | remote enforcement | state | `NOT_PROVEN` | policy and final envelope | high | operator must verify host |
| VERO-061-012 | INFERRED | recurrence | probability after V2.1 | reduced but non-zero | negative corpus and boundary | medium | no production runtime exercise |

For every assertion, `effective_at` is the relevant commit or run time,
`observed_at` and `recorded_at` are the execution clocks in the canonical
evidence, `scope` is local repository closure, `supersedes` is empty unless a
later receipt replaces an earlier draft, and limitations remain local-only
unless an external operator supplies evidence.

## Unknowns

The host provider, actual ruleset ID, actual required-check configuration,
host run reference and branch-protection bypass state remain unknown. VERO
does not fill these fields with narrative or local substitutes.
