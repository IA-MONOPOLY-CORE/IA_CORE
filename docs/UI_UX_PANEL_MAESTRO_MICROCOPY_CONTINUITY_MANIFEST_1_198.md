# UI/UX 1.198 - Microcopy continuity manifest

## Gate

`N1_MICROCOPY_CONTINUITY_MANIFEST_PASSED`

This is a test-only and documentation-only continuity boundary. It freezes the
active microcopy sources at baseline `6b9c806` without changing a word in the
product. The machine-readable implementation is
`tests/ui_ux_panel_maestro_microcopy_1_198_support.py`.

## Exact baseline

| Field | Value |
| --- | --- |
| Baseline commit | `6b9c806` |
| Branch at start | `main` |
| Product payload | `backend_internal_ui_payload.v1` |
| Payload v2 | Absent and prohibited |
| Scope | Inventory, classification, mapping, geometry and decision evidence |
| First wording decision | N7, outside this prompt |

The guard compares every protected product path byte-for-byte with the
baseline commit. This is intentionally stricter than a text-only comparison:
it also catches accidental HTML, CSS, JavaScript, i18n, backend and payload
drift.

## Registered source corpus

The registry is exact. It does not accept globs, recursive discovery or an
unregistered path.

### Active microcopy sources

- `ui/web/index.html` - direct text and accessible attributes.
- `ui/web/i18n_es.json` - flattened string leaves and exact keys.
- `ui/web/backend-contract-widgets.js` - potentially renderable widget strings.
- `ui/web/admin-panels.js` - potentially renderable administrative strings.
- `ui/web/console-interactions.js` - request-draft and interaction strings.
- `ui/web/domains.js` - domain form and catalog strings.

### Protected product paths

The active registry is a subset of the full protected set. The full set also
includes `ui/web/styles.css`, `core/backend_internal_ui_payloads.py` and
`api.py`, because those files define visual and contractual boundaries even
when they are not microcopy sources.

No source is classified by proximity alone. The later N3 and N4 artifacts must
provide the semantic classification and the surface/contract evidence.

## Source roles frozen for N1

| Role | Meaning in this manifest |
| --- | --- |
| `ACTIVE_COPY_SOURCE` | A registered product source that can expose current text. |
| `CONTRACT_COPY_SOURCE` | Text tied to declared contract vocabulary or a contract-aware surface. |
| `EDITORIAL_COPY_SOURCE` | General UI or administrative wording with no demonstrated contract binding. |
| `STATE_LABEL_SOURCE` | Status, readiness, blocker or boundary labels. |
| `WARNING_SOURCE` | Warning or diagnostic wording. |
| `ERROR_SOURCE` | Error or failed-state wording. |
| `FALLBACK_SOURCE` | `no_payload`, `not_available` or other honest fallback wording. |
| `ACTION_LIKE_COPY_SOURCE` | Wording that resembles an action and requires N3 risk review. |
| `PERMISSION_LIKE_COPY_SOURCE` | Wording that might imply authority or permission and cannot be changed autonomously. |
| `READINESS_COPY_SOURCE` | Readiness or validation wording that must not be equated with execution. |
| `UNKNOWN_REQUIRES_CLASSIFICATION` | Any item whose meaning is not derivable from source evidence. |

N1 records roles and boundaries. It does not settle semantic ambiguity; that is
the purpose of N3 and, where necessary, Direction.

## Deterministic materialization

The helper emits stable `MICROCOPY_ID` values by source and source order:

- `HTML_TEXT_NNNN` for direct text nodes;
- `HTML_ATTR_NNNN` for `aria-label`, `title`, `placeholder` and `alt`;
- `I18N_NNNN_<key>` for flattened i18n values;
- `JS_<SOURCE>_<LINE>_<ORDINAL>` for filtered potentially renderable literals.

Each emitted item carries exact text, source, file, location, surface,
visibility, language, initial type, contract-awareness, active/legacy flags,
duplicate signal and preliminary geometry/semantic risk. The corpus digest is
computed from the complete ordered record, not from a lossy deduplicated set.

## Negative guarantees

The N1 focal test rejects:

- an unknown corpus source;
- an unregistered source path;
- an unknown or malformed i18n key;
- wildcard/glob source registration;
- any protected product-file change relative to `6b9c806`;
- a change in active wording, because it changes a protected product file.

## Gate and commit classification

`N1_MICROCOPY_CONTINUITY_MANIFEST_PASSED` is valid when the exact registry,
baseline, digest materialization and negative guarantees pass. The diff is
test infrastructure plus evidence, so the honest commit prefix is `test(ui)`
for this station. No product commit is permitted.
