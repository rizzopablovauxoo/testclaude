---
feature_id: 001-icq-partner-field
feature_name: ICQ field for res.partner
created_at: 2026-05-06
approved_by: pendiente
approved_at: pendiente
---

# Spec: ICQ Field for res.partner

## Descripción funcional

Agregar un campo opcional `icq` al modelo `res.partner` de Odoo 19, que solo acepte dígitos numéricos con una longitud máxima de 9 caracteres. El campo debe ser visible en la vista de formulario de contactos, posicionado antes del campo `category_id` (Tags). Los ceros a la izquierda están permitidos y no se requiere unicidad del valor entre diferentes partners.

## Contrato (firma e invariantes)

**Firma:**

```python
# In models/res_partner.py (or similar file inheriting res.partner)
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    icq = fields.Char(
        string="ICQ",
        size=9,
        help="ICQ number (up to 9 numeric digits, optional)"
    )

    @api.constrains('icq')
    def _check_icq(self):
        for record in self:
            if record.icq:
                if not record.icq.isdigit():
                    raise ValidationError(
                        self.env._("ICQ must contain only numeric digits.")
                    )
                if len(record.icq) > 9:
                    raise ValidationError(
                        self.env._("ICQ must be at most 9 digits long.")
                    )
```

**Postcondiciones (numeradas y verificables):**

1. Si se guarda un registro de `res.partner` con `icq` vacío o False, el campo almacena un valor nulo (False).
2. Si se guarda un registro de `res.partner` con `icq` compuesto exclusivamente por dígitos numéricos y longitud ≤9, el campo almacena el valor exacto ingresado (incluyendo ceros a la izquierda).
3. Si se intenta guardar un registro de `res.partner` con `icq` que contiene caracteres no numéricos, se lanza una `ValidationError` con mensaje indicando que solo se permiten dígitos.
4. Si se intenta guardar un registro de `res.partner` con `icq` de longitud >9 caracteres, se lanza una `ValidationError` con mensaje indicando el límite de 9 dígitos.
5. Al renderizar la vista de formulario de `res.partner`, el campo `icq` está posicionado inmediatamente antes del campo `category_id` (Tags).

## Invariantes verificables

- ∀ registro `res.partner` válido: `record.icq` es False, o es una cadena de 1 a 9 caracteres donde cada carácter es un dígito numérico (0-9).
- ∀ par de registros `res.partner` válidos: No existe restricción de unicidad, por lo que pueden tener el mismo valor `icq`.

## Criterios de aceptación

- [ ] Test unitario para cada postcondición (1-5) pasa correctamente.
- [ ] Cobertura de líneas en el archivo de modelo de `res.partner` (ej. `models/res_partner.py`) ≥ 90%.
- [ ] Test de vista confirma que `icq` está presente en el formulario antes de `category_id`.
- [ ] No existen registros en la base de datos con valores `icq` inválidos tras aplicar las validaciones.

## Out of scope

- No se agrega el campo `icq` a vistas de lista (tree), kanban, o otros tipos de vista de `res.partner`.
- No se implementan permisos especiales para el campo `icq`; se rige por los permisos generales de escritura de `res.partner`.
- No se integra el campo `icq` con reportes, exportaciones de datos, o módulos externos.

## Notas de implementación (opcional)

- La validación de contenido (solo dígitos) se implementa mediante `@api.constrains` en lugar de `models.Constraint`, ya que `models.Constraint` es para restricciones a nivel base de datos y el campo es de tipo Char.
- El atributo `size=9` en `fields.Char` limita la longitud en el modelo, pero la validación de longitud se refuerza en el método `_check_icq` para consistencia.
- La vista hereda `base.view_partner_form` usando XPath: `<xpath expr="//field[@name='category_id']" position="before"><field name="icq"/></xpath>`.

## Contexto técnico

- Modelo base: `res.partner` (Odoo 19 standard model).
- Puntos de extensión: `_inherit = 'res.partner'` para el modelo, herencia de vista con `inherit_id = ref('base.view_partner_form')`.
- Validación: Uso de `@api.constrains` (Odoo 19 decorator) para validar contenido y longitud de `icq`.
- Vistas: XML en `views/res_partner_views.xml` (o similar) con posicionamiento vía XPath.
- Odoo 19: Reemplazo de `_sql_constraints` por `models.Constraint`, pero no aplica para esta feature ya que no se requieren restricciones SQL.

---
Status: Approved by Pablo Manuel Rizzo on 2026-05-06
