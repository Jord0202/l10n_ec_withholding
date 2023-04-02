{
    "name": "Electronic Ecuadorian Localization",
    "summary": "Electronic data interchange adapted Ecuadorian localization",
    "category": "Account",
    "author": "Odoo Community Association (OCA), "
    "Carlos Lopez, Renan Nazate, Yazber Romero, Luis Romero, Jorge Quiguango",
    "website": "https://github.com/OCA/l10n-ecuador",
    "license": "AGPL-3",
    "version": "15.0.1.0.0",
    "depends": ["l10n_ec_base"],
    "external_dependencies": {
        "python": ["cryptography==36.0.0", "xmlsig==0.1.9", "xades==0.2.4", "zeep"]
    },
    "data": [
        #"security/ir.model.access.csv",
        #"data/account_chart_template_data.xml",
        "data/account_tax_group_data.xml",
        "data/l10n_latam.document.type.csv",
        #"data/account_tax_report_data.xml",
        #"data/account_tax_template_withhold_profit_data.xml",
        #"data/account_tax_template_withhold_vat_data.xml",
        "views/res_partner.xml",
        "views/account_move_view.xml",
        "views/account_tax_view.xml",
        "views/wizard_withhold.xml",
        
    ],
    "installable": True,
    "auto_install": False,
}
