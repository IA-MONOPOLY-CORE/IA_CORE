# Registro de integraciones futuras

Estado: futuro; estratégico; no implementado; pendiente de implementación;
sin runtime; sin execution; sin endpoints; sin integraciones reales;
sin conectores reales; sin credenciales.

## Propósito y principio

Registrar candidatos y reglas de extensión de la [arquitectura futura](FUTURE_PLATFORM_EXTENSION_INDEX.md).
IA_CORE debe funcionar sin integraciones externas. Las integraciones futuras
son extensiones modulares, no el núcleo del sistema. Como las extensiones de
navegador, ampliarían capacidades sin definir la identidad del producto.
La inclusión en este registro no acredita compatibilidad, licencia disponible,
seguridad evaluada ni conexión existente.

## Habilitación y autoridad futuras

Integración conocida no equivale a activa; integración activa no equivale a acción
libre. Toda acción sensible requeriría contrato, permiso, evidencia, trazabilidad
y aprobación humana cuando corresponda. Ninguna integración se activaría por
defecto para todos los clientes. La habilitación debería configurarse por cliente,
empresa, unidad, sector, usuario, plan, contrato, permisos y configuración.

Los siguientes son estados futuros posibles, no estados actuales del repositorio.
Disponibilidad, licencia, configuración y autorización son dimensiones distintas;
no conforman una escalera que conceda permiso automáticamente.

| Estado | Significado propuesto |
|---|---|
| `future` | Candidato pendiente de evaluación e implementación. |
| `available` | Compatibilidad evaluada en un alcance específico. |
| `licensed` | Derecho de uso acreditado; sin autorización de acción implícita. |
| `enabled` | Seleccionado en el alcance autorizado. |
| `disabled` | Deshabilitado en ese alcance. |
| `configured` | Configuración validada, todavía sujeta a permisos de cada acción. |
| `missing_credentials` | Faltan credenciales autorizadas; operación bloqueada. |
| `blocked` | Restricción contractual, de seguridad o de permisos. |
| `unsupported` | Fuera de compatibilidad para versión, región o caso de uso. |
| `requires_approval` | Acción pendiente de aprobación humana aplicable. |
| `deprecated` | Retiro previsto; requeriría revisión y plan de migración. |

## Catálogo de candidatos

| Categoría futura | Referencias a evaluar | Alcance conceptual |
|---|---|---|
| automation/workflows | n8n | Coordinación de flujos autorizados. |
| persistent/runtime agent candidates | Hermes Agent, OpenClaw | Evaluar persistencia y colaboración bajo contratos. |
| UI/desktop/browser/computer-use candidates | UI-TARS | Interacción autorizada con interfaces. |
| physical/domotic candidates | Home Assistant | Dispositivos y entornos físicos con permisos específicos. |
| communication channels | WhatsApp text, WhatsApp audio, WhatsApp calls, Telegram, Gmail/email | Canales de intención, coordinación y reportes. |
| data/productivity | Google Sheets, Google Docs, Google Drive, Google Calendar | Documentos, datos y calendarios autorizados. |
| business systems | CRM, e-commerce, external APIs, external business systems | Intercambio contractual con sistemas empresariales. |
| finance/payments | banks, payment processors, POS, sistemas tipo Mercado Pago, bank feeds, authorized treasury connectors | Visualización y conciliación; acciones sensibles sujetas a control humano. |
| model/provider layer | OpenAI, Anthropic, Google, Meta/Llama, Mistral, DeepSeek, Qwen, Cohere, Groq, OpenRouter, NVIDIA, Ollama, LM Studio, vLLM, llama.cpp; local/cloud/enterprise providers | Opciones del motor cognitivo base sujetas a evaluación. |

Modelos, proveedores, APIs locales/cloud/híbridos y recomendación de modelo
pertenecen conceptualmente al motor cognitivo base de IA_CORE; no deben tratarse
solamente como add-ons comerciales. Las extensiones externas de canal,
automatización, datos, dispositivos y sistemas de terceros sí podrían empaquetarse
como módulos/add-ons según plan. Aquí no se agregan ni invocan modelos.

Hermes y OpenClaw quedan como candidatos futuros a evaluar. No se decide si son
complementarios, redundantes o excluyentes. La evaluación futura debería comparar
licencias, aislamiento, autoridad, persistencia, privacidad y evidencia, sin
presuponer integración real.

## Voz y canales operativos futuros

WhatsApp y voz podrían canalizar órdenes por texto/audio, aprobaciones rápidas,
reportes, KPIs, escalamiento y comunicación del Director IA_CORE con owner/cliente.
La voz no debería ejecutar acciones sensibles directamente: crearía intención;
IA_CORE debería validar identidad, alcance y contrato; un humano aprobaría cuando
corresponda. Una transcripción o mensaje recibido no constituye autorización.
La futura aprobación debería quedar ligada a una acción concreta y su evidencia.

## Mirrors oficiales y revisión

Los mirrors no deben suplantar plataformas oficiales. Se proponen como capas
autorizadas, trazables y seguras de visualización, preparación, conciliación y
asistencia. Cualquier ejecución permitida en el futuro exigiría integración válida,
permiso explícito, contrato aplicable y confirmación humana cuando corresponda.
Fuentes, vigencia de datos, alcance y resultado deberían ser distinguibles.

La [tesorería y fiscalidad](FUTURE_FINANCIAL_MIRROR_TREASURY_AND_TAX_MODEL.md),
el [acceso organizacional](FUTURE_ORGANIZATIONAL_ACCESS_MODEL.md) y la
[seguridad](FUTURE_SECURITY_AND_IT_OPERATIONS_MODEL.md) definen límites relacionados.
No se conectan ahora bancos, ARCA, WhatsApp, Gmail, Google, n8n, Hermes,
OpenClaw, UI-TARS ni Home Assistant.
