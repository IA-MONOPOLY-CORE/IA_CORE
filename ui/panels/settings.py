"""Panel de configuración visual S.A.A.O.P."""

import json
import re
from pathlib import Path

import streamlit as st
from config import ROOT_DIR


def _cargar_config():
    """Carga la configuración actual desde config.py."""
    config_path = ROOT_DIR / "config.py"
    if not config_path.exists():
        return {}
    
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extraer valores
    nvidia_key = re.search(r'NVIDIA_API_KEY = "([^"]+)"', content)
    nvidia_model = re.search(r'NVIDIA_DEFAULT_MODEL = "([^"]+)"', content)
    fallback_chain = re.search(r'PROVIDER_FALLBACK_CHAIN: list\[str\] = \[([^\]]+)\]', content)
    
    return {
        "nvidia_key": nvidia_key.group(1) if nvidia_key else "",
        "nvidia_model": nvidia_model.group(1) if nvidia_model else "meta/llama-3.1-8b-instruct",
        "fallback_chain": fallback_chain.group(1) if fallback_chain else '"nvidia", "ollama"'
    }


def render():
    st.header("⚙️ Configuración Estratégica")
    
    st.markdown("""
    > Panel de control central. Los cambios aquí afectan a la configuración global del sistema.
    """)
    
    config = _cargar_config()
    
    with st.expander("🎯 Proveedores de IA", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            provider_priority = st.selectbox(
                "Proveedor principal",
                ["nvidia", "ollama", "openai", "claude"],
                index=0 if "nvidia" in config.get("fallback_chain", "") else 1,
                help="Define qué motor IA se usa por defecto"
            )
        
        with col2:
            st.selectbox(
                "Modo de ejecución",
                ["HYBRID", "LOCAL_ONLY", "CLOUD_ONLY"],
                index=0,
                help="HYBRID: mezcla local/cloud | LOCAL_ONLY: solo Ollama | CLOUD_ONLY: solo NVIDIA"
            )
    
    with st.expander("🔑 NVIDIA API", expanded=False):
        nvidia_key = st.text_input(
            "API Key",
            value=config.get("nvidia_key", ""),
            type="password",
            help="Obtener en build.nvidia.com"
        )
        
        nvidia_model = st.selectbox(
            "Modelo",
            ["meta/llama-3.1-8b-instruct", "meta/llama-4-maverick-17b-128e-instruct"],
            index=0 if "3.1" in config.get("nvidia_model", "") else 1
        )
        
        if st.button("🔌 Testear conexión", use_container_width=True):
            with st.spinner("Conectando..."):
                try:
                    from providers.nvidia_provider import NvidiaProvider
                    provider = NvidiaProvider(api_key=nvidia_key)
                    response = provider.generate(
                        prompt="Decime 'OK'",
                        model=nvidia_model,
                        temperature=0.1
                    )
                    st.success(f"✅ Conexión exitosa")
                    st.caption(str(response)[:200])
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    with st.expander("🦙 Ollama (Local)", expanded=False):
        st.info("Ollama corre en localhost:11434")
        if st.button("🧪 Probar conexión", use_container_width=True):
            try:
                import requests
                r = requests.get("http://localhost:11434/api/tags", timeout=3)
                if r.status_code == 200:
                    models = r.json().get("models", [])
                    st.success(f"✅ Ollama conectado. Modelos: {len(models)}")
                else:
                    st.warning("⚠️ Respuesta inesperada")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with st.expander("🎨 Apariencia", expanded=False):
        theme_options = ["Dark (default)", "Light", "Cyberpunk", "Minimal"]
        selected_theme = st.selectbox("Tema visual", theme_options, index=0)
        st.info("Los cambios de tema requieren recargar la página")
        if st.button("🔄 Aplicar tema", use_container_width=True):
            st.session_state["theme"] = selected_theme.lower()
            st.rerun()
    
    with st.expander("💾 Guardar cambios", expanded=True):
        col_save, col_reset = st.columns(2)
        with col_save:
            if st.button("💾 Guardar configuración", use_container_width=True, type="primary"):
                st.info("Por ahora en modo simulación. La edición directa de config.py está en desarrollo.")
                st.json({
                    "nvidia_model": nvidia_model,
                    "provider_priority": provider_priority
                })
                st.success("✅ Configuración guardada (simulación)")
        with col_reset:
            if st.button("🔄 Resetear", use_container_width=True):
                st.warning("Resetearía a config original (pendiente)")
    
    st.divider()
    st.caption("S.A.A.O.P. — Configuración centralizada v1.0")