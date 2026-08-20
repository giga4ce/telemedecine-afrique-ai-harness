# Connecteurs (MCP) recommandés

Ce fichier concerne le tooling des agents de développement. Il ne fait pas partie du repository produit.

## Côté développement — Claude Code / Codex

Ces connecteurs se configurent dans l'environnement de développement (fichier `.mcp.json` à la racine du projet pour Claude Code, ou équivalent Codex). Ils donnent aux agents techniques un accès direct à vos outils, plutôt que de vous faire copier-coller manuellement.

| Connecteur | Utilité pour ce projet | Priorité |
|---|---|---|
| **GitHub** | Créer des branches, ouvrir des pull requests, lire les issues — l'agent `tests-qualite` ou `backend-symfony` peut ouvrir une PR directement après une tâche. | Élevée dès le démarrage du dépôt Git |
| **Base de données (Postgres/MySQL)** | Permet à l'agent backend d'inspecter le schéma réel en développement — **uniquement en environnement local/test, jamais connecté à une base contenant de vraies données**. | Élevée une fois la base de développement créée |
| **Docker** | Inspection de conteneurs en cours d'exécution pour le débogage (logs, statut) sans sortir de la session. | Moyenne |
| **Sentry (ou équivalent de suivi d'erreurs)** | Une fois en pré-production : l'agent `devops-infra` peut consulter les erreurs remontées sans changer d'outil. | Basse pour l'instant (post-POC) |

Rappel : un connecteur base de données ou GitHub donne un accès réel à vos systèmes — à activer volontairement, jamais par défaut, et à retirer une fois la tâche de développement terminée si l'accès n'est plus nécessaire.

## Côté pilotage — claude.ai (cette conversation et les suivantes)

Utile si vous voulez que je vous aide directement sur le suivi projet, pas seulement sur le code :

| Connecteur | Utilité |
|---|---|
| **Gestion de tâches (Linear, Jira, Notion...)** | Suivre l'avancement du POC et des chantiers juridiques par pays sans ressaisir un statut à chaque échange. |
| **Slack** | Partager un point d'avancement ou une synthèse directement dans le canal de l'équipe projet. |
| **Google Drive / stockage documentaire** | Centraliser les versions du dossier de projet, des comptes rendus juridiques, sans réupload manuel à chaque fois. |

Ces connecteurs se branchent depuis l'interface claude.ai (pas depuis ce dépôt de code) — à activer au moment où vous en avez l'usage concret, pas en anticipation.

## Ce qu'il ne faut pas connecter à ce stade

- Aucun connecteur donnant accès à des données patient réelles ou à un système de production tant que les autorisations réglementaires ne sont pas obtenues (voir `docs/domain/legal-reserves-by-country.md` dans le repository produit).
- Éviter de connecter plusieurs outils de gestion de tâches en parallèle (Linear + Jira par exemple) : source de confusion sur la source de vérité du planning.
