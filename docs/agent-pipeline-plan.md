# Plan de construction — Écosystème d'agents orchestrés (rôle PO/PM + pipeline)

**Statut :** proposition de plan — à valider avant toute implémentation. Aucun agent créé, aucun ticket Jira ouvert à ce stade.
**Périmètre :** état des lieux des agents existants, définition du rôle PO/PM fusionné, pipeline formalisé d'un ticket, découpage en specs actionnables (ECO-01 à ECO-06) et ordre de réalisation.
**Repository concerné :** `telemedecine-afrique-ai-harness` (contexte LLM, adapters, agents, skills). Le repository produit `telemedecine-afrique` reste la cible d'exécution du pipeline.

**Principe non négociable (rappelé dans tout le document) :** l'agent PO/PM **prépare** (cadrage, rédaction, ouverture de PR, mise à jour Jira) mais **ne décide jamais seul des priorités** et **ne fusionne jamais de PR sans validation humaine explicite**. Même garde-fou que les autres agents du harness : préparer, jamais trancher ni fusionner à la place de l'humain.

---

## 1. État des lieux des agents existants

### 1.1 Sept agents techniques opérationnels

Les fiches vivent sous `llms/claude/agents/*.md` (installées en `.claude/agents/` côté produit). La parité Codex se fait sans mécanisme de sous-agent dédié, via la posture décrite dans `llms/codex/templates/AGENTS.md.tmpl` (section « Codex Notes »), comme déjà fait pour `mentor-python`.

| Agent | Modèle | Écrit du code | Rôle actuel | Statut |
|---|---|---|---|---|
| `backend-fastapi` | sonnet | oui | Routeurs FastAPI async, modèles SQLAlchemy 2.0, migrations Alembic | conditionnel (stack non initialisée) |
| `frontend-react` | sonnet | oui | Composants React, intégration OHIF, résilience réseau côté UI | conditionnel (stack non initialisée) |
| `dicom-integration` | sonnet | oui | Chaîne Orthanc → DICOMweb → OHIF, métadonnées d'examen | actif (cœur du POC) |
| `tests-qualite` | sonnet | oui | Stratégie et exécution des tests, couverture des chemins critiques | actif / conditionnel selon stack |
| `devops-infra` | sonnet | oui | Docker Compose POC, préparation bascule local → OVHcloud | actif |
| `securite-conformite` | opus | non (lecture seule) | Revue sécurité/conformité données de santé, classée par gravité | actif (revue avant fusion) |
| `mentor-python` | opus | non (lecture seule) | Explication pédagogique post-implémentation, ancrage Symfony | actif (après revue) |

### 1.2 Ce que le harness fournit déjà

- **Flux branche + PR par ticket** formalisé dans `skills/common/git-workflow/SKILL.md` : branche `feature/KAN-XXX`, jamais de commit direct sur `main`, PR via `gh` CLI, **jamais de fusion autonome**.
- **Traçabilité Jira** (`profiles/telemedecine-afrique/context/jira.md`) : projet `KAN`, un ticket créé après chaque tâche, serveur MCP `atlassian` en OAuth.
- **Skills communs** : `git-workflow`, `documentation`, `architecture-review` ; skills santé : `data-safety`, `dicom`.
- **Deux adapters** : `claude` (sous-agents natifs) et `codex` (posture dans `AGENTS.md`).

### 1.3 Le manque identifié

Aucun agent ne **porte le ticket de bout en bout** : les sept agents sont des exécutants spécialisés, déclenchés au coup par coup. Personne n'assure le cadrage amont (rédaction du besoin en ticket actionnable), l'enchaînement discipliné des étapes, ni la clôture Jira. C'est le rôle du **PO/PM** décrit ci-dessous.

### 1.4 Décisions et ambiguïtés

| # | Sujet | Décision / statut | Tranché par |
|---|---|---|---|
| A1 | Nom de l'agent | **`po-pm`** — validé par Harou le 29/09/2026 | Harou |
| A2 | Modèle | **`opus`** (raisonnement de cadrage) — validé par Harou le 29/09/2026 | Harou |
| A3 | Outils | `po-pm` a besoin d'écrire (docs, PR) et d'accéder au MCP Jira/`gh` ; périmètre exact d'écriture à borner | ECO-02 |
| A4 | Déclenchement | **À la demande explicite uniquement, jamais proactif ni automatique** — le pipeline ne démarre que si l'utilisateur dit explicitement « lance le pipeline sur KAN-X » ou équivalent. Validé par Harou le 29/09/2026 | Harou |
| A5 | Codex | Parité via posture `AGENTS.md`, sans orchestration de sous-agents réelle côté Codex — portée à confirmer | ECO-05 |

