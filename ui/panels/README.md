# Paneles internos de Streamlit

`ui/app.py` y los módulos de este directorio forman la interfaz secundaria de
IA_CORE. Su propósito es administración, diagnóstico y debugging local con
acceso directo al Core dentro del mismo proceso.

La interfaz principal y el destino de las nuevas funcionalidades de producto es
el HUD web de `ui/web/`, servido por FastAPI y conectado mediante `/api/*`.

## Política de mantenimiento

- Streamlit no se elimina todavía: conserva las herramientas internas que aún
  no fueron migradas al HUD.
- No se agregan nuevas funcionalidades de producto a estos paneles.
- Se permiten correcciones y mantenimiento necesarios para administración y
  debugging.
- Una función sólo se considera migrada cuando existe en el HUD y opera a través
  de la API; el acceso directo al Core queda reservado para uso interno.

Esta decisión no cambia por ahora el arranque, el mount de FastAPI ni las rutas
existentes de ninguna de las dos interfaces.
