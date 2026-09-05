# Modelo futuro Financial Mirror, Treasury y fiscalidad

Estado: futuro; estratégico; no implementado; pendiente de implementación;
sin runtime; sin execution; sin endpoints; sin integraciones reales;
sin conectores reales; sin credenciales.

## Propósito y separación

Documentar dos responsabilidades relacionadas pero distintas dentro del
[bloque estratégico](FUTURE_PLATFORM_EXTENSION_INDEX.md). El modelo describe cómo
podría asistirse una operación autorizada futura; no acredita servicios financieros,
facturación, declaraciones ni cumplimiento tributario actuales.

| Modelo futuro | Información y responsabilidad conceptual |
|---|---|
| Financial Mirror / Treasury | Dinero real, bancos, caja, pagos, cobros, flujo, conciliación, movimientos, saldos, alertas y diferencias entre ventas declaradas y dinero recibido. |
| Tax Authority Mirror / Fiscalidad | Obligaciones fiscales, impuestos, declaraciones, vencimientos, comprobantes, facturación, remitos, pedidos, carga de facturas, documentación comercial y cumplimiento tributario. |

La conciliación futura debería relacionar ambos modelos sin confundir una venta,
un comprobante y un cobro. Un saldo reflejado podría estar desactualizado; una
factura preparada no equivaldría a emisión oficial; una declaración preparada no
equivaldría a presentación aceptada. Fuente, fecha, moneda, estado y evidencia de
confirmación deberían acompañar cada registro, así como diferencias pendientes.

## Facturación y documentación comercial futuras

IA_CORE podría, en el futuro y bajo integración autorizada, asistir en emisión de
facturas, carga de facturas recibidas, carga de remitos, carga de pedidos,
documentación comercial, preparación de comprobantes y conciliación entre ventas,
cobros, bancos y obligaciones fiscales. El origen documental y las correcciones
deberían ser trazables, con revisión de duplicados y discrepancias antes de una
acción sensible. Aquí no se crean comprobantes ni conexiones fiscales.

## Mirrors autorizados

Reglas del diseño futuro: no scraping; no suplantación; no réplica visual engañosa;
no almacenamiento de credenciales en texto plano. ARCA, bancos y organismos
fiscales se mencionan como referencias conceptuales. El mirror debería constituir
una capa autorizada, segura, trazable y contractual, con fuente oficial visible.
Podría seguir el flujo mental conocido por el usuario, preservando límites,
autorización y confirmación humana cuando corresponda.

Una futura conexión requeriría evaluar el mecanismo oficial permitido, contrato,
permisos y gestión segura de credenciales en un trabajo posterior. Este documento
no prescribe scraping, conexiones, configuración bancaria ni configuración fiscal
real. Tampoco atribuye disponibilidad actual a APIs de organismos específicos.

## País y jurisdicción

La configuración futura debería contemplar país, región, jurisdicción, moneda,
organismo fiscal, banco, regulador, idioma, reglas tributarias, tipo de empresa,
tipo de cliente y actividad económica. Las reglas requerirían fuente, vigencia y
revisión profesional aplicables al caso.

Argentina podría usar el organismo fiscal local correspondiente, con ARCA como
referencia conceptual del prompt; otros países deberían usar su equivalente.
No se fija una única jurisdicción universal ni se codifican reglas impositivas.
Este modelo no ofrece asesoramiento fiscal o financiero para un caso concreto.

## Autorización humana y evidencia

La asistencia futura podría ordenar, alertar, preparar, conciliar y documentar
información fiscal/financiera. Pagos, declaraciones, presentaciones tributarias y
otras acciones sensibles requerirían autorización humana, contrato aplicable,
trazabilidad y revisión correspondiente. La propuesta, aprobación, envío y resultado
oficial deberían distinguirse; un fallo o resultado incierto requeriría conciliación
antes de repetir una operación. La separación entre preparación y aprobación
debería configurarse según riesgo y organización.

Este modelo depende conceptualmente del [registro de integraciones](FUTURE_INTEGRATIONS_REGISTRY.md),
del [acceso organizacional](FUTURE_ORGANIZATIONAL_ACCESS_MODEL.md) y de la
[revisión legal](FUTURE_LEGAL_COMPLIANCE_AND_JURISDICTIONS_MODEL.md).
