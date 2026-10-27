# The Hunter

Application personnelle locale : interface, serveur Python, stockage SQLite, recherche web OpenAI, analyse des offres, questions ciblées, génération de CV et exports Word/PDF.

## Démarrer

Pour une installation Python classique : `python3 -m pip install -r requirements.txt`, puis `python3 backend/server.py`. Copier `.env.example` vers `.env` pour la configuration locale. Le dépôt ne contient ni CV ni données de recherche.

Double-cliquer `start.command`, puis ouvrir http://127.0.0.1:4173. Le runtime Python fourni avec Codex est configuré dans le script. Les bibliothèques nécessaires sont python-docx, reportlab et pypdf.

## Configuration

Renseigner `OPENAI_API_KEY` dans `.env`. Ne jamais partager ce fichier. Le serveur relit les paramètres à chaque opération, sans redémarrage. Le modèle se configure avec `OPENAI_MODEL` (par défaut gpt-5.4). Les appels utilisent l’API Responses et l’outil web_search. Les opérations IA peuvent entraîner des frais API.

Le CV maître, les réponses et les résultats restent dans `.hunter/`, hors du dossier web, et sont exclus de Git. Le CV et les données utiles à la demande sont envoyés à OpenAI lors des opérations IA. Les réponses ne sont pas stockées via l’API (`store: false`), sans prétendre modifier les règles de rétention du fournisseur.

Dans Paramètres, importer exclusivement le CV de référence. Son remplacement invalide les analyses et documents précédents. Pour un poste précis, Ajouter une offre permet de saisir sa description complète et ses vérifications. Lancer la recherche utilise le seuil, la période et le site sélectionnés. Les sources du menu sont des canaux prévus, pas une garantie d’exploration exhaustive : le journal montre les consultations rapportées pour chaque recherche.

## Parcours CV

Ouvrir une offre, analyser, répondre aux questions et confirmer chaque réponse ou choisir de ne pas l’intégrer. Les réponses en attente bloquent la génération. Les preuves citées sont rapprochées du texte de référence. Ce contrôle ne remplace pas la relecture : les scores restent des estimations IA. Les téléchargements Word et PDF sont disponibles après génération réussie. Le PDF est limité à deux pages ; la mise en page est standard A4 et ne reproduit pas le PDF maître à l’identique. Le nombre de pages Word peut varier selon le logiciel.

## Google Drive

La connexion native de cette conversation n’est pas transmissible au serveur. Configurer OAuth personnel via GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET et GOOGLE_REFRESH_TOKEN ; un GOOGLE_ACCESS_TOKEN temporaire est aussi accepté. Les autorisations doivent permettre la recherche, la création et la lecture des fichiers du dossier CV - The Hunter. Aucun secret n’est fourni au navigateur.

Le bouton Drive sauvegarde explicitement les deux fichiers dans CV - The Hunter / YYYY-MM Month. Les liens sont vérifiés par une lecture du fichier. Les uploads sont réconciliés par appProperties avant un nouvel envoi. Aucun partage public n’est créé. Le journal est stocké localement et exportable en CSV ; la synchronisation automatique avec le Google Sheet The Hunter Log n’est pas implémentée.

## Limites et vérification

L’accès à Telegram/Discord privés n’est pas connecté. Le moteur web ne garantit ni une couverture exhaustive ni l’accès aux sites bloqués. Les dates ou statuts non attestés sont exclus des résultats retenus. Aucun message ni candidature n’est envoyé. Pas de recherche récurrente ou de publication hébergée configurée.

Tests : lancer le runtime Python avec `-m unittest discover -s tests -v`. `tests/check_exports.py` teste les fichiers avec un exemple synthétique. La connexion OpenAI et la sauvegarde Drive doivent être vérifiées avec les identifiants réels avant de considérer ces intégrations opérationnelles.

## Mode accompagné sans clé API

Le bouton d’adaptation crée une demande locale via `/api/cv-request`, sans appel OpenAI. Copier cette demande puis l’envoyer dans la conversation permet de continuer avec l’agent. L’enregistrement ne déclenche ni message automatique ni génération en arrière-plan. Une analyse préparée dans le chat est affichable dans le dossier et les réponses sont conservées. Après réponse ou exclusion explicite de chaque question, une nouvelle demande peut être préparée pour la rédaction. Le CV final est ajouté par l’agent au dossier lors de son traitement.
