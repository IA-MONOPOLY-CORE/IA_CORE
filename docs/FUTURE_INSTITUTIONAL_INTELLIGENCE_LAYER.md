# IA_CORE - Capa futura de inteligencia institucional

Estado: futuro; estratégico; no implementado; pendiente de implementación;
sin runtime; sin execution; sin endpoints; sin integraciones reales;
sin conectores reales; sin credenciales.

## Definición y propósito

IA_CORE debe desarrollar una capa futura de inteligencia institucional: la
capacidad de aprender de empresas reales, detectar patrones organizacionales,
entender qué estructuras funcionan, anticipar problemas, recomendar mejoras y
convertir experiencia operativa acumulada en criterio empresarial propio.

Esta definición pertenece a una visión futura y no implementada. No crea
aprendizaje, memoria global, análisis entre clientes, recomendaciones, modelos,
agentes, paneles ni ejecución. Forma parte del
[índice estratégico](FUTURE_PLATFORM_EXTENSION_INDEX.md) y se relaciona con la
[taxonomía corporativa futura](FUTURE_CORPORATE_AREAS_AND_SUBAREAS_MODEL.md).

## Diferencia con Adaptive Business Intelligence

- Adaptive Business Intelligence adapta análisis, reportes y recomendaciones al contexto de un negocio específico.
- Institutional Intelligence Layer acumularía criterio organizacional y empresarial a partir de patrones, estructuras, decisiones, errores, resultados y evidencia de múltiples operaciones reales, siempre bajo privacidad, permisos, contratos, anonimización y aislamiento tenant.

La adaptación contextual por negocio debería permanecer aislada y trazable. El
aprendizaje institucional futuro gobernado y anonimizado requeriría un contrato
separado, finalidad explícita, controles de reidentificación y revisión humana.
Ninguna de las dos categorías implica una capacidad presente.

## Fuentes conceptuales de aprendizaje futuro

La capa podría aprender en el futuro, dentro de límites autorizados, de:

- áreas activadas;
- subáreas usadas;
- paneles visibles u ocultos;
- roles humanos;
- responsables;
- colaboradores;
- agentes;
- equipos;
- workflows;
- decisiones;
- resultados;
- errores;
- cuellos de botella;
- costos;
- riesgos;
- tiempos de respuesta;
- estructura comercial;
- estructura operativa;
- rentabilidad;
- reclamos;
- campañas;
- ventas;
- datos regionales;
- datos culturales;
- economía local;
- jurisdicción;
- sector/rubro;
- tamaño de empresa.

Cada fuente futura debería tener procedencia, finalidad, alcance, vigencia,
calidad, permiso y política de retención. La disponibilidad técnica de un dato
no debería convertirlo en dato autorizado para aprendizaje.

## Capacidades futuras posibles

Siempre como hipótesis no implementadas, esta capa podría:

- detectar estructuras débiles;
- sugerir áreas o subáreas faltantes;
- recomendar cuándo una subárea merece panel propio;
- advertir exceso de complejidad visible;
- advertir falta de control;
- anticipar riesgos organizacionales;
- identificar cuellos de botella;
- recomendar reasignación de responsabilidades;
- sugerir modelos, agentes o presets adecuados;
- sugerir mejoras de procesos;
- comparar patrones internos anonimizados;
- mejorar onboarding;
- mejorar manuales;
- mejorar ventas, operaciones y soporte según evidencia;
- ayudar al `owner` a entender qué tipo de estructura necesita cada cliente.

Estas posibilidades no autorizan cambios automáticos de estructura, permisos,
responsables, procesos, modelos, agentes, precios, contratos o políticas.

## Gobierno, privacidad y límites estrictos

- No usar datos crudos de un cliente para otro.
- No mezclar tenants.
- No exponer información privada.
- No vender datos de clientes.
- No aprender transversalmente sin contrato, consentimiento, anonimización y controles.
- No convertir correlaciones en verdades absolutas.
- No tomar decisiones sensibles sin humano autorizado.
- No prometer resultados garantizados.
- No presentar esta capa como capacidad existente o implementada.
- Toda recomendación debe estar basada en evidencia, métricas, trazabilidad o límites explícitos.
- Los permisos no deben inferirse de patrones de uso ni ampliarse por aprendizaje.
- El aislamiento tenant debe preservarse en datos, contexto, memoria, modelos derivados, evaluación y evidencia.
- La anonimización debe considerar el riesgo de reidentificación y no limitarse a retirar nombres.
- Los contratos deben definir finalidad, alcance, retención, revocación, auditoría y responsabilidades.

La inteligencia institucional no reemplaza al dueño, al gerente ni al profesional
humano. Debe funcionar como una capa de criterio acumulado que ayuda a detectar
patrones, ordenar empresas, prevenir errores y recomendar mejoras bajo gobierno
humano.

## Evidencia, incertidumbre y revisión

Una eventual recomendación debería identificar fuentes permitidas, muestra,
contexto, fecha, supuestos, métricas, incertidumbre, alternativas y responsable
de revisión. Una correlación no demuestra causalidad; un patrón frecuente no
define una regla universal; una estructura útil en un rubro o jurisdicción puede
ser inadecuada en otro contexto.

Las comparaciones futuras deberían usar agregación y controles que reduzcan el
riesgo de exposición o reidentificación. El cliente debería conservar los
derechos y controles definidos por contrato sobre sus datos y su participación.
Las decisiones sensibles deberían permanecer bajo autoridad humana verificable.

## Límites documentales

Este documento no implementa motores de aprendizaje, entrenamiento, memoria,
stores, modelos, agentes, workers, schedulers, queues, event bus, dispatchers,
endpoints, integraciones, credenciales, paneles ni acciones externas. Tampoco
modifica UI activa, backend operativo ni `backend_internal_ui_payload.v1`.
