# Active Context

Estado actual del proyecto. Cada feature cerrada agrega una entry. Las entries más recientes arriba.

---

## 2026-05-06 — Feature: ICQ field

Cerrada feature de agregar campo opcional `icq` (hasta 9 dígitos numéricos) al modelo `res.partner` de Odoo 19, visible en formulario antes de `category_id`.

Decisiones relevantes:
- Extensión de `res.partner` vía `_inherit` (patrón estándar Odoo).
- Validación de contenido/longitud con `@api.constrains`.
- Posicionamiento en vista usando XPath `//field[@name='category_id']` con `position="before"`.

Deuda técnica detectada:
- Docstring de tests obsoleto en `test_icq_field.py` (dice "RED phase").
- Placeholder "Test Writer" en campo `author` del `__manifest__.py`.

Próxima feature en cola: No hay.

<!-- Plantilla para nuevas entries (las nuevas van arriba):

## <YYYY-MM-DD> — Feature: <nombre corto>

Cerrada feature de <descripción de una línea>.

Decisiones relevantes:
- <decisión 1, con trade-off si aplica>

Deuda técnica detectada:
- <punto 1>

Próxima feature en cola: <si la sabe>.

-->

## <YYYY-MM-DD> — Bootstrap del proyecto

Memory Bank inicializado. Listos para arrancar la primera feature.

Pendientes para completar manualmente:
- `projectbrief.md`: secciones marcadas TODO.
- `systemPatterns.md`: convenciones técnicas existentes.
