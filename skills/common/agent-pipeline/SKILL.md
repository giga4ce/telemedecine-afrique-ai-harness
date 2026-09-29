---
name: agent-pipeline
description: Use when po-pm is explicitly invoked to orchestrate a ticket end to end (« lance le pipeline sur KAN-X »). Replayable checklist of the 11 pipeline stages — responsible agent, expected output, and human stop points per stage — plus the orchestration rules (security lock, fixed security→pedagogy order, three non-negotiable human stops). It is a sequence to follow, not an automatic multi-agent execution engine.
---

# Agent Pipeline

Séquence de référence pour porter un ticket du besoin à la clôture, orchestrée par `po-pm` (ou la session principale). Source de vérité : `docs/agent-pipeline-plan.md` §3 et §3.1 — ce skill en est la checklist opérationnelle rejouable.

**Déclenchement :** à la demande explicite de l'utilisateur uniquement (« lance le pipeline sur KAN-X »), jamais proactif — cf. la fiche `po-pm`.

**Nature :** ce skill décrit une **séquence à suivre** par l'orchestrateur (`po-pm` ou la session principale). Ce n'est **pas** un mécanisme d'exécution automatique inter-agents : le harness n'a pas de vraie orchestration autonome. C'est une **checklist rejouable, pas un moteur** — chaque étape est déclenchée manuellement, dans l'ordre.

## Les 11 étapes

| # | Étape | Agent responsable | Sortie attendue | Point d'arrêt |
|---|---|---|---|---|
| 0 | Expression du besoin | Humain | Besoin brut | — |
| 1 | **Cadrage** | `po-pm` | Ticket actionnable (contexte, critères d'acceptation, priorité *proposée*) | 🛑 **Validation du cadrage et de la priorité** |
| 2 | Création branche + ticket Jira | `po-pm` | Branche `feature/KAN-XXX`, ticket `KAN-XXX` | — |
| 3 | **Implémentation** | `backend-fastapi` / `frontend-react` / `dicom-integration` (selon domaine), orchestré par `po-pm` | Code sur la branche | — |
| 4 | **Tests** | `tests-qualite` | Tests des chemins critiques, résultats | — |
| 5 | **Revue sécurité / conformité** | `securite-conformite` (lecture seule) | Liste de points par gravité (bloquant / à corriger / remarque) | 🛑 si point **bloquant** ouvert |
| 6 | **Explication pédagogique** | `mentor-python` (lecture seule) | Note pédagogique ancrée Symfony | — |
| 7 | **Vérification DevOps** | `devops-infra` | Compose/CI vert, portabilité vérifiée | — |
| 8 | **Ouverture PR** | `po-pm` | PR via `gh`, description complète, référence `KAN-XXX` | 🛑 **Validation avant push + ouverture PR** |
| 9 | **Relecture humaine** | Humain | Revue de la PR | 🛑 **inhérent** |
| 10 | **Fusion** | Humain **uniquement** | PR fusionnée | 🛑 **jamais par un agent** |
| 11 | **Clôture Jira** | `po-pm` | Ticket `KAN-XXX` mis à jour (changement, impact) | — |

Représentation linéaire :

```text
besoin → [po-pm cadrage] 🛑 → branche+ticket
       → [impl: backend/frontend/dicom]
       → [tests-qualite]
       → [securite-conformite] 🛑(si bloquant)
       → [mentor-python]
       → [devops-infra]
       → [po-pm ouverture PR] 🛑
       → [relecture humaine] 🛑
       → [fusion HUMAINE] 🛑
       → [po-pm clôture Jira]
```

## Règles d'orchestration (§3.1)

- **Verrou dur — étape 5** : un point 🔴 bloquant en revue sécurité renvoie à l'étape 3. Jamais de contournement, même en mode « démo » ou « test ».
- **Ordre fixe 5 → 6** : `securite-conformite` **juge**, puis `mentor-python` **explique**. Jamais l'inverse, jamais de jugement par le mentor.
- **Boucle 3 → 7** : les étapes 3 à 7 peuvent boucler tant que la revue sécurité n'est pas verte.
- **Trois points d'arrêt humains non négociables et non désactivables** :
  1. 🛑 Étape 1 — validation du cadrage et de la priorité (avant création branche/ticket).
  2. 🛑 Étape 8 — validation avant push + ouverture de PR.
  3. 🛑 Étapes 9-10 — relecture puis **fusion humaine**, jamais par un agent.

## Articulation avec les autres règles

- **Branche et PR** : suivre `skills/common/git-workflow` (branche `feature/KAN-XXX`, jamais de commit/push/fusion autonome). Ne pas dupliquer ses règles ici.
- **Traçabilité Jira** : suivre `profiles/telemedecine-afrique/context/jira.md` (projet `KAN`, ticket créé/mis à jour par tâche). Ne pas dupliquer son contenu ici.
- **Rôle et garde-fous de l'orchestrateur** : voir la fiche `po-pm` (déclenchement, périmètre d'écriture, arrêt avant mutation sensible).
