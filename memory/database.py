"""Base de datos para Loto Plus - Walk-forward validation"""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent / "loto_plus.db"


def init_db():
    """Inicializa la base de datos con todas las tablas necesarias."""
    with get_db() as conn:
        conn.executescript("""
            -- Sorteos históricos y de validación
            CREATE TABLE IF NOT EXISTS sorteos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero INTEGER UNIQUE NOT NULL,
                fecha TEXT NOT NULL,
                n1 INTEGER, n2 INTEGER, n3 INTEGER, n4 INTEGER, n5 INTEGER,
                plus INTEGER,
                es_entrenamiento BOOLEAN DEFAULT 1,
                es_validacion BOOLEAN DEFAULT 0,
                es_prueba_real BOOLEAN DEFAULT 0,
                desbloqueado BOOLEAN DEFAULT 0,
                resultado_conocido BOOLEAN DEFAULT 0
            );
            
            -- Debates por sorteo
            CREATE TABLE IF NOT EXISTS debates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sorteo_id INTEGER NOT NULL,
                sorteo_numero INTEGER NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                prediccion_n1 INTEGER,
                prediccion_n2 INTEGER,
                prediccion_n3 INTEGER,
                prediccion_n4 INTEGER,
                prediccion_n5 INTEGER,
                prediccion_plus INTEGER,
                u_score REAL,
                u_score_tentativo REAL,
                ver REAL,
                evf REAL,
                contradiccion REAL,
                acuerdo REAL,
                duracion_segundos REAL,
                created_at TEXT,
                finalized_at TEXT,
                FOREIGN KEY(sorteo_id) REFERENCES sorteos(id)
            );
            
            -- Intervenciones de agentes por debate
            CREATE TABLE IF NOT EXISTS intervenciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                debate_id INTEGER NOT NULL,
                sorteo_numero INTEGER NOT NULL,
                agente TEXT NOT NULL,
                contenido TEXT,
                orden INTEGER,
                timestamp TEXT,
                FOREIGN KEY(debate_id) REFERENCES debates(id)
            );
            
            -- Métricas acumuladas walk-forward
            CREATE TABLE IF NOT EXISTS metricas_acumuladas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sorteo_numero INTEGER NOT NULL,
                u_score_acumulado REAL,
                ver_acumulado REAL,
                evf_acumulado REAL,
                drawdown_actual REAL,
                regimen_detectado TEXT,
                regimen_acertado BOOLEAN,
                error_absoluto REAL,
                v19_sigue_vivo BOOLEAN,
                updated_at TEXT
            );
            
            -- Configuración del sistema
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            );
        """)
        
        # Agregar columna es_prueba_real si no existe
        try:
            conn.execute("ALTER TABLE sorteos ADD COLUMN es_prueba_real BOOLEAN DEFAULT 0")
        except sqlite3.OperationalError:
            pass
        
        # Insertar config inicial si no existe
        cur = conn.execute("SELECT COUNT(*) FROM config WHERE key = 'current_sorteo'")
        if cur.fetchone()[0] == 0:
            conn.execute("""
                INSERT INTO config (key, value, updated_at) 
                VALUES ('current_sorteo', '3800', ?)
            """, (datetime.now().isoformat(),))
        
        conn.execute("""
            INSERT OR IGNORE INTO config (key, value, updated_at)
            VALUES ('v19_alive', 'true', ?)
        """, (datetime.now().isoformat(),))


@contextmanager
def get_db():
    """Context manager para conexión a DB con timeout para evitar bloqueos."""
    conn = sqlite3.connect(str(DB_PATH), timeout=20.0)  # Increased timeout
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Error en DB: {e}")
        raise
    finally:
        conn.close()


# ============= FUNCIONES PARA SORTEOS =============

