# IA_CORE - Modelo futuro de áreas, subáreas y paneles corporativos

Estado: futuro; estratégico; no implementado; pendiente de implementación;
sin runtime; sin execution; sin endpoints; sin integraciones reales;
sin conectores reales; sin credenciales.

## Propósito

IA_CORE debería poder representar empresas reales como estructuras
organizacionales modulares, no como simples listas de agentes o herramientas.
Este modelo amplía el [índice estratégico](FUTURE_PLATFORM_EXTENSION_INDEX.md)
sin crear estructura organizacional, paneles, usuarios, permisos ni capacidades
reales. Tampoco modifica la UI activa ni los contratos backend existentes.

La jerarquía conceptual futura es:

> Empresa
> -> área madre
> -> subárea
> -> sector/equipo
> -> responsable
> -> colaboradores
> -> agentes
> -> herramientas/módulos
> -> permisos
> -> reportes
> -> evidencia

Las áreas y subáreas son estructura empresarial. Las herramientas, mirrors,
integraciones, paneles y módulos son capacidades que podrían vivir dentro o
alrededor de esas áreas. Tesorería, impuestos, Legal, Compliance,
Ciberseguridad y Auditoría no deben confundirse con integraciones externas.
Un mirror financiero, fiscal, legal o documental no es el área: es una
herramienta o vista especializada al servicio de un área o subárea.

IA_CORE no debería forzar complejidad visible inicial. La estructura proyectada
debe poder escalar desde un negocio chico hasta una empresa grande, multiárea,
multiusuario, multisede y multijurisdicción.

## Reglas rectoras

IA_CORE debe permitir que cada área y subárea corporativa pueda convertirse en
panel operativo propio cuando el negocio, la escala, el riesgo, el volumen de
trabajo o la necesidad de control lo justifiquen.

Una subárea no visible por defecto no significa que no exista: puede estar
agrupada, simplificada, fusionada o pendiente de activación según el tamaño, el
rubro, la etapa y la necesidad real del cliente.

Todo merece control, chequeo e interacción, pero no todo merece complejidad
visible desde el primer día.

Estas reglas describen una arquitectura futura. No habilitan paneles, acciones,
permisos, usuarios, agentes, datos, integraciones ni ejecución.

## Taxonomía corporativa mínima futura

La taxonomía es extensible, configurable y subordinada a contrato, permisos,
escala y necesidad real. Los nombres no conceden autoridad ni implican que los
componentes estén implementados. En cada área, las listas siguientes describen
subáreas posibles.

### 1. Dirección / Gobierno ejecutivo

- Dirección general
- Estrategia
- Toma de decisiones
- Priorización
- Gobierno interno
- Revisión ejecutiva
- Control de objetivos

### 2. Finanzas / Administración financiera

- Tesorería
- Contabilidad
- Fiscalidad / Impuestos
- Facturación
- Cuentas a pagar
- Cuentas a cobrar
- Conciliación bancaria
- Presupuestos
- Control de caja
- Control de costos
- Rentabilidad
- Flujo de fondos
- Proyecciones financieras

Finanzas debe ser tratada como área madre. Tesorería, Contabilidad, Impuestos y
Facturación son subáreas o sectores que pueden tener panel propio si la escala,
el riesgo, el volumen o la necesidad de control lo justifican.

### 3. Administración

- Documentación
- Procesos internos
- Gestión operativa administrativa
- Archivo
- Proveedores administrativos
- Trámites
- Control documental

### 4. Marketing

- Marca
- Comunicación
- Campañas
- Contenido
- Diseño
- Publicidad
- Investigación de mercado
- Posicionamiento
- Canales
- Calendario comercial

### 5. Ventas

- Prospección
- CRM
- Seguimiento comercial
- Cotizaciones / presupuestos
- Conversión
- Postventa comercial
- Pipeline
- Cierres
- Objetivos comerciales

### 6. Atención al cliente / Customer Success

- Consultas
- Reclamos
- Fidelización
- Soporte al cliente
- Experiencia del cliente
- Historial del cliente
- Encuestas
- Casos críticos
- Retención

### 7. Operaciones

- Producción
- Procesos
- Tareas operativas
- Control diario
- Calidad operativa
- Coordinación de equipos
- Turnos operativos
- Incidencias operativas
- Capacidad operativa

### 8. Recursos Humanos

- Empleados
- Horarios
- Turnos
- Asistencia
- Legajos
- Capacitación
- Evaluación de desempeño
- Incidencias laborales
- Contrataciones
- Onboarding
- Cultura interna
- Comunicación interna laboral

### 9. TI / Soporte interno

- Infraestructura
- Sistemas internos
- Dispositivos
- Accesos
- Incidencias técnicas
- Soporte operativo interno
- Inventario tecnológico
- Mantenimiento
- Mesa de ayuda

### 10. Ciberseguridad

- Protección de datos
- Control de accesos
- Monitoreo
- Incidentes
- Hardening
- Auditoría de seguridad
- Gestión de claves
- Seguridad de integraciones
- Seguridad de modelos
- Seguridad de memoria/contexto
- Respuesta ante incidentes

### 11. Legal / Compliance

- Contratos
- Documentación legal
- Riesgos legales
- Jurisdicciones
- Privacidad
- Propiedad intelectual
- Cumplimiento normativo
- Revisión legal
- Aprobaciones legales
- Obligaciones regulatorias

### 12. Compras / Procurement

- Solicitudes de compra
- Órdenes de compra
- Comparación de proveedores
- Negociación
- Aprobaciones
- Historial de compras
- Evaluación de precios
- Reglas de compra

### 13. Proveedores

