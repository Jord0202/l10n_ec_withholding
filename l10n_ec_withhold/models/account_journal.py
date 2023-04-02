from odoo import _, api, fields, models

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    l10n_ec_withhold_type = fields.Selection(
        selection=[
            ('out_withhold', "Sales Withhold"),
            ('in_withhold', "Purchase Withhold")],
        string="Withhold Type",
    )

    l10n_ec_withhold_bool = fields.Boolean(
        string='use withholding?'
    )
