# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_objet = fields.Char(string="Objet du devis")

    @api.depends('name', 'is_objet')
    def _compute_display_name(self):
        for rec in self:
            if rec.is_objet:
                rec.display_name = f"{rec.is_objet} ({rec.name})"
            else:
                rec.display_name = rec.name