---

## 2. Définition du rôle PO/PM fusionné

Rôle unique fusionnant **Product Owner** (cadrage, priorisation, rédaction du besoin) et **Project Manager** (orchestration, suivi, clôture). Un seul agent, `po-pm`, deux casquettes complémentaires.

**Déclenchement (A4, validé par Harou le 29/09/2026) :** `po-pm` s'active **à la demande explicite de l'utilisateur uniquement** — jamais de manière proactive ni automatique. Le pipeline ne démarre que sur une instruction explicite du type « lance le pipeline sur KAN-X » ou équivalent. En l'absence d'une telle instruction, `po-pm` reste inactif.

### 2.1 Ce qu'il fait

- **Cadrage** : transformer un besoin exprimé en ticket actionnable (contexte, changement attendu, impact, critères d'acceptation), sur le modèle des specs du build-plan produit.
- **Rédaction** : rédiger et mettre à jour la description Jira, la description de PR (contexte → changements → tests → impact), les notes de suivi.
- **Orchestration** : déclencher les agents techniques dans le bon ordre selon le pipeline de la §3, passer le relais d'un agent au suivant, agréger leurs sorties.
- **Suivi** : maintenir l'état du ticket (à faire / en cours / en revue / bloqué), signaler les points d'arrêt atteints.
- **Ouverture de PR** : préparer la branche `feature/KAN-XXX` et ouvrir la PR via `gh` CLI **une fois le travail validé par l'humain**.
- **Clôture Jira** : mettre à jour le ticket (changement réalisé, impact) après fusion humaine.

### 2.2 Ce qu'il ne fait JAMAIS

- ❌ **Décider seul des priorités** — il propose un ordre, l'humain arbitre. Pas de reséquençage du backlog sans validation.
- ❌ **Fusionner une PR** — la fusion appartient toujours à l'humain, comme `git commit` / `git push` (cf. `git-workflow`).
- ❌ **Commit ou push autonome** — même limite d'autonomie que le reste du harness.
- ❌ **Écrire du code métier** — il oriente vers `backend-fastapi`, `frontend-react`, `dicom-integration` ; il n'implémente pas.
- ❌ **Juger la qualité / la sécurité du code** — ce rôle reste à `securite-conformite` ; le PO/PM consomme le verdict, ne le produit pas.
- ❌ **Créer un ticket `KAN-*` fictif** — pas de ticket sans besoin réel validé (cf. `workflow.md`).
- ❌ **Contourner un point d'arrêt humain** défini au pipeline, même en mode « démo » ou « test ».
- ❌ **Manipuler des données de production** ou afficher un secret (règles harness inchangées).

### 2.3 Frontière avec les agents existants

| Frontière | PO/PM | Agent concerné |
|---|---|---|
| Implémentation | oriente, n'écrit pas | `backend-fastapi`, `frontend-react`, `dicom-integration` |
| Tests | demande la couverture, ne l'écrit pas | `tests-qualite` |
| Verdict sécurité | consomme, ne juge pas | `securite-conformite` |
| Pédagogie | déclenche, n'enseigne pas | `mentor-python` |
| Infra / déploiement | planifie l'étape, n'exécute pas | `devops-infra` |

---

## 3. Pipeline formalisé d'un ticket

Séquence de référence du besoin à la clôture. Chaque étape a un **agent responsable**. Les **points d'arrêt 🛑** exigent une validation humaine explicite avant de continuer — le PO/PM prépare, s'arrête, attend le feu vert.

| # | Étape | Agent responsable | Sortie attendue | Point d'arrêt |
|---|---|---|---|---|
| 0 | Expression du besoin | Humain | Besoin brut | — |
| 1 | **Cadrage** | `PO/PM` | Ticket actionnable (contexte, critères d'acceptation, priorité *proposée*) | 🛑 **Validation du cadrage et de la priorité** |
| 2 | Création branche + ticket Jira | `PO/PM` | Branche `feature/KAN-XXX`, ticket `KAN-XXX` | — |
| 3 | **Implémentation** | `backend-fastapi` / `frontend-react` / `dicom-integration` (selon domaine), orchestré par `PO/PM` | Code sur la branche | — |
| 4 | **Tests** | `tests-qualite` | Tests des chemins critiques, résultats | — |
| 5 | **Revue sécurité / conformité** | `securite-conformite` (lecture seule) | Liste de points par gravité (bloquant / à corriger / remarque) | 🛑 si point **bloquant** ouvert |
| 6 | **Explication pédagogique** | `mentor-python` (lecture seule) | Note pédagogique ancrée Symfony | — |
| 7 | **Vérification DevOps** | `devops-infra` | Compose/CI vert, portabilité vérifiée | — |
| 8 | **Ouverture PR** | `PO/PM` | PR via `gh`, description complète, référence `KAN-XXX` | 🛑 **Validation avant push + ouverture PR** |
| 9 | **Relecture humaine** | Humain | Revue de la PR | 🛑 **inhérent** |
| 10 | **Fusion** | Humain **uniquement** | PR fusionnée | 🛑 **jamais par un agent** |
| 11 | **Clôture Jira** | `PO/PM` | Ticket `KAN-XXX` mis à jour (changement, impact) | — |

Représentation linéaire :

```text
besoin → [PO/PM cadrage] 🛑 → branche+ticket
       → [impl: backend/frontend/dicom]
       → [tests-qualite]
       → [securite-conformite] 🛑(si bloquant)
       → [mentor-python]
       → [devops-infra]
       → [PO/PM ouverture PR] 🛑
       → [relecture humaine] 🛑
       → [fusion HUMAINE] 🛑
       → [PO/PM clôture Jira]
```

### 3.1 Règles d'orchestration

- L'étape 5 (revue sécurité) est un **verrou dur** : un point 🔴 bloquant ouvert renvoie à l'étape 3, jamais de contournement.
- L'ordre étape 5 → 6 est fixe : `securite-conformite` **juge**, `mentor-python` **explique** ensuite (jamais l'inverse, jamais de jugement par le mentor).
- Les étapes 3–7 peuvent boucler tant que la revue sécurité n'est pas verte.
- Les trois points d'arrêt humains (1, 8, 9-10) sont **non négociables** et non désactivables.

---

## 4. Découpage en specs actionnables

Sur le modèle des SPEC-XX du build-plan produit. Un agent principal par spec.

### ECO-01 — Cadrage du rôle et des garde-fous PO/PM

- **Objectif :** figer le périmètre exact de l'agent PO/PM (fait / ne fait jamais), son déclenchement et ses points d'arrêt, sans élargir son autonomie au-delà du harness.
- **Inclus :** décisions A1–A5 de la §1.4 ; formulation des garde-fous non négociables ; mode de déclenchement (à la demande vs proactif).
- **Exclus :** rédaction de la fiche d'agent (ECO-02), pipeline détaillé déjà couvert §3, implémentation.
- **Dépendances :** aucune.
- **Terminé si :** nom, modèle, déclenchement, périmètre d'écriture et liste des garde-fous sont tranchés et consignés, validés par Harou.
- **Agent technique principal :** `PO/PM` (spec de cadrage — pas d'exécution).

### ECO-02 — Fiche d'agent PO/PM côté Claude

- **Objectif :** créer `llms/claude/agents/po-pm.md` définissant le rôle, les responsabilités, les garde-fous et les frontières avec les sept agents.
- **Inclus :** frontmatter (`name`, `description`, `tools`, `model`), corps décrivant fait/ne fait jamais, table de frontière §2.3, rappel des points d'arrêt.
- **Exclus :** parité Codex (ECO-05), pipeline opérationnel (ECO-04).
- **Dépendances :** ECO-01.
- **Terminé si :** la fiche existe, respecte le format des autres agents, borne explicitement les outils d'écriture et les interdits (fusion, priorité, commit/push autonomes).
- **Agent technique principal :** `PO/PM` ; revue `securite-conformite`.

### ECO-03 — Formalisation du pipeline en skill

- **Objectif :** matérialiser le pipeline §3 dans un skill réutilisable (`skills/common/agent-pipeline/SKILL.md` ou équivalent) pour que l'orchestration soit documentée et rejouable.
- **Inclus :** séquence des 11 étapes, agent responsable par étape, points d'arrêt 🛑, règles d'orchestration §3.1, articulation avec `git-workflow`.
- **Exclus :** logique d'exécution automatique inter-agents non supportée par le harness ; création de tickets.
- **Dépendances :** ECO-01.
- **Terminé si :** le skill décrit le pipeline complet, référence `git-workflow` et `jira.md`, et énonce les trois points d'arrêt humains non désactivables.
- **Agent technique principal :** `PO/PM` ; appui `devops-infra`.

### ECO-04 — Intégration Jira + branche/PR dans le rôle PO/PM

- **Objectif :** connecter le PO/PM au flux existant (Jira MCP `atlassian`, branche `feature/KAN-XXX`, PR `gh`) sans dupliquer `git-workflow`.
- **Inclus :** procédure de cadrage → ticket, de clôture Jira, de préparation PR ; rappel des limites d'autonomie (pas de commit/push/merge autonome).
- **Exclus :** modification des règles `git-workflow` (réutilisées telles quelles) ; automatisation de la fusion.
- **Dépendances :** ECO-02, ECO-03.
- **Terminé si :** la procédure décrit la création et la clôture de ticket, la préparation de PR référençant `KAN-XXX`, et rappelle chaque point d'arrêt humain.
- **Agent technique principal :** `PO/PM` ; appui `tests-qualite` (critères d'acceptation).

### ECO-05 — Parité comportementale Codex

- **Objectif :** répliquer la posture PO/PM côté Codex sans mécanisme de sous-agent, dans `llms/codex/templates/AGENTS.md.tmpl` (section dédiée), comme fait pour `mentor-python`.
- **Inclus :** rédaction de la posture (fait / ne fait jamais, points d'arrêt) ; mention explicite « même esprit que l'agent `po-pm` côté Claude, sans mécanisme de sous-agent dédié ».
- **Exclus :** émulation d'une orchestration multi-agents réelle côté Codex (non supportée).
- **Dépendances :** ECO-02.
- **Terminé si :** la section Codex décrit la posture PO/PM avec les mêmes garde-fous, et le template reste installable sans régression.
- **Agent technique principal :** `PO/PM` ; revue `securite-conformite`.

### ECO-06 — Validation de bout en bout sur un ticket pilote

- **Objectif :** vérifier le pipeline complet sur un ticket `KAN-*` réel de faible risque, en respectant chaque point d'arrêt.
- **Inclus :** déroulé des 11 étapes ; preuve que les trois points d'arrêt humains ont été honorés ; checklist traçable.
- **Exclus :** ticket à fort impact ; contournement d'un point d'arrêt « pour tester ».
- **Dépendances :** ECO-02, ECO-03, ECO-04, ECO-05.
- **Terminé si :** un ticket pilote passe le pipeline de bout en bout, chaque point d'arrêt est validé par l'humain, la clôture Jira est faite, aucun garde-fou n'a été contourné.
- **Agent technique principal :** `PO/PM` ; appui `tests-qualite`, revue `securite-conformite`.

---

## 5. Ordre de réalisation

```text
ECO-01 Cadrage
   ├── ECO-02 Fiche Claude ──┬── ECO-05 Parité Codex ──┐
   │                         └── ECO-04 Intégration ────┤
   └── ECO-03 Skill pipeline ────────────────────────── ECO-06 Pilote
```

Ordre recommandé :

1. **ECO-01** est le verrou initial : rien ne se code avant que le périmètre et les garde-fous soient tranchés et validés par Harou.
2. **ECO-02** (fiche Claude) et **ECO-03** (skill pipeline) peuvent avancer en parallèle après ECO-01.
3. **ECO-04** connecte le rôle au flux Jira/PR existant, après ECO-02 et ECO-03.
4. **ECO-05** réplique la posture côté Codex, après ECO-02.
5. **ECO-06** valide l'ensemble sur un ticket pilote — dernier maillon, dépend de tout le reste.

Chemin critique : **ECO-01 → ECO-02 → ECO-04 → ECO-06**.

**Point d'arrêt global :** aucune de ces specs ne démarre en implémentation avant validation explicite de ce découpage par Harou (principe non négociable rappelé en tête de document).
