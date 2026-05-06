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
