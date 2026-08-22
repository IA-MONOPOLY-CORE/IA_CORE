# IA_CORE GitHub Backup Ready

Fecha local: 2026-08-22 10:03:57 -03:00

HEAD base antes del backup documental: `8d889369`

Repo GitHub objetivo: `https://github.com/IA-MONOPOLY-CORE/IA_CORE`

## Objetivo

Preparar IA_CORE para backup seguro en GitHub antes de continuar con `PROMPT UI/UX 1.22 - Checkpoint Frontend Incongruence IA_CORE contract-aware sin runtime/no-execution`.

Este documento no avanza UI/UX, no desarrolla funcionalidades, no toca runtime, no toca backend operativo, no invoca modelos/tools/integraciones y no habilita execution ni dispatch.

## Checklist De Seguridad

- Working tree inicial: limpio.
- HEAD inicial confirmado: `8d889369`.
- Rama inicial detectada: `master`.
- Remotos iniciales: ninguno.
- `.env` local detectado como ignorado por `.gitignore` y no trackeado.
- Busqueda estricta de secretos: solo falsos positivos en politica/tests de redaccion de secretos; no se encontro clave real trackeada.
- Busqueda por nombres sensibles trackeados: solo documentos/tests/politica de secretos; no se encontro `.env`, llave privada o credencial trackeada.
- Archivos grandes trackeados: mayor archivo `data/market_catalog/market_catalog.generated.json` aprox. 3.47 MB; sin binarios pesados bloqueantes.
- Archivos grandes no trackeados/ignorados: `memory/state.json` aprox. 11.27 MB dentro de ruta ignorada; no se sube.
- No usar `git push --force`.
- Detener push si GitHub rechaza por autenticacion o historial remoto no relacionado.

## Estado .gitignore

`.gitignore` existe y cubre `.env`, caches Python, `venv/`, `.testdeps/`, memoria vectorial, logs, bases locales y estado volatil. En este backup se amplia de forma no destructiva para cubrir `.env.*`, caches adicionales, `node_modules/`, `dist/`, `build/`, archivos temporales, IDE local y backups comprimidos locales.

## Resultado Busqueda Secretos

No se detecto riesgo bloqueante en archivos trackeados. Las coincidencias estrictas aparecieron solo en `core/secrets_policy.py` y tests de politica de secretos, donde se prueban patrones/redaccion con fixtures falsos. No se expone ningun valor sensible en este documento.

El archivo `.env` local existe, esta ignorado, no esta trackeado y no debe subirse a GitHub.

## Resultado Revision Archivos Grandes

Archivos trackeados principales por tamano:

- `data/market_catalog/market_catalog.generated.json` aprox. 3.47 MB.
- `domains/loteria/lotoplus_completo_3511_3885.json` aprox. 0.66 MB.
- `catalogs/niches.json` aprox. 0.28 MB.
- `docs/BACKEND_INTERNAL_BOOK_DESIGN.md` aprox. 0.27 MB.
- `catalogs/professional_profiles.json` aprox. 0.20 MB.

No se detectaron zips/builds/caches trackeados como bloqueo para GitHub. `memory/state.json` es mayor, pero esta ignorado por regla existente.

## Remoto GitHub

Remoto objetivo:

```powershell
git remote add origin https://github.com/IA-MONOPOLY-CORE/IA_CORE
```

Si la rama local se normaliza a `main`, usar:

```powershell
git branch -M main
git push -u origin main
```

Solo usar push normal. No usar force push.

## Restauracion

1. Clonar `https://github.com/IA-MONOPOLY-CORE/IA_CORE`.
2. Leer `README.md` y este documento.
3. Crear entorno Python local si corresponde.
4. Instalar dependencias desde `requirements-api.txt` o `requirements.txt` segun el flujo a retomar.
5. Ejecutar tests principales:

```powershell
node --check ui/web/backend-contract-widgets.js
node --check ui/web/admin-panels.js
node --check ui/web/console-interactions.js
python -m pytest tests/test_api_admin_panels.py -q
python -m pytest tests/test_ui_ux_frontend_incongruence_hardening_1_21.py -q
python -m pytest tests/test_backend_internal_future_ui_contract_plan_8_7.py tests/test_backend_internal_ui_payloads_7_6.py -q
python -m pytest tests/test_ia_core_github_backup_readiness.py -q
```

6. Servir UI con el metodo existente de FastAPI, por ejemplo `python api.py` desde un entorno con dependencias instaladas.
7. Continuar con el prompt pendiente exacto.

## Proximo Prompt Pendiente

`PROMPT UI/UX 1.22 - Checkpoint Frontend Incongruence IA_CORE contract-aware sin runtime/no-execution`