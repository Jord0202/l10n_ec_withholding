from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    
    l10n_ec_withhold_journal_id = fields.Many2one(
        comodel_name="account.journal", string="Withhold Journal", required=False
    )