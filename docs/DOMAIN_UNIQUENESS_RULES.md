# Reglas de unicidad de dominios

IA_CORE no permite dominios duplicados o funcionalmente equivalentes. Un dominio no es solo una carpeta: representa un contexto operativo con perfiles, agentes, presets, papers, datos y trazabilidad.

## Que se considera duplicado

Dos dominios son equivalentes si coinciden por alguno de estos criterios:

- mismo `domain_id` normalizado;
- mismo slug normalizado;
- mismo nombre visible normalizado;
- aliases equivalentes;
- misma area profesional y mismo nicho;
- mismo concepto funcional, aunque cambien acentos, guiones, mayusculas o sufijos cosmeticos;
- variantes como `Loteria`, `Loteria / IA_CORE` y `Loteria - Analisis de Juegos de Azar`.

## Normalizacion

La normalizacion elimina acentos, baja a minusculas, separa signos/guiones y descarta conectores o tokens cosmeticos como `IA_CORE` cuando no representan un dominio real distinto.

La regla vive en `core/domain_identity.py` y se aplica desde `core/domain_registry.create_domain()`.

## Dominios archivados y legacy

La validacion compara contra:

- dominios activos;
- dominios internos o legacy presentes en `domains/`;
- snapshots archivados en `docs/legacy/domains/`.

Un dominio archivado no habilita crear silenciosamente otro igual. El flujo futuro debe pedir una accion explicita: restaurar, resetear, eliminar desde admin o crear una version con alcance realmente distinto.

## Error esperado

`Ya existe un dominio equivalente. No se pueden crear dominios duplicados. Revisa el dominio existente o usa otro nombre/nicho.`

## UI futura

El formulario de Dominio debe mostrar este error y ofrecer caminos claros: usar existente, restaurar archivado, resetear o elegir otro nicho/nombre.

## Deuda futura

Falta un panel admin de dominios con estados y acciones explicitas:

- ver estado;
- archivar;
- eliminar;
- resetear;
- restaurar;
- regenerar desde framework;
- ver dependencias.
