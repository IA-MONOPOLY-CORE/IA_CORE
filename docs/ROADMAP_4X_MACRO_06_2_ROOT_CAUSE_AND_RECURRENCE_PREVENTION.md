# Macro-Mission 06.2 Root Cause And Recurrence Prevention

## Root causes carried from V2.1

1. A path-set subtraction could miss a same-path content change that existed
   before and after the validation basis.
2. Remote `PROVEN` was modeled as local metadata rather than provider-derived
   evidence.
3. Level B chronology selected the last successful run but did not express
   terminal uniqueness for the final basis.

## V2.2 controls

The successor computes the direct committed range from `validation_basis` to
`HEAD` and separately inspects index, worktree and untracked surfaces. It
records status and rename source/destination paths, so no single Git view is
treated as authority.

Remote proof is an evolvable state. `PROVEN` requires five non-empty
provider-originated fields plus resolved proof and observed commits. Local
policy, workflow text and self-authored declarations cannot elevate the
state.

Terminality is explicit. A final basis must have one and only one successful
terminal Level B. Any ordinary validation after that interval fails the
evidence, and any executable/configuration/test mutation after the terminal
run requires a new basis and a new terminal run.

Receipts bind commands to durable logs and recompute both artifact hashes and
their own canonical hash. Deterministic reports exclude volatile fields and
are rendered twice from identical inputs.

## Recurrence boundary

These controls apply only to closure-method infrastructure. They do not imply
that product, backend, runtime, provider, tenant, VERO, FIRE or
Organizational Reconstruction capabilities are implemented.
