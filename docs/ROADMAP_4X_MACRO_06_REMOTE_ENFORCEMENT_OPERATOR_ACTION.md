# Macro 06 - Remote Enforcement Operator Action

## State

```text
REMOTE_ENFORCEMENT: NOT_PROVEN
OPERATOR_ACTION_REQUIRED: YES
```

The repository proves a repo-local policy validation and anti-weakening test
step in `.github/workflows/ci.yml`. It does not prove that a remote host
requires that check before merge or direct publication. The distinction is
intentional.

## Minimal external action

On the hosting platform, an operator with repository administration authority
must configure a protected `main` branch or equivalent ruleset that requires
the exact check name `closure-policy-and-anti-weakening`, prohibits force push,
requires the expected review policy, and prevents bypass by ordinary writers.
Then the operator must provide an externally verifiable ruleset reference and
one observed protected-branch result to the next mission.

Until that evidence exists, reports must continue to state `NOT_PROVEN`; no
agent narrative may claim that the repository gate is externally inescapable.
