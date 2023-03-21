from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    l10n_ec_withhold_journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Withhold Journal",
        related="company_id.l10n_ec_withhold_journal_id",
        readonly=False,
    )