- Alta de proveedores
- Evaluación
- Contratos
- Pagos pendientes
- Historial
- Riesgo proveedor
- Condiciones comerciales
- Cumplimiento proveedor

### 14. Logística / Supply Chain

- Stock / Inventario
- Depósitos
- Distribución
- Rutas
- Entregas
- Trazabilidad
- Activos físicos
- Abastecimiento
- Movimientos internos

### 15. Auditoría interna

- Controles
- Procesos
- Evidencia
- Desvíos
- Revisión independiente
- Hallazgos
- Recomendaciones
- Seguimiento de correcciones

### 16. Riesgo empresarial

- Riesgo financiero
- Riesgo operativo
- Riesgo legal
- Riesgo reputacional
- Riesgo tecnológico
- Riesgo país
- Riesgo proveedor
- Riesgo comercial
- Riesgo de continuidad
- Riesgo de datos

### 17. Calidad / Mejora continua

- Estándares
- Reclamos
- Errores
- Indicadores
- Procesos de mejora
- Control de calidad
- Correcciones
- Prevención de fallos

### 18. Gobierno de datos

- Calidad de datos
- Acceso a datos
- Retención
- Trazabilidad
- Anonimización
- Clasificación de información sensible
- Políticas de datos
- Ciclo de vida de datos

### 19. Gobierno corporativo

- Socios
- Directorio
- Autoridades
- Actas
- Decisiones estratégicas
- Participación
- Responsabilidades
- Estructura societaria

### 20. Producto / I+D

- Investigación
- Desarrollo
- Nuevos productos
- Testing
- Innovación
- Roadmap de producto
- Validación
- Prototipos
- Mejora de oferta

### 21. Continuidad del negocio

- Planes de contingencia
- Recuperación
- Backups
- Incidentes críticos
- Continuidad operativa
- Simulacros
- Restauración
- Planes de emergencia

### 22. Formación / Capacitación interna

- Manuales
- Onboarding
- Entrenamiento
- Certificación interna
- Procedimientos
- Capacitación por rol
- Evaluaciones
- Biblioteca interna

### 23. Relaciones institucionales

- Alianzas
- Convenios
- Comunicación institucional
- Relación con organismos
- Relaciones públicas
- Representación externa
- Vínculos estratégicos

### 24. Reporting ejecutivo / BI

- KPIs
- Reportes ejecutivos
- Dashboards
- Análisis
- Alertas de gestión
- Inteligencia de negocio
- Lectura transversal
- Recomendaciones ejecutivas

## Estados futuros posibles

Los siguientes estados son vocabulario documental propuesto, no estados
aceptados por un runtime actual:

| Estado | Significado futuro propuesto |
|---|---|
| `future_only` | Existe solo como definición estratégica futura. |
| `suggested` | Podría ser recomendado para evaluación humana. |
| `enabled` | Podría quedar habilitado por configuración, contrato y permiso. |
| `disabled` | Podría estar definido pero no habilitado. |
| `grouped` | Podría mostrarse dentro de una agrupación mayor. |
| `merged` | Podría compartir alcance visible con otra área o subárea. |
| `split` | Podría dividirse en unidades visibles separadas. |
| `renamed` | Podría adoptar terminología propia del cliente. |
| `requires_configuration` | Requeriría configuración válida antes de exponerse. |
| `requires_permissions` | Requeriría permisos explícitos y vigentes. |
| `requires_panel` | Requeriría diseño y contrato de panel propios. |
| `panel_available` | Podría existir una definición de panel disponible para activación. |
| `panel_hidden` | El panel podría permanecer fuera de la experiencia visible. |
| `not_implemented` | No existe implementación de la capacidad descrita. |

Los estados no forman una escalera automática. Por ejemplo, `suggested` no
autoriza `enabled`, y `panel_available` no concede acceso ni acción.

## Escala y composición

### Ejemplo A - Negocio chico

Una hamburguesería puede necesitar Finanzas, Ventas, Marketing, Operaciones y
Atención al cliente, pero no necesita ver 24 áreas desde el primer día. IA_CORE
podría agrupar o simplificar la presentación futura sin borrar la estructura
arquitectónica que permita crecer.

### Ejemplo B - Pyme

Una pyme con empleados, proveedores, facturación, stock y varias sedes puede
separar Finanzas, Recursos Humanos, Compras, Proveedores, Logística, Operaciones
y BI. La separación futura dependería de responsables, permisos y necesidad.

### Ejemplo C - Empresa grande

Una empresa multiunidad o multijurisdicción puede requerir paneles propios para
Tesorería, Fiscalidad, Legal, Compliance, Ciberseguridad, Auditoría, Gobierno de
datos y Riesgo empresarial, con aislamiento y autoridad definidos por contrato.

## Visibilidad progresiva y gobierno

- La complejidad estructural puede existir internamente en el diseño futuro.
- La complejidad visible debe depender del negocio, la escala, el riesgo y los permisos.
- Un usuario no debe ver paneles que no necesita.
- Un `owner` o `admin` autorizado podría activar, agrupar, fusionar, dividir o renombrar áreas y subáreas si el contrato futuro lo permite.
- La ausencia visual no equivale a ausencia arquitectónica.
- Un panel propio no debe ampliar por sí mismo permisos, datos ni autoridad de acción.
- Los reportes y la evidencia deben conservar alcance, fuente, responsable y trazabilidad.

## Límites documentales

Este documento no implementa runtime, workers, schedulers, queues, event bus,
dispatchers, endpoints, integraciones, credenciales, memoria compartida, paneles
ni acciones reales. No modifica `backend_internal_ui_payload.v1`. Toda eventual
implementación requeriría alcance aprobado, contrato, aislamiento, permisos,
evidencia, revisión de seguridad y validación humana según el riesgo.
