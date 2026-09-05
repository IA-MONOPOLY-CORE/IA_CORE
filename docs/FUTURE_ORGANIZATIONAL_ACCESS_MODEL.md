# Modelo futuro de acceso organizacional

Estado: futuro; estratégico; no implementado; pendiente de implementación;
sin runtime; sin execution; sin endpoints; sin integraciones reales;
sin conectores reales; sin credenciales.

## Propósito

Proyectar IA_CORE como estructura de empresa digital real futura: humanos,
sectores, responsables, colaboradores, permisos, paneles, herramientas,
comunicación, evidencia y reportes, además de agentes. Este modelo no crea
usuarios, empleados, autenticación ni multi-tenant real.
Forma parte del [índice estratégico](FUTURE_PLATFORM_EXTENSION_INDEX.md).

## Roles y alcance propuestos

| Rol | Responsabilidad futura y límite |
|---|---|
| `owner` | Gobierno de su empresa y delegación dentro de contrato y privacidad. |
| `admin` | Administración delegada de usuarios y estructura autorizada. |
| `director` | Coordinación de sectores y resultados bajo autoridad asignada. |
| `sector_manager` | Responsables, herramientas y permisos delegables del sector. |
| `supervisor` | Supervisión de equipos y revisión de trabajo autorizado. |
| `operator` | Acciones operativas expresamente permitidas. |
| `collaborator` | Participación acotada en tareas, proyectos o unidades. |
| `viewer` | Lectura del alcance asignado. |
| `support` | Asistencia temporal expresamente autorizada y auditada. |
| `external_auditor` | Lectura de evidencia habilitada para una auditoría concreta. |

El superior podría administrar hacia abajo dentro de su alcance autorizado.
El subordinado no podría modificar estructura ni permisos salvo autorización
explícita. Las jerarquías no deberían ser decorativas: el alcance efectivo debería
combinar rol, sector, unidad, empresa, jerarquía y contrato; una denegación o
separación de funciones impediría que el título del cargo otorgue acceso.
Soporte y auditoría externa son funciones acotadas, no escalones de acceso universal.
Nadie debería delegar autoridad que no posee ni acceder a otra empresa por jerarquía.

## Alta futura de usuarios

Se proyectan comandos visibles como Agregar empleado, Agregar colaborador y
Agregar responsable. El flujo futuro contemplaría invitación por email,
contraseña temporal de uso limitado y cambio obligatorio de contraseña, acceso al
panel correspondiente, asignación de permisos por rol, sector, unidad, empresa y
jerarquía, y auditoría de alta. La entrega y caducidad de la credencial temporal
requerirían diseño de seguridad; aquí no se genera ni envía ninguna contraseña.
Cambios de puesto, baja y revocación deberían retirar accesos asociados y dejar
evidencia, incluida la delegación a agentes.

## Sectores empresariales futuros

- Dirección; Marketing; Ventas; Atención al cliente.
- Administración; Tesorería; Contabilidad; Fiscalidad/Impuestos; Legal/Compliance.
- Recursos Humanos; Operaciones; TI/Soporte técnico interno; Ciberseguridad.
- Compras; Proveedores; Logística/Supply Chain.
- Auditoría interna; Riesgo empresarial; Gobierno de datos; Gobierno corporativo.
- Calidad/Mejora continua; Producto/I+D; Continuidad del negocio.
- Soporte IA_CORE autorizado, separado del TI interno de la empresa cliente.

Cada sector podría disponer de responsables, colaboradores, agentes especializados,
herramientas y paneles según necesidad. La lista no habilita ninguno de ellos.

## Unidades y ejemplos conceptuales

La estructura futura contemplaría sucursales, oficinas, sedes, zonas, franquicias,
marcas internas, locales, unidades de negocio, países y regiones. Un sector podría
compartirse entre unidades sin compartir automáticamente todos sus datos o permisos.

Bohemian Food ilustra una empresa con dos locales/unidades: Villa Morra y Márquez.
El marketing podría compartirse parcialmente, con campañas, públicos, zonas y
productos diferentes; responsables y acceso a resultados deberían preservar ese
alcance. Es un ejemplo conceptual, no un cliente configurado.

Un estudio contable ilustra una empresa con múltiples oficinas, equipos y
responsables por oficina. El acceso a los expedientes de cada oficina requeriría
asignación explícita aun dentro de una misma empresa.

## Escala y dependencias

Principio futuro: IA_CORE no fuerza complejidad. IA_CORE escala complejidad.
Un negocio chico podría usar pocos módulos; una empresa grande podría activar
estructura completa según necesidad, negocio, sector y plan.
El [modelo de comunicación](FUTURE_INTERNAL_COMMUNICATION_MODEL.md) debería respetar
estos alcances. La autoridad del proveedor se delimita aparte en el
[modelo owner](FUTURE_OWNER_SOVEREIGNTY_AND_RECOVERY_MODEL.md).
