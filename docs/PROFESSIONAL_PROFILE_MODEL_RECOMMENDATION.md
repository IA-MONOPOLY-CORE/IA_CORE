# Recomendacion Provider/Model Por Perfil Profesional

Prompt 20 agrega una primera capa de recomendacion provider/model para los 106 perfiles profesionales globales.

## Resumen Ejecutivo

Cada perfil profesional global ya declaraba `default_model_policy`. Prompt 20 formaliza esas policies en `catalogs/profile_model_policies.json` y agrega `core/professional_model_recommendation.py` para convertir la policy, la carga cognitiva, el estilo de razonamiento, la privacidad y el hardware disponible en una recomendacion estructurada.

La recomendacion no crea agentes, presets ni papers. Es una capa previa, testeable y extensible.

## Policies Disponibles

- `local_light`
- `local_standard`
- `local_heavy`
- `cloud_reasoning`
- `cloud_low_latency`
- `hybrid`
- `privacy_sensitive`
- `long_context`
- `multimodal`
- `batch_analysis`
- `cost_sensitive`
- `high_reliability`
- `fast_iteration`
- `offline_capable`
- `human_review_required`

Cada policy define uso, ejecucion preferida, carga cognitiva, latencia, costo, privacidad, contexto, confiabilidad, revision humana, viabilidad local, recomendacion cloud, fallback y tier de provider recomendado.

## Reglas Por Policy

- `local_light`: prioriza `ollama` + `phi3:mini`.
- `local_standard`: prioriza `ollama` + `llama3.2:3b`.
- `local_heavy`: usa local pesado si el hardware alcanza; con hardware limited cae a `nvidia`.
- `cloud_reasoning`: recomienda `nvidia` + modelo de razonamiento amplio.
- `cloud_low_latency`: recomienda `nvidia` + modelo rapido.
- `hybrid`: local si el hardware acompana; cloud si el hardware es limitado.
- `privacy_sensitive`: prioriza local y marca sensibilidad de privacidad.
- `long_context`: recomienda modelo cloud con contexto largo.
- `multimodal`: queda preparado para modelo cloud multimodal.
- `batch_analysis`: local heavy o cloud segun hardware.
- `cost_sensitive`: prioriza local liviano.
- `high_reliability`: recomienda provider/model estable y marca revision humana.
- `fast_iteration`: prioriza local liviano rapido y barato.
- `offline_capable`: prioriza local liviano.
- `human_review_required`: marca siempre `requires_human_review=true`.

## Ejemplos

- `estratega_negocio_digital` usa `cloud_reasoning`: recomienda `nvidia` + `meta/llama-3.3-70b-instruct`.
- `auditor_privacidad_datos` usa `privacy_sensitive`: recomienda `ollama` + `llama3.2:3b` y marca privacidad/revision.
- `especialista_bi_dashboards` usa `local_heavy`: con hardware limitado recomienda cloud; con hardware high-end puede usar local.
- `especialista_base_conocimiento` usa `long_context`: recomienda `nvidia` + `meta/llama-4-maverick-17b-128e-instruct`.

## Integracion Hardware-Aware

La capa reutiliza `core.model_recommendation.HardwareProfile`, `get_default_hardware_profile` y `evaluate_model_compatibility`.

En el hardware actual del proyecto (`local_mode=limited`, sin GPU), las policies pesadas pueden recomendar cloud o fallback local liviano. No se implementa deteccion cross-platform nueva en este prompt.

## Fallbacks

Cada policy tiene `fallback_policy`. La recomendacion devuelve tambien `fallback_provider` y `fallback_model`.

Patron inicial:

- Local liviano/estandar: fallback cloud rapido.
- Cloud reasoning/long context/high reliability: fallback local estandar.
- Privacy/human review: fallback local estandar.
- Local heavy/batch: fallback segun hardware.

## Revision Humana

`human_review_required`, `privacy_sensitive` y `high_reliability` pueden activar `requires_human_review=true`. Esto evita convertir decisiones sensibles en automatizacion ciega.

## Privacidad

`privacy_sensitive` prioriza local y marca `privacy_sensitive=true`. Si en el futuro se usa cloud para datos sensibles, debe existir criterio explicito de proveedor, contrato, anonimizado o aprobacion humana.

## Costo

`cost_sensitive`, `fast_iteration` y `local_light` priorizan ejecucion local o modelos livianos.

## Latencia

`cloud_low_latency` y `fast_iteration` priorizan modelos rapidos. La capa no mide latencia real todavia.

## Deudas Futuras

- Detectar hardware real cross-platform con mayor precision.
- Consultar providers saludables reales antes de ejecutar.
- Conectar la recomendacion con UI/admin cuando existan presets.
- Exportar recomendaciones por matriz o por dominio.
- Ajustar modelos exactos cuando cambie la disponibilidad de providers.
- Validar multimodal con flujos reales.

## Proxima Fase

Prompt 21 deberia preparar la generacion de presets o la capa que consume estas recomendaciones sin crear agentes prematuramente.

## Nota Prompt 21

Prompt 21 usa la recomendacion provider/model dentro de cada `profile_catalog` derivado. Cada candidato generado por `core/professional_profile_catalog_generator.py` incluye `model_recommendation` con provider/model primario, fallback, privacidad, revision humana, compatibilidad y nota de hardware.

## Nota Prompt 22

Prompt 22 incrusta `model_recommendation` en presets derivados. Cada preset conserva provider/model recomendado, fallback, privacidad y revision humana para que la fase de agentes no pierda la decision hardware-aware tomada desde el perfil profesional.
