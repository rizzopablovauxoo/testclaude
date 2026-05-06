# Test Audit Report: 001-icq-partner-field

**Feature**: ICQ Field for res.partner
**Date**: 2026-05-06
**Auditor**: test-writer (AUDIT sub-stage 3.0)
**Spec status**: Approved by Pablo Manuel Rizzo on 2026-05-06

---

## 1. Resumen de comportamiento que cambia

Se agrega un campo **nuevo y opcional** `icq` al modelo `res.partner`. Este cambio:

- **NO modifica** el comportamiento existente de `res.partner`
- **NO altera** validaciones existentes
- **NO cambia** la API pública del modelo
- El campo acepta `False`/vacío o una cadena de hasta 9 dígitos numéricos (ceros a la izquierda permitidos)
- Se posiciona en la vista de formulario antes de `category_id` (Tags)

**Conclusión**: Es una adición puramente incremental sin efectos secundarios en la funcionalidad existente.

---

## 2. Tests modificados

**Ninguno.**

**Justificación**: El spec no justifica modificación de ningún test existente porque:
1. El campo `icq` es opcional y no tiene valores por defecto que afecten creaciones existentes
2. Ningún test existente de `res.partner` hace referencia al campo `icq` (no existe aún)
3. Las validaciones `@api.constrains('icq')` solo se ejecutan cuando se establece un valor en `icq`, no afectan a las creaciones/actualizaciones existentes sin el campo
4. La adición de un campo opcional no rompe la serialización ni deserialización de registros existentes

---

## 3. Tests nuevos a escribir

Basado en las 5 postcondiciones del spec (`docs/specs/001-icq-partner-field/spec.md`, líneas 47-53):

| # | Postcondición | Test nuevo | Descripción |
|---|---------------|------------|-------------|
| 1 | Si `icq` vacío/False → almacena False | `test_icq_field_empty_stores_null` | Verifica que crear/escribir partner con `icq=False` o `icq=''` almacene valor nulo |
| 2 | Si `icq` es numérico (≤9 dígitos) → almacena valor exacto | `test_icq_field_valid_numeric_stores_exact` | Verifica almacenamiento correcto de valores como `'123'`, `'012345678'`, `'0'` |
| 3 | Si `icq` tiene caracteres no numéricos → `ValidationError` | `test_icq_field_non_numeric_raises_validation_error` | Verifica que valores como `'abc'`, `'123x'`, `'12.34'` lancen `ValidationError` con mensaje correcto |
| 4 | Si `icq` tiene longitud >9 → `ValidationError` | `test_icq_field_too_long_raises_validation_error` | Verifica que valores de 10+ caracteres lancen `ValidationError` con mensaje correcto |
| 5 | Vista formulario: `icq` antes de `category_id` | `test_icq_field_position_in_form_view` | Verifica mediante inspección de archivo XML o `ir.ui.view` que `icq` está posicionado antes de `category_id` |

---

## 4. Tests untouched (explícitos)

Los siguientes tests en `/home/odoo/src/odoo/odoo/addons/base/tests/test_res_partner.py` **NO se tocan** (35 tests):

1. `test_archive_internal_partners`
2. `test_email_formatted`
3. `test_find_or_create`
4. `test_is_public`
5. `test_lang_computation_code`
6. `test_name_create`
7. `test_name_search` (primer ocurrencia)
8. `test_name_search_with_user`
9. `test_partner_merge_wizard_dst_partner_id`
10. `test_display_name_translation`
11. `test_main_user_id`
12. `test_address`
13. `test_address_first_contact_sync`
14. `test_address_get`
15. `test_address_parent_company_creation`
16. `test_commercial_partner_nullcompany`
17. `test_commercial_field_sync`
18. `test_commercial_field_sync_reset`
19. `test_company_dependent_commercial_sync`
20. `test_company_dependent_commercial_sync_falsy_fields`
21. `test_company_change_propagation`
22. `test_display_address_missing_key`
23. `test_display_name`
24. `test_accessibility_of_company_partner_from_branch`
25. `test_lang_computation_form_view`
26. `test_onchange_parent_sync_user`
27. `test_100_res_partner_recursion`
28. `test_101_res_partner_recursion`
29. `test_102_res_partner_recursion`
30. `test_103_res_partner_recursion`
31. `test_104_res_partner_recursion_indirect_cycle`
32. `test_105_res_partner_recursion`
33. `test_110_res_partner_recursion_multi_update`
34. `test_111_res_partner_recursion_infinite_loop`
35. `test_name_search` (segunda ocurrencia)

**Tests en otros módulos** (también untouched):
- `/home/odoo/src/odoo/addons/mail/tests/test_res_partner.py` - Todos los tests (19 tests documentados arriba en la lectura)
- `/home/odoo/src/odoo/addons/calendar/tests/test_res_partner.py`
- `/home/odoo/src/odoo/addons/crm/tests/test_res_partner.py`
- `/home/odoo/src/odoo/addons/hr_holidays/tests/test_res_partner.py`
- `/home/odoo/src/odoo/addons/l10n_it_edi/tests/test_res_partner.py`
- `/home/odoo/src/odoo/addons/web/tests/test_res_partner.py`
- Y cualquier otro test de `res.partner` en módulos de Odoo

**Justificación**: Ninguno de estos tests interactúa con el campo `icq`, y al ser un campo opcional, su mera existencia no altera el comportamiento de los tests existentes.

---

## 5. Regression risk assessment

**Nivel de riesgo**: **BAJO**

**Factores que contribuyen al bajo riesgo**:
1. **Campo opcional**: No tiene valor por defecto, no afecta creaciones existentes sin el campo
2. **Sin cambios en lógica existente**: No se modifican métodos existentes de `res.partner`
3. **Validaciones aisladas**: Los `@api.constrains('icq')` solo se disparan cuando se toca el campo `icq`
4. **Sin cambios en vistas existentes**: Se hereda la vista con XPath `position="before"`, no se sobreescribe
5. **Sin cambios en permisos**: El campo usa los permisos generales de `res.partner`
6. **Sin cambios en base de datos**: No hay migración de datos, el campo acepta NULL

**Posibles riesgos marginales** (mitigados):
- Si algún test existente crea un partner con todos los campos posibles y el campo `icq` aparece inesperadamente en respuestas API... pero el spec no incluye exposición en list views, así que esto no aplica.

---

## 6. Conclusión del audit

- **Tests a modificar**: 0
- **Tests untouched**: 35+ (explícitamente listados arriba)
- **Tests nuevos a escribir**: 5 (uno por postcondición)
- **Regression risk**: Bajo
- **Recomendación**: Proceder a fase RED (escribir tests que fallen inicialmente)

---

**Firma del auditor**: test-writer (AUDIT)
**Fecha**: 2026-05-06
**Estado**: Pendiente de aprobación humana
