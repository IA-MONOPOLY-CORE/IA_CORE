# Roadmap 4.x Macro-Mission 03 - Canonical JSON Census Reconciliation

## Regla adoptada

La métrica vigente es:

`TRACKED_JSON_FILES_PARSEABLE`

El universo se construye exclusivamente con:

```text
git ls-files -- '*.json'
```

Cada path devuelto se lee como UTF-8 y se parsea con el parser JSON de Python.
Un archivo versionado que no pueda parsearse es un bloqueo de la misión. No se
incluyen caches, entornos virtuales, archivos ignorados ni JSON recursivos que
no estén versionados.

## Reconciliación histórica

| Fuente | Conteo observado | Alcance que puede demostrarse | Tratamiento |
| --- | ---: | --- | --- |
| Prompt de Macro 03 | `328` | Declara un conteo histórico, pero no conserva el comando ni el listado | Se preserva como evidencia declarada; no se usa como métrica vigente |
| Evidencia Macro 02 | `248` | El checkpoint dice `PASS: 248 files`; el comando exacto no quedó preservado | Se conserva como fotografía histórica de esa corrida |
| Evidencia Macro 02.1 antes de evidencia documental | `268` | El checkpoint dice `268 files before documentary evidence` | Se conserva como subconjunto de esa corrida |
| Evidencia Macro 02.1 con evidencia documental | `269` | El checkpoint dice `269 files including documentary evidence` | Se conserva como fotografía histórica ampliada |
| Baseline Macro 03 `2969ed4` | `250` | `git ls-tree -r --name-only <baseline>` filtrado a `.json` | Base versionada reproducible |
| Estación 1 Macro 03 | `251` | Baseline más el JSON de cierre P4 de esta misión | Métrica vigente parcial, todos parseables |

La diferencia `328` versus `269` no demuestra pérdida de archivos: los
artefactos no conservan universos equivalentes y uno de los conteos fue
declarado por el operador en el prompt. Tampoco se reescriben esos reportes
históricos para forzar equivalencia. La diferencia `248` versus `268/269` es
compatible con el agregado de evidencia documental y con cambios de alcance,
pero no se afirma una causa no demostrada.

## Censo canónico de Macro 03

- Comando de selección: `git ls-files -- '*.json'`.
- Commit de referencia inicial: `2969ed469ed482968b4db4deac7b35a855f635e2`.
- Conteo versionado en el baseline: `250`.
- Conteo después de la estación 1: `251`.
- Paths fallidos: `0`.
- Encoding requerido: UTF-8.
- Parser: `json.loads` sobre el contenido completo de cada path.
- Resultado: `PASS`.

La validación final de Macro 03 repite el mismo comando después de todos los
commits documentales y registra el conteo final en el checkpoint final. Las
mediciones futuras deben reutilizar esta definición y no mezclarla con un
recorrido recursivo del directorio de trabajo.

`TRACKED_JSON_FILES_PARSEABLE_CANONICAL_RULE_ESTABLISHED`
