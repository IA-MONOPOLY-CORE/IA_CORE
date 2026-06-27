# Relevamiento de usos de ResponseScore

## Introducción
Este documento lista todos los lugares del código donde se usa o accede a la clase `ResponseScore` (o equivalente en `demo_generico`).

---

## 1. domains/loteria/scoring.py
- **Clase ResponseScore definida** (líneas 36-78) con soporte de acceso híbrido (atributo y dict)
- **Líneas 210-227**: `u_score_v2_1()` devuelve un `ResponseScore`
- **Líneas 248, 299-300**: `score_response()` devuelve un `ResponseScore`
- **Líneas 322-325, 334-337**: En `build_scores_summary()`: se accede a ambos tipos (dict y atributo) para compatibilidad
  * Línea 323: `s.score["total"]` (acceso dict)
  * Línea 325: `s.score.total` (acceso atributo)

---

## 2. core/supervisor.py
- **Líneas 913-916**: Acceso a score híbrido para compatibilidad
  * Línea 914: `step.score["total"]` (dict)
  * Línea 916: `step.score.total` (atributo)
- **Líneas 993-995**: Mismo patrón para obtener score total
  * Línea 993: `step.score["total"]` (dict)
  * Línea 995: `step.score.total` (atributo)

---

## 3. api.py
- **Líneas 161-166**: En `_serialize_result()`, manejo híbrido de score para compatibilidad
  * Línea 162: `step.score.total` (atributo)
  * Línea 166: `step.score["total"]` (dict)

---

## 4. tests/test_scoring.py
- **Líneas 54-57**: Prueba de acceso dict en step.score
  * Línea 54: `step.score["total"]`
  * Línea 55: `step.score["confidence"]`
  * Línea 56: `step.score["reasoning_quality"]`
  * Línea 57: `step.score["execution_quality"]`
- **Líneas 115-147**: Nueva prueba para validar acceso híbrido

---

## 5. domains/demo_generico/scoring_demo_generico.py
- **Clase ResponseScore definida** (líneas 8-10), independiente de la de lotería
- **Líneas 20,24,26**: Funciones devuelven esta clase
- **Línea35**: `build_scores_summary()` accede a `step.score.total` (atributo)

---

## Observaciones importantes
1. **Uso híbrido intencional en build_scores_summary (scoring.py) y supervisor.py**:
   - Estos lugares usan ambos tipos de acceso para ser compatibles tanto con diccionarios como con objetos ResponseScore
2. **NO hay dependencia de isinstance(score, dict) para diferenciar de ResponseScore**:
   - La lógica usa `isinstance(s.score, dict)` para chequear si es un dict, y `hasattr(score, 'total')` para chequear si es un objeto
   - Esto es seguro porque el ResponseScore tiene atributos, no es un dict
3. **tests/test_scoring.py usa ambos tipos de acceso en su prueba**:
   - Esto es correcto ya que la clase está diseñada para soportarlo

---

## Casos de uso mixto en una misma función
- **domains/loteria/scoring.py: build_scores_summary()**: usa `s.score["total"]` y `s.score.total` en el mismo bucle
- **core/supervisor.py: líneas 910-916 y 990-995**: mismo caso
- **api.py: _serialize_result()**: usa ambos métodos de acceso

---

## Nota sobre ResponseScore de demo_generico
Es una clase completamente separada, con atributos `total` y `detalles`, y no implementa el acceso híbrido.
