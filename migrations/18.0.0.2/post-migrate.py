# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID

# Taxes de vente gardees : id -> (libelle, categorie UNECE, motif d'exoneration)
TAXES_CODES = {
    36: ("20% G", "tax_categ_s", None),
    49: ("20% S", "tax_categ_s", None),
    47: ("0% EX G", "tax_categ_g", "tax_vatex_eu_g"),
    58: ("0% EX S", "tax_categ_g", "tax_vatex_eu_g"),
    48: ("0% EU G", "tax_categ_k", "tax_vatex_eu_ic"),
    59: ("0% EU S", "tax_categ_k", "tax_vatex_eu_ic"),
}

# Taxes de vente archivees : id -> libelle
TAXES_ARCHIVEES = {
    46: "0% EXEMPT G",
    57: "0% EXEMPT S",
}


def migrate(cr, version):
    """Codes UNECE des taxes de vente et archivage des taxes inutilisees.

    La facturation electronique (account_invoice_en16931) controle toutes
    les taxes de vente actives a la validation de chaque facture : type
    UNECE, categorie et, pour les taxes a 0 %, motif d'exoneration (VATEX).

    Gardees, avec type VAT :
    - categorie S : 20% G et 20% S ;
    - export (G, VATEX-EU-G) et intracommunautaire (K, VATEX-EU-IC) :
      cibles des positions fiscales "Import/Export Hors Europe + DOM-TOM"
      et "Intra-EU B2B" (une taxe cible archivee est supprimee des
      factures au lieu d'etre remplacee).

    Archivees : 0% EXEMPT G et 0% EXEMPT S, sur aucune facture, aucun
    produit ni aucune cible de position fiscale.

    Ids et libelles controles en production (odoo18-couverture) le
    2026-10-18, verifies avant modification. Necessite
    l10n_fr_account_invoice_en16931 (champs de account_tax_unece) : a
    installer avant cette mise a jour.
    """
    env = api.Environment(cr, SUPERUSER_ID, {"lang": "en_US", "active_test": False})
    Tax = env["account.tax"]
    if "unece_categ_id" not in Tax._fields:
        raise Exception(
            "is_jura_couverture_18 0.2 : installer l10n_fr_account_invoice_en16931 "
            "avant de mettre a jour is_jura_couverture_18"
        )
    libelles = {tax_id: name for tax_id, (name, categ, vatex) in TAXES_CODES.items()}
    libelles.update(TAXES_ARCHIVEES)
    for tax_id, name in libelles.items():
        tax = Tax.browse(tax_id).exists()
        if not tax or tax.name != name or tax.type_tax_use != "sale":
            raise Exception(
                "is_jura_couverture_18 0.2 : taxe %s introuvable ou differente de %r" % (tax_id, name)
            )
    vat = env.ref("account_tax_unece.tax_type_vat")
    for tax_id, (name, categ, vatex) in TAXES_CODES.items():
        Tax.browse(tax_id).write({
            "unece_type_id": vat.id,
            "unece_categ_id": env.ref("account_tax_unece.%s" % categ).id,
            "unece_vatex_id": vatex and env.ref("account_tax_unece.%s" % vatex).id,
        })
    Tax.browse(list(TAXES_ARCHIVEES)).write({"active": False})
