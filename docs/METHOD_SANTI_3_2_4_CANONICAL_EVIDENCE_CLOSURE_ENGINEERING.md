# Method Santi 3.2.4 - Canonical Evidence Closure Engineering

```text
METHOD_SANTI_3_2_4_CANONICAL_EVIDENCE_CLOSURE_ENGINEERING
CANONICAL_EVIDENCE_GATE_V1
IA_CORE_PRODUCT_CAPABILITY: NO
IA_CORE_RUNTIME_COMPONENT: NO
COGNITIVE_KERNEL_FAMILY: NO
COMMERCIAL_FEATURE: NO
```

## Purpose and boundary

Method Santi 3.2.4 is an additive development and evidence method for closing
a repository checkpoint. It governs how claims are reconciled, validated and
published. It does not implement a product capability, activate runtime or
execution, create authority, promote GOKV knowledge, or change an endpoint,
payload, integration or external exposure policy.

Method Santi 3.2.3 remains unchanged and is the predecessor method. This
document adds a canonical-evidence closure layer; it does not replace or
rewrite the verified adaptive execution feedback method.

```text
METHOD_UPDATE_IS_NOT_PRODUCT_CAPABILITY
METHOD_UPDATE_IS_NOT_RUNTIME
METHOD_UPDATE_IS_NOT_AUTHORITY
METHOD_UPDATE_IS_NOT_GOKV_PROMOTION
```

## Canonical evidence gate

Every claim must identify its source class and its validation state. Valid
source classes are repository content, executable test output, Git state,
fetch-verified publication state, or explicit operator evidence. Unknown
external facts remain unknown and are not converted into estimates.

The gate rejects parse failures, duplicate JSON keys, contradictory clocks,
unbounded source claims, unstated working-tree substitutions and evidence that
tries to contain the hash of the commit containing that same evidence.

```text
UNKNOWN_IS_VALID_EVIDENCE
```

Unknown is valid only when it is named, scoped, and paired with the evidence
needed to resolve it. It is not a pass substitute for a required repository or
test gate.

## Four closure anchors

The method keeps these events distinct:

```text
FUNCTIONAL_PUBLICATION_FETCH_VERIFIED_TIME
DOCUMENTARY_CONTENT_FINALIZED_TIME
DOCUMENTARY_LOCK_FETCH_VERIFIED_TIME
OPERATOR_VISIBLE_COMPLETION_TIME
```

Functional publication is the fetch-verified state of the product/test
publication. Documentary content finalization is the point at which the
checkpoint, evidence, metric, ledger and supporting documents are complete.
Documentary lock fetch verification is the remote confirmation of the final
documentary lock commit. Operator-visible completion requires evidence outside
the repository; when unavailable it remains
`UNKNOWN_EXTERNAL_OPERATOR_EVIDENCE_REQUIRED`.

Historical timestamps retain their original meaning. A historical content
timestamp cannot be silently relabeled as a functional publication or
documentary lock timestamp.

## Fixed-point publication

```text
PUBLICATION_METADATA_MUST_NOT_CHASE_ITS_OWN_HEAD
```

Evidence may reference the baseline, validation basis, functional publication
head and the parent of the documentary lock. It must not write the final hash
of the commit that contains its own final content. The live final HEAD and
`origin/main` are reported externally after fetch verification. No follow-up
commit is created merely to insert that hash into the evidence, so the
publication reaches a fixed point.

## Required closure sequence

1. Freeze repository truth and the authorized scope.
2. Execute focal and cross-boundary tests before product repair decisions.
3. Reconcile structured evidence with a duplicate-key-rejecting parser.
4. Run historical impact, Level A and Level B gates.
5. Finalize documentary content without self-reference.
6. Create one documentary lock commit, fetch and verify publication.
7. Report the live final head and operator-visible unknowns separately.

The method preserves exact historical contracts, requires scoped allowlists for
new files, and forbids replacing a historical snapshot with the current
working tree. It is documentation and validation logic only; it does not add
an IA_CORE product capability, runtime component, authority source, GOKV
promotion, cognitive-kernel behavior or commercial feature.
