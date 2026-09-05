# IA_CORE - Modelo futuro de Root Control Plane, Owner Nodes y continuidad operativa

Estado: futuro; estratégico; no implementado; pendiente de implementación;
sin servidores; sin infraestructura real; sin cloud; sin failover; sin nodos;
sin runtime; sin execution; sin endpoints; sin integraciones reales;
sin conectores reales; sin credenciales.

## Propósito y separación de responsabilidades

IA_CORE debería evitar depender físicamente del equipo personal del owner. Esta
visión futura separa gobierno, interfaces, nodos autorizados, instancias cliente,
continuidad y recuperación. Amplía el
[índice estratégico](FUTURE_PLATFORM_EXTENSION_INDEX.md) sin crear servidores,
topología, sincronización, elección de líder ni infraestructura.

### 1. Root Control Plane

Root Control Plane sería la capa central futura de gobierno, coordinación, estado
crítico, licencias, clientes, backups, auditoría, health checks, recovery, soporte
autorizado, versiones y continuidad. Su autoridad debería estar definida por
contrato, identidad, permisos y evidencia, no por la ubicación de una computadora.

### 2. Owner Console

Owner Console sería la interfaz soberana desde donde el owner podría gobernar el
ecosistema, aprobar acciones, revisar salud global, administrar clientes, gestionar
soporte, revisar auditoría y recuperar acceso.

Owner Console no es el servidor. Owner Console es la interfaz soberana del owner
hacia el ecosistema IA_CORE.

### 3. Owner Nodes

Owner Nodes serían equipos autorizados del owner que podrían cumplir funciones de
nodo principal, secundario, standby, recuperación, cómputo o administración. Ser
un dispositivo del owner no concedería automáticamente autoridad de nodo.

### 4. Client Instances

Client Instances serían instancias aisladas de cada cliente o empresa, con sus
propios permisos, contratos, módulos, usuarios, agentes, datos, integraciones
habilitadas y auditoría. No deberían heredar disponibilidad ni autoridad de la PC
personal del owner.

### 5. Continuity Layer

Continuity Layer sería la capa conceptual futura que evitaría que una falla del
owner o de un equipo congele el ecosistema. Debería separar continuidad normal,
degradación segura, espera de aprobación y recuperación.

### 6. Backup / Recovery Layer

Backup / Recovery Layer sería la capa conceptual futura para restaurar acceso,
datos, configuración, evidencia, clientes, estados y continuidad ante robo,
rotura, mudanza, pérdida de equipo, pérdida de sesión, corrupción o desastre.

### 7. Cloud Safety Net

Cloud Safety Net sería un respaldo externo mínimo futuro para sostener continuidad,
emergencia, recuperación o una ventana de gracia cuando los nodos principales no
estuvieran disponibles. No reemplazaría aislamiento, permisos ni backups probados.

## Problema que este modelo busca evitar

El diseño futuro debería contemplar escenarios reales como:

- corte de electricidad del owner;
- caída de internet del owner;
- PC owner apagada;
- traslado o mudanza del equipo;
- robo del equipo;
- rotura de disco;
- pérdida de sesión;
- falla de hardware;
- indisponibilidad temporal;
- mantenimiento;
- cambio de ubicación;
- caída de un nodo;
- error humano;
- desastre físico.

Si IA_CORE dependiera de una única computadora personal del owner, una falla local
podría congelar clientes, negocios, agentes, paneles y procesos. Eso no es
aceptable para una empresa real.

IA_CORE no debe fundarse sobre la disponibilidad física del equipo personal del
owner.

IA_CORE debe poder comenzar en una máquina local, pero no debe nacer
arquitectónicamente atado a una sola máquina.

## Principio de continuidad

El owner puede estar desconectado. El ecosistema no debería quedar desconectado
por eso.

IA_CORE debe estar preparado para que el owner gobierne el ecosistema, pero no sea
el punto único de falla del ecosistema. La PC personal del owner no debería ser el
corazón único del sistema.

En la arquitectura futura:

