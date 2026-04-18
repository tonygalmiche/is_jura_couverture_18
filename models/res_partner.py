# -*- coding: utf-8 -*-
from odoo import api, fields, models


class IsFormeJuridique(models.Model):
    _name = 'is.forme.juridique'
    _description = 'Forme juridique'
    _order = 'name'

    name = fields.Char(string='Nom', required=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_forme_juridique_id = fields.Many2one('is.forme.juridique', string="Forme juridique")
    is_capital_social = fields.Float(string="Capital social (€)")
    is_lieu_rcs = fields.Char(string="Lieu d'immatriculation RCS")
    is_code_naf = fields.Char(string="Code NAF")
    is_siren = fields.Char(
        string="SIREN",
        size=9,
        compute='_compute_is_siren',
        store=True,
        readonly=False,
        help="Numéro SIREN (9 chiffres). Calculé automatiquement depuis le SIRET si renseigné.",
    )

    @api.depends('siret')
    def _compute_is_siren(self):
        for partner in self:
            if partner.siret and len(partner.siret) >= 9:
                partner.is_siren = partner.siret[:9]
            elif not partner.is_siren:
                partner.is_siren = False

    def action_open_contact(self):
        """Ouvrir la fiche du contact"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }
