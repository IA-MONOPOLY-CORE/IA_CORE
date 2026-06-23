# IA_CORE

Sistema cognitivo local modular: supervisor, agentes con roles, herramientas, memoria persistente y orquestación multi-agente.

## Requisitos

- Python 3.11+
- [Ollama](https://ollama.com/) (para inferencia local con `phi3:mini`)
- Una clave NVIDIA NIM en `.env`:

```powershell
NVIDIA_API_KEY=nvapi-...
```

Los comandos asumen que `python` apunta a Python 3.11+ (`python --version`). Si Windows no lo tiene en `PATH`, usa la ruta completa a tu `python.exe` para crear el entorno virtual.

## Instalación limpia

```powershell
cd c:\IA_CORE
python -m venv venv
.\venv\Scripts\activate
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements-api.txt -r requirements-ui.txt
```

## API local

```powershell
.\venv\Scripts\python.exe api.py
```

La API queda disponible por defecto en `http://localhost:8000`.

## Arranque por consola

Este modo ejecuta una orquestación local y espera que Ollama esté instalado, con el modelo `phi3:mini` disponible.

```powershell
ollama pull phi3:mini
.\venv\Scripts\python.exe main.py
```

## Interfaz visual (Streamlit)

Dashboard local para operar el sistema sin tocar el código.

```powershell
cd c:\IA_CORE
.\venv\Scripts\activate
.\venv\Scripts\python.exe -m pip install -r requirements-api.txt -r requirements-ui.txt
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