- el owner gobierna dentro de su autoridad;
- los clientes deberían continuar dentro de sus permisos;
- las acciones propias del owner o sensibles podrían quedar pendientes;
- la auditoría debería registrar estados, decisiones y transiciones;
- la recuperación debería estar prevista antes de fallas reales;
- una degradación no debería ampliar permisos para conservar disponibilidad.

## Diferencia entre caída del owner y continuidad del cliente

Si el owner se cae, no se deben pausar las operaciones normales de los clientes.
Lo que se pausa es lo que dependa específicamente del owner, de su negocio, de su
aprobación o de una acción sensible bajo su autoridad.

Podrían quedar pausadas o pendientes:

- acciones que dependan específicamente del owner;
- acciones del negocio propio del owner;
- aprobaciones globales del owner;
- soporte bajo autoridad del owner;
- cambios de configuración global;
- cambios de licencias;
- acciones sensibles que requieran aprobación superior;
- recovery;
- administración global;
- acciones cross-tenant.

No deberían pausarse por la sola indisponibilidad del owner:

- operaciones normales de cada cliente;
- acceso de usuarios cliente;
- tareas autorizadas de bajo riesgo;
- reportes internos del cliente;
- paneles del cliente;
- agentes del cliente dentro de sus permisos;
- integraciones ya autorizadas del cliente;
- auditoría del cliente;
- comunicación interna del cliente;
- procesos propios del cliente que no dependan del owner.

Las instancias cliente no deben congelarse por indisponibilidad del owner. Cada
cliente debe continuar operando dentro de sus propios permisos, contratos,
módulos e integraciones habilitadas.

## Client Instances aisladas

Cada cliente debería funcionar conceptualmente como una instancia aislada:

> Cliente / Empresa
> -> unidades/sedes si aplica
> -> áreas
> -> subáreas
> -> usuarios
> -> roles
> -> agentes
> -> módulos
> -> integraciones habilitadas
> -> datos
> -> reportes
> -> auditoría
> -> permisos
> -> límites

El diseño futuro debería asegurar que:

- la caída de un cliente no derribe a otros clientes;
- la caída del owner no derribe instancias cliente;
- un error en una instancia no contamine otras;
- los datos de un cliente no se mezclen con los de otro;
- el soporte owner respete permisos y trazabilidad;
- las acciones cross-client estén fuertemente gobernadas o prohibidas por defecto.

La continuidad no debería justificar acceso cross-tenant, replicación indiscriminada
ni soporte sin autorización.

## Owner Node Network

La red futura de nodos owner autorizados podría organizarse así:

| Nodo conceptual | Posición futura |
|---|---|
| Owner Node 1 | Principal. |
| Owner Node 2 | Segundo mando / standby. |
| Owner Node 3 | Respaldo. |
| Owner Server Room futuro | Nodo dedicado permanente. |
| Cloud Safety Net | Respaldo externo de emergencia. |

La composición podría evolucionar desde una PC principal hacia una notebook
autorizada, segunda PC, servidor propio, equipo en otra ubicación, server room,
VPS, cloud backup, appliance o nodo dedicado con UPS.

Regla de diseño: no depender de una sola PC. IA_CORE debería contemplar varios
nodos owner autorizados, en distintas máquinas o lugares, capaces de sostener
continuidad si uno falla.

No basta con tener sesión abierta en varias PCs. Debería existir una lógica
gobernada de nodos, autoridad, estado, sincronización, auditoría y prevención de
duplicaciones.

## Línea estricta de mando entre nodos owner

IA_CORE debe tener una línea estricta de mando entre nodos owner.

Los estados mínimos futuros de nodo serían:

| Estado | Interpretación documental futura |
|---|---|
| `primary` | Nodo con autoridad principal confirmada. |
| `secondary` | Segundo mando preautorizado. |
| `standby` | Nodo preparado sin autoridad principal. |
| `candidate` | Nodo elegible pendiente de validación. |
| `degraded` | Nodo con capacidad o confianza reducida. |
| `offline` | Nodo no disponible. |
| `recovering` | Nodo dentro de un proceso de recuperación. |
| `revoked` | Nodo cuya autoridad fue retirada. |
| `maintenance` | Nodo fuera de mando por mantenimiento controlado. |
| `compromised` | Nodo sospechado o confirmado como comprometido. |

