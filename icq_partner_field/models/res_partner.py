from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    icq = fields.Char(
        string="ICQ",
        size=9,
        help="ICQ number (up to 9 numeric digits, optional)"
    )
