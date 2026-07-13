# Biblioteca De Arquetipos De Agente

## Que es

La biblioteca de arquetipos de agente vive en `catalogs/agent_archetypes.json`. Es patrimonio compartido de IA_CORE y contiene perfiles psicologicos/metodologicos reutilizables por multiples dominios.

Un arquetipo no es un agente real, no es un preset real por dominio y no es un paper. Es una base adaptable para que una fase futura genere system prompts, presets y papers con contexto de dominio.

## Perfil profesional global vs arquetipo psicologico

Un perfil profesional global describe una funcion de negocio reutilizable: marketing, datos, operaciones, finanzas, soporte, legal o sectores. Un arquetipo psicologico describe una forma de pensar y operar: auditar, integrar, explorar, simular, archivar, refutar o detectar sesgos.

Los perfiles profesionales responden a "que trabajo hace". Los arquetipos responden a "con que enfoque cognitivo lo hace".

## Por que dejaron de ser exclusivos de Loteria

Los nombres historicos nacieron en Loteria, pero sus patrones utiles no pertenecen a ese dominio. Auditor hostil, simulador, integrador, archivista, detector de anomalias o analista de sesgos pueden aplicarse a ventas, operaciones, datos, producto, compliance, investigacion y otros nichos.

Por eso los prompts legacy quedan archivados como baseline historico, mientras los arquetipos nuevos usan templates activos neutrales de IA_CORE.

## Arquetipos incluidos

1. `estadistico_integral`
2. `intuitivo_obsesivo`
3. `persistente_metodico`
4. `arquitecto_sistemas`
5. `competidor_estrategico`
6. `mistico_simbolico`
7. `hipercontrolado`
8. `visionario_matematico`
9. `auditor_hostil`
10. `archivista`
11. `destructor`
12. `minimalista_senal`
13. `cazador_anomalias`
14. `psicologia_masas`
15. `intuitivo_caotico`
16. `antisistema`
17. `apostador_profesional`
18. `jugador_obsesivo`
19. `analista_sesgos`
20. `esceptico_radical`
21. `simulador`
22. `detector_patrones`
23. `observador_conductual`
24. `gestor_bankroll`
25. `experimentalista`
26. `analista_temporal`
27. `historiador`
28. `geometra`
29. `integrador_central`

## Como se usan en otros dominios

Una futura materializacion podra seleccionar un arquetipo y combinarlo con dominio, area, nicho, escala, objetivo, herramientas y paper seed. El resultado esperado sera un system prompt por defecto editable, un preset candidato y un paper seed candidato.

## Que contiene cada arquetipo

Cada entrada declara `role_id`, `specialization_id`, `system_prompt_template`, `preset_seed_template`, `paper_seed_template`, `tools_expected`, capacidades, limites, metodologia, salidas esperadas, compatibilidad por tipos de dominio y tags de nicho, `model_policy`, sensibilidad, prompt historico y baseline legacy cuando existe.

## Historical prompt

`historical_prompt` preserva el material historico disponible. Si el prompt completo no existe en el repositorio, el campo lo declara explicitamente en vez de inventarlo.

## Legacy system prompt baseline

`legacy_system_prompt_baseline` guarda el system prompt manual actual cuando existia. Su estado es `archived_non_operational` y puede contener referencias viejas solo como archivo historico.

## System prompt template adaptable

`system_prompt_template` es la instruccion activa y reusable. Acepta variables como `{domain_name}`, `{area_name}`, `{niche_name}`, `{business_scale}`, `{objective}`, `{paper_seed}` y `{tools_available}`.

Los templates activos usan IA_CORE como identidad. No usan la identidad vieja como sistema activo.

## Preset seed template

`preset_seed_template` prepara el futuro preset real por dominio: objetivo, instrucciones base, capacidades, limites, output esperado, herramientas y policy de modelo.

## Paper seed template

`paper_seed_template` define que memoria/paper necesitara el agente cuando se materialice: objetivo, alcance, contexto, metodologia, herramientas, criterios, limites, riesgos, formato, memoria historica, ejemplos y criterios de actualizacion.

## Tools expected

`tools_expected` enumera herramientas esperadas para futura UI/backend. No instala herramientas, no ejecuta integraciones y no crea agentes.

## Role + specialization

Cada arquetipo usa roles y especializaciones existentes de los catalogos globales. No se crearon roles ni especializaciones nuevas en RESET 01.

## Model policy

Cada arquetipo usa una `model_policy` existente en `catalogs/profile_model_policies.json`.

## Que no hace todavia

- No crea agentes reales.
- No crea papers reales.
- No crea presets reales por dominio.
- No escribe equipos.
- No toca HUD.
- No integra n8n.

## Relacion con futura materializacion

La siguiente fase deberia tomar un arquetipo, combinarlo con perfil profesional y dominio, generar una propuesta revisable y pedir aprobacion humana antes de escribir cualquier archivo operativo.

## Comparar prompt nuevo vs baseline viejo

El usuario podra comparar:

- template nuevo activo: `catalogs/agent_archetypes.json`;
- baseline viejo: `docs/legacy/loteria/legacy_system_prompts_baseline.json`.

Esa comparacion permite recrear agentes desde cero sin perder la memoria historica.

## Deudas futuras

- Definir generador de system prompt por defecto desde arquetipo + perfil profesional.
- Definir UI/backend para elegir arquetipo al crear agente.
- Crear materializacion controlada con rollback.
- Clasificar referencias antiguas de identidad en UI y modulos legacy de Loteria.
