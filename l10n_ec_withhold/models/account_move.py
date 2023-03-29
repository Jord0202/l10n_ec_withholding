import json
import logging
import re
from xml.etree.ElementTree import SubElement

from lxml import etree
#from ..models import modules_mapping

from odoo import _, api, fields, models, tools
from odoo.tools.safe_eval import safe_eval


_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_ec_withhold_ids = fields.Integer(
        comodel_name="l10n_ec.withhold",
        string="Withhold",
        readonly=True,
        store=True
    )

    def action_create_sale_withhold_wizard(self):
        self.ensure_one()
        action = self.env.ref("l10n_ec_withhold.l10n_ec_withhold_sales_wizard_window").read()[0]
        action["views"] = [(self.env.ref("l10n_ec_withhold.l10n_ec_form_sale_withhold").id, "form")]
        ctx = safe_eval(action["context"])
        ctx.pop("default_type", False)
        ctx.update(
            {
                "default_partner_id": self.partner_id.id,
                "default_invoice_id": self.id,
                "default_issue_date": self.invoice_date,
            }
        )
        action["context"] = ctx
        return action

    def action_show_l10n_ec_withholds(self):
        self.ensure_one()
        action = self.env.ref("l10n_ec_withhold.l10n_ec_withhold_sales_act_window").read()[0]
        action["views"] = [(self.env.ref("l10n_ec_withhold.l10n_ec_withhold_form_view").id, "form")]
        action['res_id'] = self.l10n_ec_withhold_ids
        return action
    








"""    def create_withhold_customer(self):
        self.ensure_one()
        action = self.env.ref("l10n_ec_withhold.l10n_ec_withhold_sales_act_window").read()[0]
        action["views"] = [(self.env.ref("l10n_ec_withhold.l10n_ec_withhold_form_view").id, "form")]
        ctx = safe_eval(action["context"])
        ctx.pop("default_type", False)
        ctx.update(
            {
                "default_partner_id": self.partner_id.id,
                "default_invoice_id": self.id,
                "withhold_type": "sale",
                "default_issue_date": self.invoice_date,
                "default_l10n_ec_is_create_from_invoice": True,
            }
        )
        action["context"] = ctx
        return action
"""