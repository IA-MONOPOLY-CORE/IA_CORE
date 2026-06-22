"""Panel para crear nuevos agentes desde la UI."""

import json
from pathlib import Path

import streamlit as st
from config import ROOT_DIR


def render():
    st.header("➕ Crear Nuevo Agente")
    
    st.markdown("""
    > Crea un nuevo agente cognitivo con su propia identidad y memoria.
    > El agente se generará automáticamente y estará disponible en el sistema.
    """)
    
    with st.form("create_agent_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            agent_id = st.text_input(
                "ID del agente",
                placeholder="ej: analista_conductual",
                help="Identificador único. Se usará para el archivo JSON."
            )
            
            role = st.selectbox(
                "Rol",
                ["analyst", "critic", "optimizer", "orchestrator", "explorer", "auditor"],
                help="Define la función del agente en el debate"
            )
        
        with col2:
            provider = st.selectbox(
                "Proveedor LLM",
                ["nvidia", "ollama", "openai", "claude"],
                index=0
            )
            
            model = st.text_input(
                "Modelo",
                placeholder="meta/llama-3.1-8b-instruct",
                help="Nombre del modelo según el provider"
            )
        
        temperature = st.slider(
            "Temperatura (creatividad)",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1
        )
        
        system_prompt = st.text_area(
            "System Prompt (identidad base)",
            height=150,
            placeholder="Ej: Eres un analista especializado en detectar patrones de comportamiento humano..."
        )
        
        st.subheader("📄 Memoria de entrenamiento")
        uploaded_file = st.file_uploader(
            "Subir conversación/completar (opcional)",
            type=["txt", "md", "json"],
            help="Si se sube, se indexará automáticamente en la memoria vectorial"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submitted = st.form_submit_button("🚀 Crear agente", use_container_width=True)
        with col_btn2:
            st.form_submit_button("Cancelar", use_container_width=True)
    
    if submitted:
        if not agent_id:
            st.error("❌ El ID del agente es obligatorio")
            return
        
        if not system_prompt.strip():
            st.error("❌ El System Prompt es obligatorio")
            return
        
        # Crear estructura del agente
        agent_config = {
            "id": agent_id,
            "role": role,
            "provider": provider,
            "model": model if model else ("phi3:mini" if provider == "ollama" else "meta/llama-3.1-8b-instruct"),
            "temperature": temperature,
            "system_prompt": system_prompt,
            "instructions": []
        }
        
        # Guardar JSON
        config_dir = ROOT_DIR / "agents" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        json_path = config_dir / f"{agent_id}.json"
        
        if json_path.exists():
            st.warning(f"⚠️ Ya existe un agente con ID '{agent_id}'. ¿Sobrescribir?")
            if not st.button("Confirmar sobrescritura"):
                return
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(agent_config, f, indent=2, ensure_ascii=False)
        
        st.success(f"✅ Agente '{agent_id}' creado en {json_path}")
        
        # Procesar archivo subido
        if uploaded_file is not None:
            st.info(f"📄 Procesando archivo: {uploaded_file.name}")
            try:
                content = uploaded_file.read().decode("utf-8")
                
                # Indexar en memoria vectorial
                from core.memoria_perpetua import sincronizar_memoria_vectorial
                fragmentos = sincronizar_memoria_vectorial(agent_id, content)
                st.success(f"✅ Memoria vectorial indexada: {fragmentos} fragmentos")
                
                # Generar paper automáticamente
                st.info("🔧 Generando paper de identidad...")
                # Aquí se llamaría a la función mejorar_paper
                st.warning("⚠️ La generación automática de paper requiere integración con mejorar_papers.py")
                
            except Exception as e:
                st.error(f"❌ Error procesando archivo: {e}")
        
        st.balloons()
        st.info("🔄 Para usar el nuevo agente, reiniciá la UI o seleccionalo en el panel de agentes")


def render_quick():
    """Versión simplificada para mostrar en otros paneles."""
    st.caption("Usa el panel 'Crear Agente' para agregar nuevos perfiles")