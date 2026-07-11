# Scripts de Mantenimiento

Esta carpeta contiene scripts de mantenimiento y auditoría manual para IA_CORE.

## audit_profile_preset_consistency.py

Script de auditoría manual para verificar consistencia entre profiles, presets, papers y agentes del dominio Lotería.

**Propósito**: Herramienta de diagnóstico manual para detectar inconsistencias en la cadena de trazabilidad operativa.

**Uso**:
```bash
python scripts/audit_profile_preset_consistency.py
```

**Nota**: Los tests oficiales de regresión están en `tests/test_profile_preset_consistency.py`. Este script es complementario, no reemplaza los tests automatizados.
