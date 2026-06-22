"""Sistema de memoria perpetua por agente con búsqueda vectorial local (ChromaDB)."""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

# Intentar importar ChromaDB y sentence-transformers
try:
    import chromadb
    from sentence_transformers import SentenceTransformer
    CHROMADB_AVAILABLE = True
    print("✅ ChromaDB y SentenceTransformers cargados correctamente")
except ImportError as e:
    CHROMADB_AVAILABLE = False
    print(f"⚠️ ChromaDB no disponible. Instalar con: pip install chromadb sentence-transformers. Error: {e}")

# Ruta base para las memorias
MEMORIA_BASE = Path(__file__).parent.parent / "memoria_agentes"
MEMORIA_VECTORIAL_BASE = Path(__file__).parent.parent / "memoria_vectorial"

# Tamaño de fragmentos para búsqueda vectorial (caracteres)
CHUNK_SIZE = 2000
# Fragmentos a recuperar por consulta
TOP_K_RESULTS = 5


class MemoriaVectorial:
    """
    Gestor de memoria vectorial con ChromaDB.
    Permite búsqueda por similitud semántica local (sin API).
    """
    
    _instances = {}
    
    def __new__(cls, agente_id: str):
        if agente_id not in cls._instances:
            instance = super().__new__(cls)
            instance._initialized = False
            cls._instances[agente_id] = instance
        return cls._instances[agente_id]
    
    def __init__(self, agente_id: str):
        if self._initialized:
            return
        
        self.agente_id = agente_id
        self.vector_dir = MEMORIA_VECTORIAL_BASE / agente_id
        self.vector_dir.mkdir(parents=True, exist_ok=True)
        
        self.client = None
        self.collection = None
        self.encoder = None
        
        if CHROMADB_AVAILABLE:
            try:
                self.client = chromadb.PersistentClient(path=str(self.vector_dir))
                self.collection = self.client.get_or_create_collection(
                    name=agente_id,
                    metadata={"hnsw:space": "cosine"}
                )
                self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
                print(f"✅ Memoria vectorial inicializada para {agente_id}")
            except Exception as e:
                print(f"⚠️ Error inicializando ChromaDB para {agente_id}: {e}")
                self.client = None
        
        self._initialized = True
    
    def esta_disponible(self) -> bool:
        return CHROMADB_AVAILABLE and self.client is not None
    
    def fragmentar_texto(self, texto: str, chunk_size: int = CHUNK_SIZE) -> List[str]:
        """Divide el texto en fragmentos solapados."""
        if not texto:
            return []
        
        fragmentos = []
        for i in range(0, len(texto), chunk_size // 2):  # 50% solapamiento
            fragmento = texto[i:i + chunk_size]
            if len(fragmento) > 100:  # Ignorar fragmentos muy pequeños
                fragmentos.append(fragmento)
        
        return fragmentos
    
    def agregar_documento(self, texto: str, fuente: str = "conocimiento_base", sorteo: int = None) -> int:
        """Agrega un documento a la memoria vectorial con metadata de sorteo."""
        if not self.esta_disponible() or not texto:
            return 0
        
        fragmentos = self.fragmentar_texto(texto)
        agregados = 0
        
        for i, frag in enumerate(fragmentos):
            try:
                embedding = self.encoder.encode(frag).tolist()
                doc_id = f"{fuente}_{datetime.now().timestamp()}_{i}"
                
                metadata = {
                    "fuente": fuente, 
                    "timestamp": datetime.now().isoformat()
                }
                if sorteo is not None:
                    metadata["sorteo"] = sorteo
                
                self.collection.add(
                    ids=[doc_id],
                    embeddings=[embedding],
                    documents=[frag],
                    metadatas=[metadata]
                )
                agregados += 1
            except Exception as e:
                print(f"⚠️ Error agregando fragmento a ChromaDB: {e}")
        
        return agregados
    
    def buscar(self, consulta: str, top_k: int = TOP_K_RESULTS, sorteo_actual: int = None) -> List[Dict[str, Any]]:
        """
        Busca fragmentos relevantes por similitud semántica.
        
        Args:
            consulta: Texto de búsqueda
            top_k: Cantidad de resultados
            sorteo_actual: Si se provee, filtra resultados que NO sean de sorteos futuros
        """
        if not self.esta_disponible() or not consulta:
            return []
        
        try:
            embedding = self.encoder.encode(consulta).tolist()
            resultados = self.collection.query(
                query_embeddings=[embedding],
                n_results=top_k * 2  # Pedir más para filtrar después
            )
            
            docs = resultados.get('documents', [[]])[0]
            metadatas = resultados.get('metadatas', [[]])[0]
            ids = resultados.get('ids', [[]])[0]
            
            resultados_filtrados = []
            for doc, meta, doc_id in zip(docs, metadatas, ids):
                if not doc:
                    continue
                
                # Filtrar por sorteo si es necesario
                if sorteo_actual is not None:
                    sorteo_doc = meta.get("sorteo", 0)
                    if sorteo_doc >= sorteo_actual and sorteo_doc > 0:
                        continue  # Saltar documentos de sorteos futuros
                
                resultados_filtrados.append({
                    "id": doc_id,
                    "texto": doc,
                    "metadata": meta
                })
                
                if len(resultados_filtrados) >= top_k:
                    break
            
            return resultados_filtrados
            
        except Exception as e:
            print(f"⚠️ Error buscando en ChromaDB: {e}")
            return []
    
    def limpiar(self):
        """Elimina toda la memoria vectorial del agente."""
        if self.esta_disponible():
            try:
                self.client.delete_collection(self.agente_id)
                self.collection = self.client.create_collection(self.agente_id)
                print(f"✅ Memoria vectorial limpiada para {self.agente_id}")
            except Exception as e:
                print(f"⚠️ Error limpiando memoria vectorial: {e}")


def asegurar_carpeta(agente_id: str) -> Path:
    """Asegura que exista la carpeta del agente para memoria JSON."""
    carpeta = MEMORIA_BASE / agente_id
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta


def cargar_memoria(agente_id: str) -> dict:
    """Carga la memoria del agente (JSON básico)."""
    carpeta = asegurar_carpeta(agente_id)
    archivo = carpeta / "memoria.json"
    
    memoria_default = {
        "agente_id": agente_id,
        "creado": datetime.now().isoformat(),
        "ultima_actualizacion": datetime.now().isoformat(),
        "conocimiento_base": "",
        "patrones_aprendidos": [],
        "errores_cometidos": [],
        "aciertos_historicos": [],
        "notas_personales": ""
    }
    
    if archivo.exists():
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Asegurar que tiene todos los campos
                for key, default_value in memoria_default.items():
                    if key not in data:
                        data[key] = default_value
                return data
        except json.JSONDecodeError:
            print(f"⚠️ Error leyendo memoria de {agente_id}, usando valores por defecto")
            return memoria_default
    
    guardar_memoria(agente_id, memoria_default)
    return memoria_default


def guardar_memoria(agente_id: str, memoria: dict):
    """Guarda la memoria del agente (JSON básico)."""
    carpeta = asegurar_carpeta(agente_id)
    archivo = carpeta / "memoria.json"
    
    memoria["ultima_actualizacion"] = datetime.now().isoformat()
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(memoria, f, indent=2, ensure_ascii=False)


def actualizar_memoria(agente_id: str, nueva_info: str, tipo: str = "general", sorteo: int = None):
    """Actualiza la memoria con nueva información."""
    memoria = cargar_memoria(agente_id)
    
    if tipo == "patron":
        item = {
            "patron": nueva_info,
            "fecha": datetime.now().isoformat()
        }
        if sorteo:
            item["sorteo"] = sorteo
        memoria["patrones_aprendidos"].append(item)
    elif tipo == "error":
        item = {
            "error": nueva_info,
            "fecha": datetime.now().isoformat()
        }
        if sorteo:
            item["sorteo"] = sorteo
        memoria["errores_cometidos"].append(item)
    elif tipo == "acierto":
        item = {
            "acierto": nueva_info,
            "fecha": datetime.now().isoformat()
        }
        if sorteo:
            item["sorteo"] = sorteo
        memoria["aciertos_historicos"].append(item)
    else:
        # Limitar el conocimiento base a los últimos 5000 caracteres
        conocimiento_actual = memoria.get("conocimiento_base", "")
        if len(conocimiento_actual) + len(nueva_info) > 10000:
            # Si es muy grande, priorizar información nueva
            nuevo_conocimiento = conocimiento_actual[-5000:] + "\n" + nueva_info
            memoria["conocimiento_base"] = nuevo_conocimiento[-10000:]
        else:
            memoria["conocimiento_base"] += f"\n{nueva_info}"
    
    guardar_memoria(agente_id, memoria)
    
    # También indexar en memoria vectorial si está disponible
    try:
        mv = MemoriaVectorial(agente_id)
        if mv.esta_disponible():
            mv.agregar_documento(nueva_info, fuente=tipo, sorteo=sorteo)
    except Exception as e:
        print(f"⚠️ Error indexando en memoria vectorial: {e}")


def cargar_memoria_al_prompt(agente_id: str, consulta_actual: str = "", sorteo_actual: int = None) -> str:
    """
    Convierte la memoria en texto para inyectar al prompt.
    OPTIMIZADO: Usa búsqueda vectorial en lugar de inyectar TODO.
    
    Args:
        agente_id: ID del agente
        consulta_actual: La consulta del usuario para buscar fragmentos relevantes
        sorteo_actual: Número del sorteo actual para filtrar resultados futuros
    
    Returns:
        Texto con la memoria relevante para inyectar al prompt
    """
    memoria_json = cargar_memoria(agente_id)
    
    # Filtrar patrones y errores por sorteo si es necesario
    if sorteo_actual:
        patrones_recientes = [
            p for p in memoria_json.get('patrones_aprendidos', [])
            if p.get('sorteo', 0) < sorteo_actual or p.get('sorteo', 0) == 0
        ][-3:]
        errores_recientes = [
            e for e in memoria_json.get('errores_cometidos', [])
            if e.get('sorteo', 0) < sorteo_actual or e.get('sorteo', 0) == 0
        ][-3:]
    else:
        patrones_recientes = memoria_json.get('patrones_aprendidos', [])[-3:]
        errores_recientes = memoria_json.get('errores_cometidos', [])[-3:]
    
    # Siempre inyectar la información básica (pocos tokens)
    texto_base = f"""
[MI IDENTIDAD Y APRENDIZAJE BASE]

Agente: {agente_id}
Conocimiento base (resumen): {memoria_json.get('conocimiento_base', 'Ninguno aún')[:500]}

Patrones clave aprendidos ({len(memoria_json.get('patrones_aprendidos', []))}):
{json.dumps(patrones_recientes, indent=2, ensure_ascii=False)}

Errores que no debo repetir ({len(memoria_json.get('errores_cometidos', []))}):
{json.dumps(errores_recientes, indent=2, ensure_ascii=False)}

Notas personales:
{memoria_json.get('notas_personales', 'Ninguna')[:300]}
"""
    
    # Si hay una consulta específica, buscar fragmentos relevantes en memoria vectorial
    if consulta_actual and len(consulta_actual) > 10:
        try:
            mv = MemoriaVectorial(agente_id)
            if mv.esta_disponible():
                resultados = mv.buscar(consulta_actual, top_k=TOP_K_RESULTS, sorteo_actual=sorteo_actual)
                
                if resultados:
                    # Solo mostrar el fragmento más relevante para no saturar
                    texto_adicional = f"""
[MEMORIA RELEVANTE PARA TU CONSULTA (búsqueda semántica)]

{resultados[0]['texto'][:1000]}
"""
                    return texto_base + texto_adicional
        except Exception as e:
            print(f"⚠️ Error en búsqueda vectorial para {agente_id}: {e}")
    
    return texto_base


def cargar_memoria_completa_para_entrenamiento(agente_id: str, sorteo_actual: int = None) -> str:
    """
    Carga la memoria COMPLETA (solo para exportar/entrenar, NO para prompts diarios).
    Útil para generar papers o respaldos.
    
    Args:
        agente_id: ID del agente
        sorteo_actual: Si se provee, solo muestra resultados anteriores a este sorteo
    """
    memoria = cargar_memoria(agente_id)
    
    # Filtrar por sorteo si es necesario
    if sorteo_actual:
        patrones = [p for p in memoria.get('patrones_aprendidos', []) 
                   if p.get('sorteo', 0) < sorteo_actual or p.get('sorteo', 0) == 0]
        errores = [e for e in memoria.get('errores_cometidos', []) 
                  if e.get('sorteo', 0) < sorteo_actual or e.get('sorteo', 0) == 0]
        aciertos = [a for a in memoria.get('aciertos_historicos', []) 
                   if a.get('sorteo', 0) < sorteo_actual or a.get('sorteo', 0) == 0]
    else:
        patrones = memoria.get('patrones_aprendidos', [])
        errores = memoria.get('errores_cometidos', [])
        aciertos = memoria.get('aciertos_historicos', [])
    
    texto_completo = f"""
[MEMORIA COMPLETA DEL AGENTE {agente_id}]

=== CONOCIMIENTO BASE ===
{memoria.get('conocimiento_base', 'Ninguno aún')}

=== PATRONES APRENDIDOS ===
{json.dumps(patrones, indent=2, ensure_ascii=False)}

=== ERRORES COMETIDOS ===
{json.dumps(errores, indent=2, ensure_ascii=False)}

=== ACIERTOS HISTÓRICOS ===
{json.dumps(aciertos, indent=2, ensure_ascii=False)}

=== NOTAS PERSONALES ===
{memoria.get('notas_personales', 'Ninguna')}

=== METADATOS ===
Creado: {memoria.get('creado', 'desconocido')}
Última actualización: {memoria.get('ultima_actualizacion', 'desconocida')}
"""
    return texto_completo


def sincronizar_memoria_vectorial(agente_id: str, texto_base: Optional[str] = None, sorteo_limite: int = None):
    """
    Sincroniza toda la memoria JSON con la memoria vectorial.
    Útil para la primera carga o después de agregar mucho conocimiento.
    
    Args:
        agente_id: ID del agente
        texto_base: Texto opcional para indexar (si no se usa, se indexa la memoria existente)
        sorteo_limite: Si se provee, solo indexa elementos con sorteo < sorteo_limite
    """
    if not CHROMADB_AVAILABLE:
        print("⚠️ ChromaDB no disponible. Instalar con: pip install chromadb sentence-transformers")
        return
    
    memoria = cargar_memoria(agente_id)
    mv = MemoriaVectorial(agente_id)
    
    if not mv.esta_disponible():
        print(f"⚠️ No se pudo inicializar memoria vectorial para {agente_id}")
        return
    
    # Limpiar colección existente
    mv.limpiar()
    
    agregados = 0
    
    # Agregar conocimiento base
    if texto_base or memoria.get('conocimiento_base'):
        contenido = texto_base or memoria.get('conocimiento_base', '')
        if contenido:
            agregados += mv.agregar_documento(contenido, "conocimiento_base")
    
    # Agregar patrones aprendidos
    for patron in memoria.get('patrones_aprendidos', []):
        if isinstance(patron, dict) and 'patron' in patron:
            sorteo = patron.get('sorteo')
            if sorteo_limite is None or (sorteo and sorteo < sorteo_limite):
                agregados += mv.agregar_documento(patron['patron'], "patron", sorteo=sorteo)
        elif isinstance(patron, str):
            agregados += mv.agregar_documento(patron, "patron")
    
    # Agregar lecciones de errores
    for error in memoria.get('errores_cometidos', []):
        if isinstance(error, dict) and 'error' in error:
            sorteo = error.get('sorteo')
            if sorteo_limite is None or (sorteo and sorteo < sorteo_limite):
                agregados += mv.agregar_documento(f"ERROR A EVITAR: {error['error']}", "error", sorteo=sorteo)
        elif isinstance(error, str):
            agregados += mv.agregar_documento(f"ERROR A EVITAR: {error}", "error")
    
    print(f"✅ Memoria vectorial sincronizada para {agente_id}. {agregados} fragmentos indexados.")
    return agregados


def obtener_memoria_para_paper(agente_id: str, sorteo_actual: int = None) -> str:
    """
    Exporta la memoria completa en formato legible para generar papers.
    
    Args:
        agente_id: ID del agente
        sorteo_actual: Si se provee, solo exporta información anterior a este sorteo
    """
    return cargar_memoria_completa_para_entrenamiento(agente_id, sorteo_actual)


# Función de compatibilidad con el sistema existente
def cargar_memoria_al_prompt_legacy(agente_id: str) -> str:
    """
    Versión LEGACY que inyectaba TODO (NO RECOMENDADA).
    Se mantiene por compatibilidad pero no se usa.
    """
    memoria = cargar_memoria(agente_id)
    
    texto = f"""
[MI MEMORIA PERPETUA]

Conocimiento base que me cargaste:
{memoria.get('conocimiento_base', 'Ninguno aún')}

Patrones que he aprendido:
{json.dumps(memoria.get('patrones_aprendidos', []), indent=2)}

Errores que he cometido y no debo repetir:
{json.dumps(memoria.get('errores_cometidos', []), indent=2)}

Aciertos históricos:
{json.dumps(memoria.get('aciertos_historicos', []), indent=2)}

Notas personales:
{memoria.get('notas_personales', 'Ninguna')}
"""
    return texto
