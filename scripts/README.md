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

## generate_professional_profile_matrix.py

Genera `docs/PROFESSIONAL_PROFILE_AREA_NICHE_MATRIX.md` desde `catalogs/professional_profiles.json`.

**Proposito**: artefacto derivado para consultar cobertura perfil <-> area/nicho sin duplicar la fuente de verdad.

**Uso**:
```bash
python scripts/generate_professional_profile_matrix.py
```

**Nota**: La matriz generada no debe editarse como catalogo. Si cambian los perfiles, ejecutar el script y validar con `tests/test_professional_profile_matrix.py`.

## generate_domain_profile_catalog.py

Genera un `profile_catalog` derivado desde la Biblioteca Profesional Global sin modificar dominios reales.

**Proposito**: obtener candidatos trazables por area/nicho para preparar dominios futuros sin duplicar `catalogs/professional_profiles.json`.

**Uso**:
```bash
python scripts/generate_domain_profile_catalog.py --area marketing_publicidad --niche contenidos_redes --max-profiles 5
```

**Salida JSON opcional**:
```bash
python scripts/generate_domain_profile_catalog.py --area marketing_publicidad --niche contenidos_redes --output docs/example_profile_catalog.json
```

**Nota**: El script rechaza rutas dentro de `domains/`, no sobrescribe archivos existentes y no crea presets, papers ni agentes.
