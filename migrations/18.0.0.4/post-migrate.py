# -*- coding: utf-8 -*-
import logging

from odoo import api, SUPERUSER_ID
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Champ is_siren remplace par le champ standard siren (l10n_fr_siret).

    is_siren (libelle "SIREN", calcule depuis le SIRET) faisait doublon avec
    siren de l10n_fr_siret, que la facturation electronique utilise pour le
    XML Factur-X. La colonne is_siren existe encore a ce stade : sa valeur
    est copiee dans siren quand siren est vide. Ecriture par l'ORM pour
    recalculer le SIRET et passer le controle de l10n_fr_siret (9 chiffres,
    cle, coherence avec le N° TVA) ; une valeur refusee est laissee de cote
    et signalee dans le journal, a corriger a la main.

    En production (odoo18-couverture) le 2026-10-18 : 4 partenaires avec
    is_siren et sans siren, dont 1 valeur tronquee ("894 279").
    """
    cr.execute("""
        select id, is_siren from res_partner
        where coalesce(is_siren, '') <> '' and coalesce(siren, '') = ''
    """)
    lignes = cr.fetchall()
    env = api.Environment(cr, SUPERUSER_ID, {"active_test": False})
    for partner_id, is_siren in lignes:
        partner = env["res.partner"].browse(partner_id)
        try:
            with cr.savepoint():
                partner.write({"siren": is_siren})
            _logger.info("is_jura_couverture_18 0.4 : SIREN %s copie sur %s", is_siren, partner.display_name)
        except ValidationError as err:
            _logger.warning(
                "is_jura_couverture_18 0.4 : SIREN %r non copie sur %s (id %s) : %s",
                is_siren, partner.display_name, partner_id, err,
            )
