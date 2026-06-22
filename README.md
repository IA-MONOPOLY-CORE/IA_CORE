# IA_CORE

Sistema cognitivo local modular: supervisor, agentes con roles, herramientas, memoria persistente y orquestación multi-agente.

## Requisitos

- Python 3.11+
- [Ollama](https://ollama.com/) (para inferencia local con `phi3:mini`)

```powershell
cd c:\IA_CORE
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements-ui.txt
ollama pull phi3:mini
```

## Arranque por consola

```powershell
.\venv\Scripts\python.exe main.py
```

## Interfaz visual (Streamlit)

Dashboard local para operar el sistema sin tocar el código.

```powershell
cd c:\IA_CORE
.\venv\Scripts\activate
pip install -r requirements-ui.txt
streamlit run ui/app.py
```

1. Abre el navegador en la URL que muestra Streamlit (por defecto `http://localhost:8501`).
2. En la barra lateral, pulsa **Connect supervisor**.
3. Navega por los paneles: Overview, Agents, Providers, Orchestration, Memory, Logs.

La UI consume el `Supervisor` existente; no duplica la lógica del núcleo.

**Idiomas:** español por defecto. Selector en la barra lateral (Español / English). Traducciones en `ui/i18n/translations/`.

## Enrutamiento híbrido

`core/hybrid/` selecciona proveedor local (Ollama/phi3) u online según conectividad, política de recursos y `config.HYBRID_MODE`. Sin APIs de pago implementadas aún — solo arquitectura, fallback y métricas. Panel **Híbrido** en la UI.

## Estructura

```
core/          Supervisor y orquestación
agents/        Agentes y roles
tools/         Herramientas dinámicas
memory/        Estado JSON persistente
providers/     Proveedores LLM
ui/            Interfaz Streamlit
```

## Tests

```powershell
.\venv\Scripts\python.exe -m pytest tests\ -q --ignore=tests/test_ollama_integration.py
```
