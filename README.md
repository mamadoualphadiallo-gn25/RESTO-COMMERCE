# RESTO-COMMERCE

Gestion unifiée restaurant + commerce sur une base SQLite centrale.

## Architecture
- PC Windows principal : API locale FastAPI + fichier SQLite.
- Clients : application Windows, Android, web PC et web mobile.
- Les clients accèdent aux données uniquement via l'API HTTP locale. Ne jamais ouvrir le fichier SQLite directement depuis les appareils réseau.

## Démarrage API
1. Installer Python 3.11+.
2. Windows : lancer `windows/install.bat`.
3. Lancer `windows/start-server.bat`.
4. Ouvrir `http://127.0.0.1:8000/docs`.
5. Depuis le réseau local, remplacer 127.0.0.1 par l'adresse IP privée du PC.

## Compilation
GitHub Actions contient deux workflows : Windows EXE et Android APK. Dans GitHub > Actions, lancer chacun manuellement ou pousser un commit qui modifie les dossiers concernés. Les artefacts seront téléchargeables depuis le run.

Attention : les premières sorties sont des builds de développement. L'APK debug n'est pas signé pour distribution publique. L'EXE actuel est une interface cliente et nécessite que l'API locale tourne sur le PC.

## État
Socle initial : catalogue produits, API, enregistrement de ventes et mouvements de stock. Les modules avancés (commandes restaurant, cuisine, caisse, employés, achats, rapports et impressions) restent à compléter.
