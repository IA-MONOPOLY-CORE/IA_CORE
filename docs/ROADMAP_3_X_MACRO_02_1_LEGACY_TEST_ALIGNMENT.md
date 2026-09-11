# Roadmap 3.x Macro-Mission 02.1 Legacy Test Alignment

## Disposition

| Legacy surface | Decision | Evidence and boundary |
|---|---|---|
| Root `test_debate.py` | `ALIGN_WITH_CURRENT_CONTRACT` plus explicit integration isolation | The obsolete `supervisor` import was replaced by the existing canonical `core.supervisor.Supervisor`. Importing the module still does not run the probe; direct execution requires `IA_CORE_ALLOW_EXTERNAL_TESTS=1`. The maintained unit coverage remains `tests/test_debate.py`. No fake runtime was introduced. |
| Root `test_respuesta.py` | `ISOLATE_AS_EXPLICIT_LEGACY_TEST` | The old top-level NVIDIA call is now a marked test body gated by explicit `IA_CORE_ALLOW_EXTERNAL_TESTS=1`; credentials are read only inside that gated body. Default collection and execution are safe and produce an explicit skip. |
| `tests/test_api_admin_panels.py::test_hud_active_identity_is_ia_core_without_legacy_product_branding` | `ALIGN_WITH_CURRENT_CONTRACT` | The current HUD identity is `IA_CORE` with the active subtitle `PANEL MAESTRO / DOCUMENTARY CONSOLE`; the old `CONTRACT-AWARE FRAMEWORK CONSOLE` assertion described an earlier surface. Legacy-brand exclusions and current identity checks remain. |
| `tests/test_api_admin_panels.py::test_provider_panel_has_single_flight_loading_and_visible_error_state` | `ALIGN_WITH_CURRENT_CONTRACT` | The current provider flow declares `providersLoadPromise`, loading/error/retry states, and loads from the provider section selection. The former same-line settings onclick lookup was an obsolete implementation detail; the behavior assertions remain at the current contract points. |

## Exclusion policy

No test is silently skipped. External probes are identifiable through the
`external` marker and the `IA_CORE_ALLOW_EXTERNAL_TESTS=1` opt-in. The default
suite keeps the root network guard active. The current UI was not changed to
make an historical assertion pass; only the historical assertions were aligned
with verified current source evidence.

## Evidence commands

- `python -m pytest --collect-only -q test_debate.py test_respuesta.py`
- `python -m pytest -q test_respuesta.py tests/test_ollama_integration.py`
- `python -m pytest -q tests/test_api_admin_panels.py`

The first command must collect without errors, the second must report explicit
default skips, and the third must validate the current HTML/admin contract.