La línea futura debería contemplar un nodo principal, uno o más secundarios
preautorizados, jerarquía, promoción controlada, prevención de doble autoridad,
registro de cambios, trazabilidad, verificación antes de asumir mando, degradación
segura ante incertidumbre, revocación de nodos comprometidos y recuperación desde
un dispositivo autorizado.

Si el nodo owner principal desaparece de la red, se apaga, pierde conexión o queda
fuera de servicio, el sistema debe poder promover un nodo secundario preautorizado
como nuevo nodo principal temporal, respetando jerarquía, permisos, auditoría,
configuración mínima diferencial y prevención de duplicaciones.

No deben existir dos nodos owner actuando como autoridad principal al mismo tiempo
sin coordinación explícita del sistema.

Estas reglas son requisitos conceptuales futuros. No describen leader election,
heartbeat, quorum, consenso ni promoción implementados.

## Prevención de duplicaciones y conflicto de autoridad

Los riesgos futuros incluyen:

- dos nodos ejecutando la misma tarea;
- dos nodos aprobando cambios contradictorios;
- doble escritura;
- configuración desincronizada;
- acciones repetidas;
- pérdida de trazabilidad;
- inconsistencias entre clientes;
- conflictos de permisos;
- estados divergentes;
- split-brain conceptual.

Una futura solución debería poder detectar autoridad vigente, registrar quién
tiene mando, bloquear doble liderazgo, degradar a modo seguro, requerir confirmación
adicional ante conflicto, reconciliar estado, auditar cada transición, evitar
duplicación de tareas y evitar aprobación cruzada insegura.

Si la autoridad no pudiera confirmarse, la opción segura debería ser retener las
acciones que requieren mando único y mantener solamente lo permitido por contrato
en modo degradado. Disponibilidad no debería prevalecer sobre aislamiento o
prevención de doble autoridad.

## Estados de continuidad futuros

Estos estados son vocabulario documental futuro, no estados implementados:

- `system_online`
- `system_degraded`
- `system_offline`
- `owner_online`
- `owner_offline`
- `owner_unreachable`
- `owner_recovery_mode`
- `root_available`
- `root_degraded`
- `root_unavailable`
- `client_online`
- `client_degraded`
- `client_offline`
- `node_primary`
- `node_secondary`
- `node_standby`
- `node_promoted`
- `node_revoked`
- `node_compromised`
- `approval_pending`
- `approval_blocked`
- `backup_ok`
- `backup_failed`
- `recovery_required`
- `cloud_safety_net_available`
- `manual_intervention_required`

Los estados no deberían implicar una transición automática ni conceder permisos.
Cada transición futura requeriría precondiciones, evidencia, auditoría y autoridad.

## Acciones que pueden continuar sin owner online

Según permisos y contrato, en el futuro podrían continuar:

- paneles de clientes;
- lectura de datos autorizada;
- análisis internos;
- reportes programados;
- alertas;
- backups;
- auditoría;
- tareas de bajo riesgo;
- integraciones ya autorizadas;
- agentes con permisos limitados;
- comunicación interna;
- monitoreo;
- procesos propios del cliente.

Esta lista no habilita esas acciones ni determina hoy su riesgo. La continuidad
futura debería respetar límites por cliente, rol, módulo, integración y finalidad.

## Acciones que deben quedar retenidas o requerir aprobación

Según propiedad, riesgo y contrato, en el futuro deberían quedar retenidas o
requerir un aprobador autorizado:

- pagos;
- operaciones financieras reales;
- borrado de datos;
- cambios de permisos altos;
- activación de integraciones sensibles;
- acceso soporte a información privada;
- operaciones cross-tenant;
- cambios legales;
- declaraciones fiscales;
- envíos masivos externos;
- cambios de configuración crítica;
- restauración de backups;
- promoción manual de nodos;
- revocación de nodos;
- recuperación owner;
- acciones sobre licencias;
- acciones sobre seguridad global.

