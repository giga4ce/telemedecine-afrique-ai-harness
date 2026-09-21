# Jira — suivi projet

## Projet

- Clé projet : `KAN`
- Template : Kanban
- Board : https://harouguindja.atlassian.net/jira/software/projects/KAN/boards/1
- Accès outillé : serveur MCP Atlassian `atlassian` (transport HTTP `https://mcp.atlassian.com/v2/mcp`).

## Règle de traçabilité

Un ticket Jira est créé après chaque tâche effectuée, pour traçabilité (règle actée par Harou).

- Une tâche livrée sans ticket associé est incomplète.
- Le ticket décrit : contexte, changement réalisé, impact.
- Rattacher le ticket au board `KAN`.

## Authentification

Le serveur MCP Atlassian utilise OAuth. Aucun token n'est stocké dans le dépôt.
Chaque développeur s'authentifie une fois par machine (voir `docs/install-context.md`).
