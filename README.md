# Proyecto Demo CDAD en Odoo.sh

Este es el **primer desarrollo completo** utilizando la metodología **CDAD (Contract-Driven AI Development)** dentro del entorno Odoo.sh, orquestado por IA y ejecutado mediante subagentes especializados.

## Metodología Aplicada

Ciclo completo de 5 etapas ejecutado rigurosamente:

1. **Descubrimiento**: Mapeo de `res.partner` y APIs de Odoo 19 vía subagente `architect`.
2. **Especificación**: Borrador de `spec.md` con 5 postcondiciones numeradas, aprobado por humano (Pablo Manuel Rizzo).
3. **TDD Anti-trampa**:
   - Subagente `test-writer`: Auditoría de tests existentes + escritura de 5 tests (fase RED).
   - Subagente `implementer`: Código mínimo para pasar tests (fase GREEN).
   - Correcciones iterativas: validación `@api.constrains`, ajuste de `size=9`, posicionamiento XPath en vista.
4. **Review de dos capas**: Subagente `reviewer` detectó 2 bloqueantes iniciales, resueltos en fase GREEN (resultado final: 0 bloqueantes).
5. **Merge + Memory Bank**: Subagente `scribe` generó borradores de `activeContext.md`, `progress.md`.

## Aprendizajes Clave

### 1. Aislamiento de Subagentes Crítico
- El `test-writer` creó implementación prematura en fase RED (violación de CDAD). Corregido eliminando el código antes de ejecutar tests.
- Los subagentes deben respetar sus permisos estrictos (test-writer: solo tests, implementer: solo código).

### 2. Fase RED Debe Fallar Siempre
- Tests 1 y 2 pasaron inicialmente porque el campo `icq` ya existía. Esto invalidaba la fase RED.
- Verificación empírica obligatoria: `odoo-bin --test-tags` para confirmar 0 failed antes de avanzar.

### 3. Conflictos Odoo 19: `size=9` vs `@api.constrains`
- `fields.Char(size=9)` trunca valores en BD antes de que se ejecute la validación Python.
- Solución: combinar `size=9` (límite BD) con validación `@api.constrains` para consistencia.

### 4. Posicionamiento en Vistas XML
- XPath `//field[@name='category_id']` puede apuntar al campo equivocado si hay múltiples en la vista base.
- Requiere inspección de `base.view_partner_form` vía `psql` para ajustar posición.

### 5. Documentación como Primera Clase
- Memory Bank (`docs/`) es fundamental para persistir contexto entre sesiones efímeras de Odoo.sh.
- `odoosh-push` es obligatorio para persistir cambios (entorno efímero).

## Estructura del Proyecto

```
├── icq_partner_field/          # Módulo Odoo 19
│   ├── models/res_partner.py    # Campo icq + validación
│   ├── views/res_partner_views.xml  # Herencia de vista
│   └── tests/test_icq_field.py # 5 tests (postcondiciones)
├── docs/                       # Memory Bank CDAD
│   ├── specs/001-icq-partner-field/
│   │   ├── spec.md             # Spec aprobado
│   │   ├── test-audit.md      # Auditoría de tests
│   │   └── review.md          # Reporte de revisión
│   ├── activeContext.md        # Entrada de feature cerrada
│   ├── progress.md             # Estado de features
│   └── landscape.md           # Mapeo técnico inicial
└── README.md                   # Este archivo
```

## Comandos Útiles

- Probar módulo: `odoo-bin -u icq_partner_field --test-tags /icq_partner_field --stop-after-init --no-http`
- Verificar vista base: `psql -c "SELECT arch FROM ir_ui_view WHERE xml_id='base.view_partner_form';"`
- Persistir cambios: `odoosh-push`

---

**Orquestado por**: CDAD Cycle Skill + Odoo 19 Skill  
**Autoría humana**: Pablo Manuel Rizzo  
**Fecha**: 2026-05-06  
**Entorno**: Odoo.sh (Rama de Desarrollo)
