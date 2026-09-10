---
name: fastapi-conventions
description: Conditional Claude skill for future FastAPI backend work in telemedecine-afrique. Use only after the product repository initializes that stack or the user explicitly asks for it.
---

# Conventions FastAPI conditionnelles

Statut : future / conditional / stack not initialized.

Ne pas introduire FastAPI, SQLAlchemy, Alembic ou des ressources métier pendant le POC documentaire ou le POC Orthanc/OHIF, sauf demande explicite.

- Un routeur (`APIRouter`) par domaine métier : `etablissement`, `expert`, `examen`, `vacation`, `compte_rendu`, `avis_specialise`, `rcp`.
- Schémas Pydantic séparés lecture/écriture : `{Ressource}Read` et `{Ressource}Write`, jamais d'exposition par défaut de tous les champs du modèle SQLAlchemy.
- Toute donnée médicale (examen, compte rendu) expose un champ `date_suppression_prevue` ou équivalent de traçabilité, cohérent avec les exigences de conformité du dossier de projet.
- Sécurité : contrôle d'accès par dépendance FastAPI (`Depends(require_role(...))`), une dépendance dédiée par ressource sensible, jamais une vérification de rôle inline dans la route.
- Pagination (`limit`/`offset` ou curseur) et filtres activés par défaut sur les collections volumineuses (liste des examens par établissement).
- Endpoints async (`async def`) avec session SQLAlchemy 2.0 async injectée par dépendance ; migrations gérées par Alembic.
