# Long Test Suite Validation Policy

## 1. Estado

`LONG_TEST_SUITE_VALIDATION_POLICY_READY`

## 2. Motivo

La suite filtrada de IA_CORE ya supera los 2800 tests. En entornos de runner, IDE agent o consola con timeout operativo, una corrida monolitica puede cortar por tiempo aunque los tests no fallen.

Esta politica evita confundir un timeout operativo del runner con un fallo de tests, y define una validacion equivalente por bloques para suites largas.

## 3. Politica Principal

La suite monolitica filtrada sigue siendo la validacion preferida cuando el entorno la permite.

Frase normativa exacta:

```txt
La suite monolítica filtrada sigue siendo la validación preferida
```

Comando monolitico preferido:

```bash
python -m pytest tests/ -q -k "not test_ollama_integration and not sandbox_chain_full_benchmark"
```

## 4. Politica Alternativa Aceptada

Cuando la suite monolitica se corta por timeout operativo sin fallo visible, se permite validacion equivalente por bloques.

Frase normativa exacta:

```txt
timeout operativo sin fallo visible
validación equivalente por bloques
```

Esta alternativa no degrada el criterio de aceptacion: todos los bloques deben pasar y deben cubrir el mismo universo filtrado relevante.

## 5. Condiciones Obligatorias Para Aceptar Bloques

- El timeout debe ser operativo, no un fallo de test.
- No debe haber fallo visible antes del timeout.
- Los bloques deben cubrir el mismo universo filtrado relevante.
- Todos los bloques deben pasar.
- Se debe reportar el total agregado.
- Se debe reportar skipped/deselected si corresponde.
- Se debe ejecutar git diff --check.
- El working tree final debe quedar limpio.
- El reporte final debe declarar explicitamente que se uso validacion equivalente por bloques.

Resumen obligatorio:

```txt
timeout operativo sin fallo visible
validacion equivalente por bloques
todos los bloques deben pasar
mismo universo filtrado
total agregado
git diff --check
working tree limpio
```

## 6. Segmentacion Inicial Repetible

La segmentacion recomendada para el estado actual del repo es por orden alfabetico de archivos `tests/*.py`, excluyendo los mismos tests que excluye la suite filtrada monolitica.

Esta estrategia es estable porque:

- usa el mismo universo filtrado que el comando monolitico;
- no depende de keywords parciales;
- no duplica archivos entre bloques;
- permite reportar totales agregados.

Bloque 1:

```powershell
$env:PYTHONPATH='C:\IA_CORE\.testdeps'
$files = Get-ChildItem tests -Filter *.py | Sort-Object Name | Where-Object { $_.Name -notin @('test_ollama_integration.py','test_sandbox_chain_full_benchmark.py') } | Select-Object -First 50 -ExpandProperty FullName
python -m pytest @files -q
```

Bloque 2:

```powershell
$env:PYTHONPATH='C:\IA_CORE\.testdeps'
$files = Get-ChildItem tests -Filter *.py | Sort-Object Name | Where-Object { $_.Name -notin @('test_ollama_integration.py','test_sandbox_chain_full_benchmark.py') } | Select-Object -Skip 50 -First 50 -ExpandProperty FullName
python -m pytest @files -q
```

Bloque 3:

```powershell
$env:PYTHONPATH='C:\IA_CORE\.testdeps'
$files = Get-ChildItem tests -Filter *.py | Sort-Object Name | Where-Object { $_.Name -notin @('test_ollama_integration.py','test_sandbox_chain_full_benchmark.py') } | Select-Object -Skip 100 -ExpandProperty FullName
python -m pytest @files -q
```

Si el numero de archivos crece, se puede aumentar la cantidad de bloques manteniendo la misma regla: lista alfabetica filtrada, particiones sin solapamiento y cobertura total.

## 7. Regla Para Proximos Prompts

Para prompts posteriores, la validacion principal puede ser segmentada por bloques cuando la suite monolitica sea propensa a timeout.

La suite monolitica puede intentarse si el tiempo lo permite, pero no debe bloquear el cierre si los bloques equivalentes pasan completos.

El reporte debe declarar si la validacion fue monolitica o por bloques equivalentes.

## 8. Fronteras No Modificadas

Esta politica NO modifica ni activa:

```txt
runtime
stores
lifecycle writes
result store
scheduler
worker
queue
model invocation
tool execution
memory persistence
external access
API
UI
Market Catalog runtime
Business Composition Layer runtime
```

## 9. Proximo Paso

`PROMPT 3.7 - Auditoria de integracion result/history/read model`

Referencia exacta:

```txt
PROMPT 3.7 — Auditoría de integración result/history/read model
```
