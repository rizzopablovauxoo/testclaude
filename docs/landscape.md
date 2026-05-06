# Landscape — Odoo 19 Instance

## Contexto del sistema
Instancia Odoo 19 en entorno Odoo.sh. Los módulos custom se desarrollan en `/home/odoo/src/user/`. Odoo core está en `/home/odoo/src/odoo` (read-only).

## Entidades y modelos centrales
- `res.partner` — modelo base de contactos/partners
- `ir.ui.view` — vistas XML para formularios
- `res.partner.category` — categorías (Tags en la vista)

## Puntos de extensión
- Herencia de modelo: `_inherit = 'res.partner'`
- Herencia de vista: `inherit_id = ref('base.view_partner_form')`
- Validación con `@api.constrains('icq')`
- Posicionamiento en vista: XPath `//field[@name='category_id']` con `position="before"`

## Convenciones del proyecto
- Módulos custom en `/home/odoo/src/user/<module_name>/`
- Campos: `snake_case`, opcionales declarados sin `required=True`
- Validación de solo dígitos: `record.icq.isdigit()` + `ValidationError`
- Views: XML en `views/<model>_views.xml`
- Models: Python en `models/<model>.py` (o archivo específico como `models/res_partner.py`)

## Diferencias con documentación oficial
- Odoo 19: `@api.constrains` y `models.Constraint` reemplazan `_sql_constraints` (ver skill odoo-19.0)
- Verificaciones pendientes:
  - XML ID de vista form `res.partner` (asumida `base.view_partner_form`)
  - Nombre de campo Tags (asumido `category_id`)
  - Conflictos con otros módulos que hereden la vista form

## Lo que NO usamos
- SQL constraints (`_sql_constraints`) — reemplazado por `models.Constraint` en Odoo 19
- Creación de modelo nuevo — usamos `_inherit` sobre `res.partner`
