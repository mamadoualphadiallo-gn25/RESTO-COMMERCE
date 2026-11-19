# Cahier des charges — RESTO-COMMERCE

## Objectif
Logiciel de gestion restaurant + commerce avec application Windows, application Android, site PC et site mobile, utilisant une base SQLite unique hébergée sur un PC principal.

## Architecture
- PC principal : API locale FastAPI et SQLite.
- Clients : Windows, Android et navigateurs.
- Les clients distants communiquent par API ; aucun accès direct au fichier SQLite.
- Réseau local Wi-Fi/Ethernet ; PC principal requis pour l'accès aux données centrales.
- File d'attente locale et synchronisation différée à ajouter pour les périodes sans réseau.

## Modules attendus
- Utilisateurs, rôles et permissions.
- Paramètres, établissement, logo, imprimantes.
- Produits, catégories, unités, codes-barres, prix achat/vente.
- Stocks, inventaires, mouvements et alertes.
- Restaurant : salles, tables, réservations, commandes, menus, suppléments, cuisine, service, additions.
- Commerce : panier, ventes, retours, remises, reçus.
- Caisse : sessions, ouverture/fermeture, mouvements.
- Clients, fournisseurs, achats, dettes.
- Dépenses, charges, rapports, exports PDF/CSV.
- Journal d'audit, sauvegarde et restauration.

## Règles
- Montants monétaires en entiers GNF.
- Vente et mouvements de stock dans une transaction atomique.
- Contrôle du stock avant validation.
- Annulation tracée avec motif ; pas de suppression silencieuse.
- Séparation des canaux restaurant et commerce, avec statistiques consolidées.
- Chaque opération sensible doit être associée à un utilisateur.

## Sécurité
- Authentification et hachage sécurisé des mots de passe.
- API limitée au réseau privé local.
- Pare-feu Windows limité au profil privé.
- Sauvegarde cohérente et test de restauration.
- Journalisation et protection contre doubles validations.

## Phases
1. Socle API, SQLite, catalogue et ventes.
2. Restaurant, tables, commandes et cuisine.
3. Commerce, caisse, achats et stocks avancés.
4. Comptes, permissions, clients, fournisseurs et dépenses.
5. Rapports, PDF, tickets et imprimantes.
6. Interfaces Windows, Android et web.
7. Tests multi-appareils, sauvegarde, restauration et installateurs.
