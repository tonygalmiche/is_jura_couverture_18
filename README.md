# Module Jura Couverture 18

## Créer un nouveau mode de règlement

Les modes de règlement (affichés sur les factures via le champ **"Mode de paiement"**) sont liés aux journaux comptables. Ils ne peuvent pas être créés directement depuis un menu dédié.

**Procédure :**

1. Aller dans **Comptabilité → Configuration → Journaux**
2. Ouvrir le journal souhaité (ex : **Banque**)
3. Onglet **Paramètres avancés**
4. Section **Modes de paiement entrants** → cliquer **Ajouter une ligne**
5. Saisir un nom (ex : "Virement SEPA") en sélectionnant la méthode de base disponible (`Manual Payment`)
6. Sauvegarder

Le nouveau mode sera alors disponible dans le champ **"Mode de paiement"** de toutes les factures clients.

> **Note technique :** Le champ utilisé sur la facture est `preferred_payment_method_line_id`
> (modèle `account.payment.method.line`). Chaque ligne est rattachée à un journal.
