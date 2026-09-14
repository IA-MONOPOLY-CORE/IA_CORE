# Roadmap 4.x Macro-Mission 02.1 - Commit Accountability Ledger

## Estado

- Resultado: `ROADMAP_4X_MACRO_02_1_P4_POST_BOUNDARY_E2E_ADVERSARIAL_CHECKPOINT_PASSED_AFTER_EVIDENCE_BOUND_REPAIR`.
- Baseline: `05674020671e98557262e26df8c380da631138b2`.
- Branch: `main`.
- `VALIDATION_BASIS_HEAD`: `d0fe3b789249101b9acf526db47b89ee4d797715`.
- External exposure: `DEFAULT_DENIED`.
- Production readiness: `NOT_AUTHORIZED`.
- Macro-Mission 03: `NOT_STARTED`.
- Publication metadata: stable role references; no self-referential hash chase.

## Commits de la mision

| Orden | Commit | Responsabilidad | Alcance | Resultado |
| ---: | --- | --- | --- | --- |
| 1 | `3c9fce7e3b7b5ee858776abc04c90396f497da3e` | Suite adversarial E2E | nuevo test Macro 02.1 | PASS despues de reparar defectos detectados |
| 2 | `fc3e5952eab6f7ff1f4cdda89fd03990f375920b` | Reparacion de producto contenida | `api.py` P4 y `core/p4_request_access.py` | PASS red -> green |
| 3 | `6ec1b7b362e32da101f37b236de9320542ed5729` | Continuidad historica | reconocer el test exacto en dos guards | PASS, assertions preservadas |
| 4 | `d0fe3b789249101b9acf526db47b89ee4d797715` | Continuidad documental preventiva | reservar cinco paths documentales exactos | PASS, no guard global relajado |
| 5 | `EXTERNAL_REPORT_REFERENCE` | Cierre documental y publicacion | checkpoint, evidencia, matriz, ledger, GOKV, README/index | pendiente de hash externo hasta commit |

Los cuatro commits materiales antes del cierre documental son independientes.
El commit de producto contiene solo la reparacion demostrada por la prueba
roja. Los dos commits de guards agregan paths exactos y no eliminan ni
generalizan aserciones.

## Validacion

- Replay inicial antes de reparar: `7 failed, 12 passed, 6 warnings` en
  `13.23 s`.
- Adversarial + Macro 02 despues de reparar: `37 passed, 6 warnings` en
  `11.80 s`.
- Replays focales Level A: `210 passed, 6 warnings` en `19.71 s`.
- Full suite final de Level A: `7003 passed, 6 skipped, 6 warnings` en
  `1534.39 s` segun pytest (`1538.76 s` instrumentados).
- Level B focal post-closeout: `210 passed, 6 warnings` en `16.84 s`; JSON
  final: `269` archivos validos.
- GOKV: `38` items, valido.
- JSON parse: PASS; Python compile: PASS; Node contractual: PASS.
- CORS contra baseline: PASS, sin cambios.
- Protected diff y `git diff --check`: PASS.

## Cierre y rollback

El rollback productivo es exclusivamente `fc3e5952eab6f7ff1f4cdda89fd03990f375920b`.
No hay rollback de datos porque no se modifico registry ni store productivo.
No hubo red, provider, secreto, hosting, CORS, runtime o execution.

La separacion entre `VALIDATION_BASIS_HEAD`, commit documental y verificacion
post-fetch se mantiene por el protocolo
`publication_metadata_must_not_chase_its_own_head`.
