"""Panel de gestión de agentes S.A.A.O.P."""

import json

import streamlit as st
from config import ROOT_DIR


def _cargar_agentes():
    """Carga todos los agentes JSON del directorio config."""
    config_dir = ROOT_DIR / "agents" / "config"
    agentes = []
    
    if config_dir.exists():
        for json_file in config_dir.glob("*.json"):
            if json_file.name.endswith(".bak"):
                continue
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                agentes.append({
                    "id": data.get("id", json_file.stem),
                    "role": data.get("role", "unknown"),
                    "provider": data.get("provider", "nvidia"),
                    "model": data.get("model", "-"),
                    "file": json_file.name,
                    "active": True  # Por ahora todos activos
                })
            except Exception as e:
                st.warning(f"Error cargando {json_file.name}: {e}")
    
    return sorted(agentes, key=lambda x: x["id"])


def render():
    st.header("🧠 Agentes Cognitivos del Búnker")
    
    agentes = _cargar_agentes()
    
    st.markdown(f"""
    > **Total de agentes disponibles:** `{len(agentes)}`
    > Cada agente tiene una identidad, un rol y una memoria vectorial propia.
    """)
    
    # Selector de agente activo (vista detalle)
    agente_ids = [a["id"] for a in agentes]
    selected_agent = st.selectbox("Seleccionar agente para ver detalles", agente_ids)
    
    # Mostrar detalle del agente seleccionado
    agente = next((a for a in agentes if a["id"] == selected_agent), None)
    if agente:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rol", agente["role"].upper())
        with col2:
            st.metric("Provider", agente["provider"].upper())
        with col3:
            st.metric("Modelo", agente["model"].split("/")[-1] if "/" in agente["model"] else agente["model"])
        
        # Verificar paper
        paper_path = ROOT_DIR / "agents" / "papers" / f"{agente['id']}_paper.json"
        if paper_path.exists():
            st.success(f"✅ Paper de identidad encontrado")
            if st.button("📄 Ver paper", use_container_width=True):
                with open(paper_path, "r", encoding="utf-8") as f:
                    paper = json.load(f)
                st.json(paper)
        else:
            st.warning(f"⚠️ No se encontró paper para {agente['id']}")
            if st.button("🔧 Generar paper desde memoria", use_container_width=True):
                st.info("Función en desarrollo - usar consola: python mejorar_papers.py")
    
    # Lista de todos los agentes
    st.divider()
    st.subheader("📋 Escuadrón Completo")
    
    # Tabla de agentes
    table_data = []
    for a in agentes:
        table_data.append({
            "ID": a["id"],
            "Rol": a["role"],
            "Provider": a["provider"],
            "Modelo": a["model"][:30] + "..." if len(a["model"]) > 30 else a["model"]
        })
    
    st.dataframe(table_data, use_container_width=True)
    
    # Acciones masivas (placeholder)
    st.divider()
    st.subheader("⚙️ Acciones")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Sincronizar memorias vectoriales", use_container_width=True):
            st.info("Función en desarrollo - usar consola: python indexar_perfiles.py")
    with col2:
        if st.button("📊 Ver ranking de herramientas", use_container_width=True):
            st.info("Función en desarrollo")
