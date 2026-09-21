# telemedecine-afrique-ai-harness

Ce repository contient le contexte LLM, les adapters et les skills utilisés pour travailler sur le repository produit `telemedecine-afrique`.

Le repository produit reste la source canonique pour la vision, le POC, l'architecture réelle, le domaine et les réserves juridiques. Le harness pointe vers ces documents sans les recopier.

## Structure

- `profiles/telemedecine-afrique/` : contexte commun du projet.
- `llms/codex/` : adapter et template Codex.
- `llms/claude/` : adapter, template et sous-agents Claude.
- `skills/` : skills réutilisables.
- `docs/mcp/` : recommandations MCP et connecteurs.
- `scripts/install-context` : installe le contexte généré dans un repository produit.

## Installation du contexte

Exemple Codex :

```bash
./scripts/install-context \
  --llm codex \
  --profile telemedecine-afrique \
  --target /path/to/telemedecine-afrique \
  --dry-run
```

Exemple Claude :

```bash
./scripts/install-context \
  --llm claude \
  --profile telemedecine-afrique \
  --target /path/to/telemedecine-afrique \
  --dry-run
```

Lire [`docs/install-context.md`](docs/install-context.md) pour les options, les manifestes, les conflits et les codes de sortie.

## Serveur MCP Atlassian (Jira)

Le harness installe la déclaration du serveur MCP `atlassian` (transport HTTP `v2/mcp`, sans secret) : `.mcp.json` côté Claude, `.codex/config.toml` côté Codex. Après installation, chaque développeur s'authentifie **une fois par outil et par machine** :

```bash
claude mcp login atlassian   # Claude Code
codex mcp login atlassian    # Codex CLI
```

Détails et règle de traçabilité par ticket : [`docs/install-context.md`](docs/install-context.md) et `profiles/telemedecine-afrique/context/jira.md`.

## Hors périmètre

Ce repository ne contient pas le code produit, ne gère pas les données DICOM et ne remplace pas la documentation métier du produit.
