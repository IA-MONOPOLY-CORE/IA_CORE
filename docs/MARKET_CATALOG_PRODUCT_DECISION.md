# Market Catalog / Catálogo de Mercados

## 1. Nombre

`Market Catalog / Catálogo de Mercados`

## 2. Estado

`planned_not_active`

## 3. Proposito

El Catálogo de Mercados sera la capa externa de mercado que permitirá a IA_CORE conectar sus capacidades internas con rubros reales para crear negocios digitales, ofertas, equipos de perfiles y unidades operativas.

En esta fase queda registrado como database no activa. No participa en runtime, ejecucion, UI, API, scheduler, worker ni composicion automatica.

## 4. Diferencia Conceptual

Nicho interno IA_CORE:

Capacidad, problema, sistema, dominio operativo o linea de trabajo validada dentro de IA_CORE.

Rubro externo de mercado:

Tipo de cliente, industria, negocio o categoria comercial alcanzable en el mundo real.

## 5. Formula

```txt
Área interna
+
Nicho interno
+
Rubro externo de mercado
+
Perfiles compatibles
=
Equipo operativo / unidad de negocio digital
```

## 6. Ejemplo

Área:

Ventas / Operaciones comerciales

Nicho interno:

Seguimiento de oportunidades comerciales

Rubro externo:

Clínicas dentales

Perfiles posibles:

- Estratega comercial;
- Prospector;
- Copywriter WhatsApp;
- Analista CRM;
- Automatizador.

Unidad de negocio:

Sistema para captar, responder, ordenar y recuperar pacientes interesados.

## 7. Boundaries

- El Market Catalog queda registrado como database no activa.
- No participa en runtime.
- No participa en ejecucion.
- No crea equipos automaticamente.
- No crea ofertas automaticamente.
- No modifica el catalogo interno validado.
- No modifica perfiles/presets.
- No habilita UI.
- No habilita API.
- No habilita scheduler/worker.
- No habilita modelos/tools/memoria.
- No habilita external access.

## 8. Motivo Estrategico

IA_CORE debe poder evolucionar hacia una fabrica de unidades de negocio asistidas por IA. Para eso necesita una capa que conecte capacidades internas con mercados reales.

El Market Catalog prepara esa futura `Business Composition Layer / Capa de Composicion de Negocio`, sin activarla todavia.