No todo depende del owner. Algunas acciones sensibles podrían depender de
aprobadores del cliente cuando pertenezcan al cliente y estén definidas por
contrato. La continuidad owner no debería desplazar su autoridad.

## Server room futuro e inversión en infraestructura

Si IA_CORE generara ingresos suficientes, podría ser razonable evolucionar hacia
infraestructura propia con:

- workstation o server dedicado;
- GPU potente;
- CPU fuerte;
- mucha RAM;
- varios terabytes de almacenamiento;
- UPS;
- almacenamiento externo;
- backups locales;
- backups cloud;
- nodo secundario;
- servidor en ubicación alternativa;
- cuarto dedicado tipo server room;
- monitoreo;
- control térmico;
- protección eléctrica;
- redundancia de internet.

Una máquina potente mejora capacidad, pero no debe convertirse en único punto de
falla. Una composición futura razonable podría ser: PC potente local + UPS + nodo
secundario + backups automáticos + cloud mínimo de continuidad + recovery owner.

La inversión no sustituiría arquitectura, procedimientos, pruebas de restore,
seguridad física, aislamiento ni gobierno de autoridad.

## Almacenamiento, memoria y crecimiento

IA_CORE puede ocupar poco al principio, pero el peso futuro podría provenir de:

- logs;
- auditoría;
- evidencia;
- archivos de clientes;
- documentos;
- backups;
- embeddings;
- historiales;
- capturas;
- reportes;
- datasets;
- modelos locales;
- artefactos generados;
- operaciones;
- versionados;
- integraciones;
- snapshots.

IA_CORE debe separar memoria operativa, evidencia, archivos, backups, modelos y
logs para poder escalar sin volverse un bloque inmanejable.

Cada categoría futura requeriría clasificación, retención, cifrado, ubicación,
cuotas, acceso, borrado y recuperación definidos. Acumular datos no equivale a
crear inteligencia ni garantiza continuidad.

## Recovery del owner

El owner debería poder recuperar acceso ante robo de PC, rotura, pérdida de
sesión, mudanza, reinstalación, dispositivo nuevo, pérdida parcial de datos,
cambio de hardware o incidente de seguridad.

El proceso futuro se conecta con el
[modelo de soberanía y recuperación](FUTURE_OWNER_SOVEREIGNTY_AND_RECOVERY_MODEL.md)
y podría involucrar claves, dispositivos confiables, MFA/passkeys, recovery kit,
backup cifrado, verificación de identidad, auditoría, revocación de dispositivos
perdidos, restauración controlada y alertas de seguridad.

Recovery no debería crear una puerta alternativa sin controles ni restaurar
sesiones o nodos revocados. Ningún flujo se implementa mediante este documento.

## Relación con IA_CORE OS y Device Ecosystem

El [modelo de IA_CORE OS y dispositivos](FUTURE_IA_CORE_OS_AND_DEVICE_ECOSYSTEM.md)
describe el entorno operativo y de dispositivos. Este documento describe la
continuidad, autoridad, nodos owner, recovery y protección ante caídas. Ambos son
visiones futuras y no crean infraestructura ni conexión entre equipos.

## Límites actuales

- Root Control Plane no existe todavía.
- Owner Nodes no existen todavía.
- Owner Node Network no existe todavía.
- No hay failover real.
- No hay leader election real.
- No hay heartbeat real.
- No hay Cloud Safety Net real.
- No hay recovery automático.
- No hay server room IA_CORE.
- No hay nodos distribuidos.
- No hay continuidad operativa distribuida.
- No hay promoción automática de nodo secundario.
- No hay backups cloud conectados por este documento.
- Este documento es exclusivamente estratégico y futuro.

Este documento no implementa servidores, infraestructura, cloud, failover,
nodos, leader election, heartbeat, backups, recovery, scripts, servicios systemd,
contenedores, runtime, workers, schedulers, queues, event bus, dispatchers,
endpoints, integraciones, clientes, credenciales, UI ni contratos backend. No
modifica `backend_internal_ui_payload.v1`.
