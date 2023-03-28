from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from ast import literal_eval
from odoo.tools.safe_eval import safe_eval as eval
from dateutil.relativedelta import relativedelta
import datetime
from datetime import date
import logging
_logger = logging.getLogger(__name__)

TYPE_TAX_USE = [
    ('sale', 'Ventas'),
    ('purchase', 'Compras'),
    ('VAT Withhold', 'Retención de IVA'),
    ('Profit Withhold', 'Retención a la fuente'),
    ('none', 'Ninguno'),
]


class AccountTaxTemplate(models.Model):
    _inherit = "account.tax.template"

    def create_or_update_account_taxes(self):
        """This method creates or updates account taxes based on the tax templates"""
        for tax_template in self:
            tax_vals = tax_template._get_tax_vals(self.env.company, {})
            tax = self.env['account.tax'].search([('id', '=', tax_template.tax_id.id)])
            if not tax:
                tax = self.env['account.tax'].create(tax_vals)
            else:
                tax.write(tax_vals)
                tax.name = tax_template.name

    def post_init_hook(self):
        self.create_or_update_account_taxes()
    
    type_tax_use = fields.Selection(TYPE_TAX_USE, string='Tax Type', required=True, default="sale",
        help="Determina dónde se puede seleccionar el impuesto. Nota: 'Ninguno' significa que un impuesto no se puede usar solo, sin embargo, aún se puede usar en un grupo. 'Ajuste' se utiliza para realizar el ajuste de impuestos.")    

class AccountTax(models.Model):
    _inherit = "account.tax"

    type_tax_use = fields.Selection(TYPE_TAX_USE, string='Tax Type', required=True, default="sale",
        help="Determina dónde se puede seleccionar el impuesto. Nota: 'Ninguno' significa que un impuesto no se puede usar solo, sin embargo, aún se puede usar en un grupo. 'Ajuste' se utiliza para realizar el ajuste de impuestos.")