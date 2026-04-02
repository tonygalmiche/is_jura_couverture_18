# -*- coding: utf-8 -*-
{
    "name"     : "Module Odoo 18 pour Jura Couverture",
    "version"  : "0.1",
    "author"   : "InfoSaône",
    "category" : "InfoSaône",
    "description": """
Module Odoo 18 pour Jura Couverture
===================================================
""",
    "maintainer" : "InfoSaône",
    "website"    : "http://www.infosaone.com",
    "depends"    : [
        "base",
        "purchase",
        "product",
        "project",
        "crm",
        "l10n_fr_account",
        "web_chatter_position",
    ],
    "data" : [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/report_layout_view.xml",
        "views/report_invoice_view.xml",
        "views/res_partner_view.xml",
        "views/product_view.xml",
        "views/crm_lead_view.xml",
        "views/account_move_view.xml",
        "views/menu.xml"
    ],
    'assets': {
        'web.assets_backend': [
            'is_jura_couverture_18/static/src/scss/styles.scss',
            
        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
