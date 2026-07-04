"""Script para cargar sorteos desde JSON a la base de datos"""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "loto_plus.db"

# Buscar el JSON en múltiples ubicaciones
posibles_nombres = ["lotoplus_completo_3511_3885.json", "loto_plus_completo.json", "sorteos.json"]

JSON_PATH = None

# Buscar en C:\IA_CORE\ y subcarpetas
raiz = Path(__file__).parent.parent.parent
for archivo in raiz.rglob("*.json"):
    if archivo.name in posibles_nombres or "lotoplus" in archivo.name.lower():
        JSON_PATH = archivo
        print(f"OK JSON encontrado: {JSON_PATH}")
        break

if JSON_PATH is None:
    print("ERROR No se encontró el archivo JSON con sorteos")
    print("   Por favor, asegurate de que el archivo esté en C:\\IA_CORE\\")
    exit(1)


def cargar_sorteos():
    """Carga los sorteos desde el JSON a la base de datos"""

    # Leer JSON
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    sorteos = data["sorteos"]

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # Asegurar que la tabla tiene las columnas necesarias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sorteos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER UNIQUE NOT NULL,
            fecha TEXT,
            n1 INTEGER,
            n2 INTEGER,
            n3 INTEGER,
            n4 INTEGER,
            n5 INTEGER,
            plus INTEGER,
            es_entrenamiento BOOLEAN DEFAULT 0,
            es_validacion BOOLEAN DEFAULT 0,
            es_prueba_real BOOLEAN DEFAULT 0,
            desbloqueado BOOLEAN DEFAULT 0,
            resultado_conocido BOOLEAN DEFAULT 0
        )
    """)

    # Agregar columna es_prueba_real si no existe
    try:
        cursor.execute("ALTER TABLE sorteos ADD COLUMN es_prueba_real BOOLEAN DEFAULT 0")
    except sqlite3.OperationalError:
        pass  # Ya existe

    clasificados = {"entrenamiento": 0, "validacion": 0, "prueba_real": 0}

    for sorteo in sorteos:
        numero = sorteo["sorteo"]

        # Extraer números del Tradicional
        nums = sorteo["resultados"]["Tradicional"]["numeros"]
        n1, n2, n3, n4, n5 = nums[:5]
        plus = int(sorteo.get("numero_plus", 0))

        # Determinar tipo de sorteo
        if 3511 <= numero <= 3799:
            es_entrenamiento = 1
            es_validacion = 0
            es_prueba_real = 0
            desbloqueado = 1
            clasificados["entrenamiento"] += 1

        elif 3800 <= numero <= 3850:
            es_entrenamiento = 0
            es_validacion = 1
            es_prueba_real = 0
            desbloqueado = 0
            clasificados["validacion"] += 1

        elif 3851 <= numero <= 3885:
            es_entrenamiento = 0
            es_validacion = 0
            es_prueba_real = 1
            desbloqueado = 0
            clasificados["prueba_real"] += 1

        else:
            continue

        # Insertar o actualizar
        cursor.execute(
            """
            INSERT OR REPLACE INTO sorteos 
            (numero, fecha, n1, n2, n3, n4, n5, plus, 
             es_entrenamiento, es_validacion, es_prueba_real, desbloqueado, resultado_conocido)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                numero,
                sorteo.get("fecha", ""),
                n1,
                n2,
                n3,
                n4,
                n5,
                plus,
                es_entrenamiento,
                es_validacion,
                es_prueba_real,
                desbloqueado,
                1 if desbloqueado else 0,
            ),
        )

    conn.commit()
    conn.close()

    print(f"Carga completada:")
    print(f"   - Entrenamiento (3511-3799): {clasificados['entrenamiento']} sorteos")
    print(f"   - Validación ciega (3800-3850): {clasificados['validacion']} sorteos")
    print(f"   - Prueba real (3851-3885): {clasificados['prueba_real']} sorteos")
    print(f"   - Total: {sum(clasificados.values())} sorteos")


if __name__ == "__main__":
    cargar_sorteos()
