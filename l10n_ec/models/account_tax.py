# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

TYPE_TAX_USE = [
    ('sale', 'Ventas'),
    ('purchase', 'Compras'),
    ('VAT Withhold', 'Retención de IVA'),
    ('Profit Withhold', 'Retención a la fuente'),
    ('none', 'Ninguno'),
]


class AccountTax(models.Model):

    _inherit = "account.tax"

    l10n_ec_code_base = fields.Char(
        string="Code base",
        help="Tax declaration code of the base amount prior to the calculation of the tax",
    )
    l10n_ec_code_applied = fields.Char(
        string="Code applied",
        help="Tax declaration code of the resulting amount after the calculation of the tax",
    )
    l10n_ec_code_ats = fields.Char(
        string="Code ATS",
        help="Tax Identification Code for the Simplified Transactional Annex",
    )
    
    type_tax_use = fields.Selection(TYPE_TAX_USE, string='Tax Type', required=True, default="sale",
        help="Determina dónde se puede seleccionar el impuesto. Nota: 'Ninguno' significa que un impuesto no se puede usar solo, sin embargo, aún se puede usar en un grupo. 'Ajuste' se utiliza para realizar el ajuste de impuestos.")    



class AccountTaxTemplate(models.Model):

    _inherit = "account.tax.template"

    def _get_tax_vals(self, company, tax_template_to_tax):
        vals = super(AccountTaxTemplate, self)._get_tax_vals(
            company, tax_template_to_tax
        )
        vals.update(
            {
                "l10n_ec_code_base": self.l10n_ec_code_base,
                "l10n_ec_code_applied": self.l10n_ec_code_applied,
                "l10n_ec_code_ats": self.l10n_ec_code_ats,
            }
        )
        return vals

    l10n_ec_code_base = fields.Char(
        string="Code base",
        help="Tax declaration code of the base amount prior to the calculation of the tax",
    )
    l10n_ec_code_applied = fields.Char(
        string="Code applied",
        help="Tax declaration code of the resulting amount after the calculation of the tax",
    )
    l10n_ec_code_ats = fields.Char(
        string="Code ATS",
        help="Tax Identification Code for the Simplified Transactional Annex",
    )
    
    type_tax_use = fields.Selection(TYPE_TAX_USE, string='Tax Type', required=True, default="sale",
        help="Determina dónde se puede seleccionar el impuesto. Nota: 'Ninguno' significa que un impuesto no se puede usar solo, sin embargo, aún se puede usar en un grupo. 'Ajuste' se utiliza para realizar el ajuste de impuestos.")    

    
