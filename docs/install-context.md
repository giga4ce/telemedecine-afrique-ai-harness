# install-context

`scripts/install-context` installe le contexte AI Harness dans un repository produit. La v1 supporte uniquement `codex` et `claude`.

## Source de vérité

Le repository produit reste canonique pour la vision, le POC, l'architecture réelle, la roadmap, le domaine, le juridique et les futures fonctionnalités produit.

Le harness installe des pointeurs, des règles de travail, des skills et des templates LLM. Il ne recopie pas la documentation produit.

## Commandes

Codex :

```bash
./scripts/install-context \
  --llm codex \
  --profile telemedecine-afrique \
  --target /path/to/telemedecine-afrique
```

Claude :

```bash
./scripts/install-context \
  --llm claude \
  --profile telemedecine-afrique \
  --target /path/to/telemedecine-afrique
```

## Options

- `--llm <codex|claude>` : adapter à utiliser.
- `--profile <profile>` : profil à installer.
- `--target <path>` : repository produit cible.
- `--dry-run` : affiche les opérations sans écrire.
- `--check` : vérifie l'installation sans écrire.
- `--diff` : affiche les différences sans écrire.
- `--force` : remplace un fichier géré modifié localement, avec sauvegarde.
- `--help` : affiche l'aide.

Codes de sortie :

- `0` : succès ou contexte à jour.
- `1` : erreur technique.
- `2` : contexte absent, obsolète ou différent.
- `3` : conflit local.

## Sorties Codex

- `AGENTS.md`
- `.codex/context/`
- `.codex/skills/`
- `.codex/harness-manifest.json`

## Sorties Claude

- `CLAUDE.md`
- `.claude/context/`
- `.claude/agents/`
- `.claude/skills/`
- `.claude/harness-manifest.json`

Les skills conditionnels FastAPI et React ne sont pas installés en v1, car le produit n'initialise pas encore ces stacks.

## Manifest

Chaque LLM reçoit son manifeste :

- Codex : `.codex/harness-manifest.json`
- Claude : `.claude/harness-manifest.json`

Structure :

```json
{
  "schema_version": 1,
  "harness": "telemedecine-afrique-ai-harness",
  "profile": "telemedecine-afrique",
  "llm": "codex",
  "adapter": "llms/codex/adapter.yaml",
  "files": {
    "AGENTS.md": {
      "source": "llms/codex/templates/AGENTS.md.tmpl",
      "sha256": "..."
    }
  }
}
```

Les chemins du manifeste sont relatifs et portables.

## Conflits

Si un fichier géré a été modifié localement, l'installation normale s'arrête :

```text
CONFLICT: AGENTS.md was modified locally.
```

`--diff` affiche l'écart entre le contenu actuel et le contenu attendu.

`--force` remplace uniquement les fichiers gérés par le manifeste. Avant remplacement, le script crée une sauvegarde dans :

- `.codex/.harness-backups/`
- `.claude/.harness-backups/`

La sauvegarde utilise un nom déterministe et remplace la sauvegarde précédente du même fichier pour éviter une accumulation infinie.

## Sécurité

Le script refuse les sources ou destinations sensibles évidentes :

- `.env`
- `.env.*`
- `*.pem`
- `*.key`
- `*.p12`
- `*.pfx`
- `id_rsa`
- `id_ed25519`
- `credentials*`
- `secrets*`

Il ne modifie pas Git, ne crée pas de branche, ne commit pas, ne push pas et ne supprime pas les anciens fichiers gérés. Les anciens fichiers absents du nouveau plan sont signalés comme `STALE MANAGED FILE`.
