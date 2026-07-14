# Notas admin de limpieza de dominios

## Dominio vacio vs dominio activo

Un dominio vacio puede tener `domain.json` pero no tener perfiles, presets, agentes ni papers. Eso no lo vuelve operativo. Para aparecer como activo debe tener estado claro y no ser equivalente a otro dominio existente o archivado.

## Legacy vs materializado

Un dominio legacy conserva historia o compatibilidad tecnica. Un dominio materializado tiene perfil profesional, presets revisados, agentes/papers operativos y trazabilidad actual.

## Por que se limpio Loteria

Loteria existia en dos formas:

- dominio viejo historico: `loteria`, visible como "Loteria / IA_CORE";
- dominio nuevo creado desde UI: `loteria_analisis_de_juegos_de_azar`, visible como "Loteria - Analisis de Juegos de Azar";
- dominio futuro materializado: aun no existe y debe recrearse desde el framework nuevo.

El viejo era historico. El nuevo estaba parcial. Dejarlos visibles generaba la falsa idea de que habia dos dominios operativos distintos.

## Eliminar, archivar, resetear

- Eliminar: sacar del flujo operativo cuando no debe existir como dominio activo.
- Archivar: conservar evidencia, snapshots e inventario.
- Resetear: limpiar contenido operativo para preparar una recreacion controlada.
- Restaurar: recuperar un dominio archivado hacia un estado materializado o revisable, sin activarlo automaticamente.

En backend interno, estas acciones viven en `core/domain_state.py`:

- `archive_domain()` retira del flujo activo sin borrar informacion.
- `restore_domain()` recupera de forma controlada, pero no marca `active`.
- `reset_domain()` vuelve a `empty` conservando manifest y trazabilidad.
- `delete_domain_safely()` es destructiva, exige confirmacion, dominio `archived` y rechaza `legacy`.

Loteria no debe quedar como excepcion: si vuelve, debe hacerlo con estado, perfiles y trazabilidad nuevos.

## Recomendacion futura

El panel admin deberia permitir ver dependencias, estado, origen, fecha, perfiles, presets, agentes, papers y acciones disponibles antes de eliminar o restaurar un dominio.
