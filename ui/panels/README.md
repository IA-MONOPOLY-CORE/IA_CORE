# Paneles internos de Streamlit

`ui/app.py` y los módulos de este directorio forman una interfaz deprecada,
pendiente de eliminación. Su propósito histórico fue administración,
diagnóstico y debugging local con acceso directo al Core dentro del mismo
proceso.

La interfaz principal y el destino de las nuevas funcionalidades de producto es
el HUD web de `ui/web/`, servido por FastAPI y conectado mediante `/api/*`.

## Política de mantenimiento

- Las capacidades internas reales ya fueron migradas al HUD web.
- No se agregan nuevas funcionalidades de producto a estos paneles.
- Sólo se permiten correcciones imprescindibles hasta eliminar Streamlit.

El HUD de `ui/web/` es la única interfaz activa a futuro y opera mediante
FastAPI; Streamlit no debe recibir nuevas dependencias ni integraciones.
