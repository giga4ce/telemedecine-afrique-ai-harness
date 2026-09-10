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

## Hors périmètre

Ce repository ne contient pas le code produit, ne gère pas les données DICOM et ne remplace pas la documentation métier du produit.
