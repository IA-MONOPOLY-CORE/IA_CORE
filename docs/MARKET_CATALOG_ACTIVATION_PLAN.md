# Market Catalog Activation Plan

## 1. Estado Actual

`Market Catalog / Catálogo de Mercados` queda en estado `planned_not_active`.

No hay activacion automatica. No hay ejecucion comercial automatica. No hay generacion operativa de negocio en esta fase.

## 2. Fases Futuras

Fase futura 1:

Auditar catalogo y schema.

Fase futura 2:

Crear scoring de mercado.

Fase futura 3:

Mapear rubros externos contra areas internas.

Fase futura 4:

Mapear rubros externos contra nichos internos.

Fase futura 5:

Sugerir perfiles/especializaciones compatibles.

Fase futura 6:

Sugerir presets compatibles.

Fase futura 7:

Crear Business Composition Layer.

Fase futura 8:

Generar unidades de negocio candidatas.

Fase futura 9:

Validar ofertas y readiness comercial.

Fase futura 10:

Conectar con UI/API solamente cuando backend lo permita.

## 3. Boundaries De Activacion

- No activar runtime desde el catalogo.
- No convertir rubros externos en nichos internos activos.
- No modificar perfiles, especializaciones ni presets.
- No crear unidades de negocio automaticamente.
- No crear ofertas automaticamente.
- No habilitar UI/API antes de una auditoria de frontera.
- No habilitar scheduler/worker, modelos/tools/memoria ni external access.

## 4. Criterio Para Fase Futura

Una fase futura podra avanzar solo si define contrato, scoring, mappings, tests E2E, boundaries y rollback documental antes de cualquier activacion operativa.
