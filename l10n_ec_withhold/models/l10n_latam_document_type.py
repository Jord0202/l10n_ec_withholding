from odoo import fields, models, _
from odoo.exceptions import UserError
import re


class L10nLatamDocumentType(models.Model):
    _inherit = "l10n_latam.document.type"

    internal_type = fields.Selection(
        selection_add=[
            ("withhold", "Withhold"),
        ]
    )