def cargar_sorteos_desde_json(json_path: Path):
    """Carga sorteos desde archivo JSON a la base de datos."""
    with open(json_path, 'r', encoding='utf-8') as f:
        sorteos = json.load(f)
    
    with get_db() as conn:
        for s in sorteos:
            conn.execute("""
                INSERT OR IGNORE INTO sorteos 
                (numero, fecha, n1, n2, n3, n4, n5, plus, es_entrenamiento, es_validacion, es_prueba_real, desbloqueado, resultado_conocido)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                s['numero'], s['fecha'], s['n1'], s['n2'], s['n3'], s['n4'], s['n5'],
                s.get('plus', 0),
                s.get('es_entrenamiento', True),
                s.get('es_validacion', False),
                s.get('es_prueba_real', False),
                s.get('desbloqueado', False),
                s.get('resultado_conocido', False)
            ))


def get_sorteo_actual() -> int:
    """Obtiene el número del sorteo actual (el próximo a analizar)."""
    with get_db() as conn:
        cur = conn.execute("SELECT value FROM config WHERE key = 'current_sorteo'")
        row = cur.fetchone()
        return int(row['value']) if row else 3800


def set_sorteo_actual(numero: int):
    """Actualiza el sorteo actual usando conexión independiente."""
    conn = sqlite3.connect(str(DB_PATH), timeout=10.0)
    try:
        conn.execute("""
            UPDATE config SET value = ?, updated_at = ? WHERE key = 'current_sorteo'
        """, (str(numero), datetime.now().isoformat()))
        conn.commit()
    finally:
        conn.close()


def get_sorteo_by_numero(numero: int) -> Optional[dict]:
    """Obtiene un sorteo por su número."""
    with get_db() as conn:
        cur = conn.execute("SELECT * FROM sorteos WHERE numero = ?", (numero,))
        row = cur.fetchone()
        return dict(row) if row else None


def desbloquear_siguiente_sorteo(sorteo_actual_numero: int) -> bool:
    """
    Desbloquea el siguiente sorteo para análisis.
    Usa conexión independiente para evitar bloqueos.
    """
    siguiente = sorteo_actual_numero + 1
    conn = sqlite3.connect(str(DB_PATH), timeout=10.0)
    try:
        # Verificar que existe el siguiente
        cur = conn.execute("SELECT id FROM sorteos WHERE numero = ?", (siguiente,))
        if not cur.fetchone():
            return False
        
        conn.execute("UPDATE sorteos SET desbloqueado = 1 WHERE numero = ?", (siguiente,))
        conn.execute("""
            UPDATE config SET value = ?, updated_at = ? WHERE key = 'current_sorteo'
        """, (str(siguiente), datetime.now().isoformat()))
        conn.commit()
        logger.info(f"Sorteo {siguiente} desbloqueado correctamente")
        return True
    except Exception as e:
        logger.warning(f"No se pudo desbloquear siguiente sorteo: {e}")
        return False
    finally:
        conn.close()


# ============= FUNCIONES PARA DEBATES =============

def crear_debate(sorteo_numero: int, estado: str = 'pendiente') -> int:
    """Crea un nuevo debate para un sorteo."""
    with get_db() as conn:
        # Obtener sorteo_id
        cur = conn.execute("SELECT id FROM sorteos WHERE numero = ?", (sorteo_numero,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Sorteo {sorteo_numero} no encontrado")
        sorteo_id = row['id']
        
        cur = conn.execute("""
            INSERT INTO debates (sorteo_id, sorteo_numero, estado, created_at)
            VALUES (?, ?, ?, ?)
        """, (sorteo_id, sorteo_numero, estado, datetime.now().isoformat()))
        
        return cur.lastrowid


def guardar_intervencion(debate_id: int, sorteo_numero: int, agente: str, contenido: str, orden: int):
    """Guarda una intervención de un agente en un debate."""
    with get_db() as conn:
        conn.execute("""
            INSERT INTO intervenciones (debate_id, sorteo_numero, agente, contenido, orden, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (debate_id, sorteo_numero, agente, contenido, orden, datetime.now().isoformat()))


def obtener_intervenciones(debate_id: int) -> dict:
    """Obtiene todas las intervenciones de un debate, indexadas por agente."""
    with get_db() as conn:
        cur = conn.execute("""
            SELECT agente, contenido, orden FROM intervenciones 
            WHERE debate_id = ? 
            ORDER BY orden
        """, (debate_id,))
        
        intervenciones = {}
        for row in cur.fetchall():
            intervenciones[row['agente']] = row['contenido']
        return intervenciones


def actualizar_debate_con_consenso(
    debate_id: int,
    prediccion: dict,
    contradiccion: float,
    u_score_tentativo: float,
    estado: str = 'consenso'
):
    """Actualiza un debate con la predicción y métricas de consenso."""
    with get_db() as conn:
        conn.execute("""
            UPDATE debates 
            SET prediccion_n1 = ?, prediccion_n2 = ?, prediccion_n3 = ?,
                prediccion_n4 = ?, prediccion_n5 = ?, prediccion_plus = ?,
                contradiccion = ?, u_score_tentativo = ?, estado = ?, finalized_at = ?
            WHERE id = ?
        """, (
            prediccion.get('n1'), prediccion.get('n2'), prediccion.get('n3'),
            prediccion.get('n4'), prediccion.get('n5'), prediccion.get('plus'),
            contradiccion, u_score_tentativo, estado, datetime.now().isoformat(),
            debate_id
        ))


def actualizar_debate_con_resultado(debate_id: int, resultado: dict, u_score: float, acuerdo: float):
    """Actualiza un debate con el resultado real del sorteo."""
    with get_db() as conn:
        conn.execute("""
            UPDATE debates 
            SET u_score = ?, acuerdo = ?, estado = 'finalizado'
            WHERE id = ?
        """, (u_score, acuerdo, debate_id))
        
        # Marcar sorteo como resultado conocido
        conn.execute("""
            UPDATE sorteos SET resultado_conocido = 1 
            WHERE numero = (SELECT sorteo_numero FROM debates WHERE id = ?)
        """, (debate_id,))


# ============= FUNCIONES PARA MÉTRICAS =============

def guardar_metrica_acumulada(sorteo_numero: int, metricas: dict):
    """Guarda métricas acumuladas después de cada sorteo."""
    with get_db() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO metricas_acumuladas 
            (sorteo_numero, u_score_acumulado, ver_acumulado, evf_acumulado, 
             drawdown_actual, regimen_detectado, regimen_acertado, 
             error_absoluto, v19_sigue_vivo, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sorteo_numero,
            metricas.get('u_score_acumulado'),
            metricas.get('ver_acumulado'),
            metricas.get('evf_acumulado'),
            metricas.get('drawdown_actual'),
            metricas.get('regimen_detectado'),
            metricas.get('regimen_acertado'),
            metricas.get('error_absoluto'),
            metricas.get('v19_sigue_vivo', True),
            datetime.now().isoformat()
        ))


def get_v19_status() -> bool:
    """Retorna True si V19 sigue vivo."""
    with get_db() as conn:
        cur = conn.execute("SELECT value FROM config WHERE key = 'v19_alive'")
        row = cur.fetchone()
        return row['value'].lower() == 'true' if row else True


def set_v19_status(alive: bool):
    """Actualiza el estado de V19."""
    with get_db() as conn:
        conn.execute("""
            UPDATE config SET value = ?, updated_at = ? WHERE key = 'v19_alive'
        """, ('true' if alive else 'false', datetime.now().isoformat()))
