# -*- coding: utf-8 -*-
from odoo import fields, models, api  
from markupsafe import Markup


class IsProvenanceClient(models.Model):
    _name = 'is.provenance.client'
    _description = "Provenance client"
    _order = 'name'

    name = fields.Char("Nom", required=True)


class crm_lead(models.Model):
    _inherit = "crm.lead"
    
    is_provenance_client_id = fields.Many2one('is.provenance.client', string="Provenance client", tracking=True)
    is_adresse      = fields.Char("Adresse", size=60, tracking=True, required=False)
    is_localisation = fields.Char("Localisation", tracking=True)
    is_date_changement_etat = fields.Datetime("Date de dernier changement d'état", readonly=False, tracking=True)
    is_memoire_technique_ids = fields.Many2many(
        'ir.attachment',
        'crm_lead_memoire_technique_rel',
        'lead_id',
        'attachment_id',
        string="Mémoire technique",
    )
    is_etude_ids = fields.Many2many(
        'ir.attachment',
        'crm_lead_etude_rel',
        'lead_id',
        'attachment_id',
        string="Etude",
    )

    def write(self, vals):
        # Mettre à jour la date de changement d'état si stage_id est modifié
        if 'stage_id' in vals:
            vals['is_date_changement_etat'] = fields.Datetime.now()
        return super(crm_lead, self).write(vals)
