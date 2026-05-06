from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError


class TestICQField(TransactionCase):
    """Tests for ICQ field on res.partner - RED phase (implementation not done yet)"""

    def test_postcondition_1_icq_empty_stores_null(self):
        """Postcondition 1: Si icq vacío/False → almacena False"""
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'icq': False,
        })
        self.assertFalse(partner.icq, "icq=False should store False/null")

        partner2 = self.env['res.partner'].create({
            'name': 'Test Partner 2',
            'icq': '',
        })
        self.assertFalse(partner2.icq, "icq='' should store False/null")

    def test_postcondition_2_icq_valid_numeric_stores_exact(self):
        """Postcondition 2: Si icq es numérico (≤9 dígitos) → almacena valor exacto"""
        test_cases = [
            ('123', '123'),
            ('012345678', '012345678'),
            ('0', '0'),
        ]
        for icq_input, expected in test_cases:
            with self.subTest(icq=icq_input):
                partner = self.env['res.partner'].create({
                    'name': 'Test Partner',
                    'icq': icq_input,
                })
                self.assertEqual(partner.icq, expected,
                                 f"icq='{icq_input}' should store '{expected}'")

    def test_postcondition_3_icq_non_numeric_raises_error(self):
        """Postcondition 3: Si icq tiene caracteres no numéricos → ValidationError"""
        invalid_values = ['abc', '123x', '12.34', '12 34']
        for icq_input in invalid_values:
            with self.subTest(icq=icq_input):
                with self.assertRaises(ValidationError,
                                     msg=f"icq='{icq_input}' should raise ValidationError"):
                    self.env['res.partner'].create({
                        'name': 'Test Partner',
                        'icq': icq_input,
                    })

    def test_postcondition_4_icq_too_long_raises_error(self):
        """Postcondition 4: Si icq tiene longitud >9 → ValidationError"""
        with self.assertRaises(ValidationError,
                              msg="icq with 10+ digits should raise ValidationError"):
            self.env['res.partner'].create({
                'name': 'Test Partner',
                'icq': '1234567890',  # 10 digits
            })

    def test_postcondition_5_icq_position_in_form_view(self):
        """Postcondition 5: icq antes de category_id en form view"""
        # Get the inherited view
        view = self.env.ref('icq_partner_field.view_partner_form_inherit_icq')
        arch = view.arch
        # Check that icq field is positioned before category_id
        icq_pos = arch.find('icq')
        category_pos = arch.find('category_id')
        self.assertNotEqual(icq_pos, -1, "icq field should be in the view")
        self.assertNotEqual(category_pos, -1, "category_id should be in the view")
        self.assertLess(icq_pos, category_pos,
                         "icq should appear before category_id in the view")
