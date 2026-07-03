# IA_CORE

Sistema cognitivo local modular: motor de debate multiagente genérico con arquitectura separada por dominios.

## Arquitectura

IA_CORE es un **motor de debate multiagente genérico** que puede usarse en cualquier dominio. El proyecto incluye un caso de uso específico implementado en domains/loteria/:

- core/: Motor genérico de debate multiagente (Supervisor, orquestación, memoria persistente, gestión de proveedores LLM)
- domains/loteria/: Caso de uso específico para análisis de Lotería con el framework S.A.A.O.P. (Sistema de Análisis y Arbitraje de Oportunidades Probabilísticas)

Esta separación permite reutilizar el motor genérico en otros dominios sin contaminar el código base con lógica específica.

## Caso de uso: S.A.A.O.P. (Lotería)

El sistema incluye 6 agentes especializados para análisis de Lotería:

1. gpt_auditor (Critic) - Escéptico que destruye hipótesis
2. gemini_cuantico (Analyst Zones) - Explorador de zonas y densidad energética
3. viejo_lobo_rey (Analyst Human) - Integrador con perspectiva humana
4. estadistico_integral (Analyst) - Defensor de la hipótesis V19
5. viejo_deepseek (Optimizer) - Árbitro matemático
6. nuevo_deepseek_saaop (Orchestrator) - Cierre metodológico

Estos agentes participan en debates estructurados para evaluar combinaciones de lotería usando métricas específicas (U-Score v2.1, zonas Z1-Z9, pesos zonales, etc.).

## Requisitos

- Python 3.11+
- Ollama (para inferencia local con phi3:mini)
- Una clave NVIDIA NIM en .env:

NVIDIA_API_KEY=nvapi-...

Los comandos asumen que python apunta a Python 3.11+ (python --version). Si Windows no lo tiene en PATH, usa la ruta completa a tu python.exe para crear el entorno virtual.

## Instalación limpia

cd c:\IA_CORE
python -m venv venv
.\venv\Scripts\activate
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements-api.txt -r requirements-ui.txt

## API local

.\venv\Scripts\python.exe api.py

La API queda disponible por defecto en http://localhost:8000.

## Arranque por consola

Este modo ejecuta una orquestación local y espera que Ollama esté instalado, con el modelo phi3:mini disponible.

ollama pull phi3:mini
.\venv\Scripts\python.exe main.py

## Interfaces visuales

El **HUD web de `ui/web/` es la interfaz principal**. FastAPI lo sirve en
http://localhost:8000 y el frontend consume el backend mediante `/api/*`.

Streamlit está deprecado y pendiente de eliminación. Sus capacidades internas
reales ya fueron migradas al HUD; no recibe nuevas funcionalidades ni
integraciones.

Para iniciar el panel interno de Streamlit:

cd c:\IA_CORE
.\venv\Scripts\activate
.\venv\Scripts\python.exe -m pip install -r requirements-api.txt -r requirements-ui.txt
streamlit run ui/app.py

1. Abre el navegador en la URL que muestra Streamlit (por defecto http://localhost:8501).
2. En la barra lateral, pulsa Connect supervisor.
3. Navega por los paneles: Overview, Agents, Providers, Orchestration, Memory, Logs.

Streamlit consume el Supervisor directamente dentro de su proceso. El HUD web,
en cambio, accede al sistema exclusivamente a través de la API FastAPI.

Idiomas: español por defecto. Selector en la barra lateral (Español / English). Traducciones en ui/i18n/translations/.

## Enrutamiento híbrido

core/hybrid/ selecciona proveedor local (Ollama/phi3) u online según conectividad, política de recursos y config.HYBRID_MODE. Panel Híbrido en la UI.

## Estructura

core/                  Motor genérico de debate multiagente
  base.py              Contrato ABC para componentes del sistema
  debate.py            Motor de debate multi-ronda
  evolution_base.py    Clase base genérica para sistemas evolutivos
  herramientas.py      Sistema de herramientas compartidas
  memoria_perpetua.py  Sistema de memoria con ChromaDB
  orchestration.py     Modelos de datos para orquestación
  supervisor.py        Orquestador principal de debates
  hybrid/              Enrutamiento híbrido local/online

agents/                Gestión genérica de agentes
  base.py              Contrato ABC para agentes
  manager.py           Registro y carga dinámica de agentes
  prompts.py           Construcción de prompts por rol
  roles.py             Enum de roles genéricos
  runtime_json_agent.py Implementación de agente desde JSON
  loader.py            Descubrimiento de módulos de agentes

providers/             Proveedores LLM
  base.py              Contrato ABC para proveedores
  registry.py          Registro de proveedores
  claude_provider.py   Implementación Claude
  deepseek_provider.py Implementación DeepSeek
  gemini_provider.py   Implementación Gemini
  groq_provider.py     Implementación Groq
  nvidia_provider.py   Implementación NVIDIA NIM
  ollama_provider.py   Implementación Ollama
  openai_provider.py   Implementación OpenAI
  openrouter_provider.py Implementación OpenRouter

tools/                 Gestión de herramientas
  manager.py           Catálogo de herramientas
  loader.py            Descubrimiento de módulos de herramientas

domains/loteria/       Caso de uso específico: Lotería/S.A.A.O.P.
  config_loteria.py    Configuración específica (agentes, límites, mapeos)
  debate_loteria.py    Patrones de contradicción específicos
  prompts_loteria.py   Prompts específicos de los 6 agentes
  evolution_loteria.py Gestión evolutiva específica de Lotería
  scoring.py           U-Score v2.1 (100% específico)
  uscore_calculator.py Calculadora U-Score v2.1
  backtest_ciego.py    Backtesting ciego específico
  cargar_sorteos.py    Carga de sorteos específica
  lotoplus_completo_3511_3885.json Datos históricos
  agents/config/       Configuraciones JSON de los 6 agentes

memoria_agentes/       Memoria persistente por agente (JSON)
memoria_vectorial/     Memoria vectorial por agente (ChromaDB)
ui/web/                HUD web principal servido por FastAPI
ui/app.py              Panel interno secundario de Streamlit
ui/panels/             Administración y debugging internos de Streamlit
config.py              Configuración global del proyecto
api.py                 API REST FastAPI

## Tests

.\venv\Scripts\python.exe -m pytest tests\ -q --ignore=tests/test_ollama_integration.py
