---
name: api-platform-conventions
description: Conditional Claude skill for future Symfony/API Platform work in telemedecine-afrique. Use only after the product repository initializes that stack or the user explicitly asks for it.
---

# Conventions API Platform conditionnelles

Statut : future / conditional / stack not initialized.

Ne pas introduire Symfony, API Platform, Doctrine ou des ressources métier pendant le POC documentaire ou le POC Orthanc/OHIF, sauf demande explicite.

- Une ressource API par concept métier du dossier de projet : `Etablissement`, `Expert`, `Examen`, `Vacation`, `CompteRendu`, `AvisSpecialise`, `RCP`.
- Groupes de sérialisation systématiques : `{ressource}:read` et `{ressource}:write`, jamais d'exposition par défaut de tous les champs.
- Toute donnée médicale (examen, compte rendu) expose un champ `dateSuppressionPrevue` ou équivalent de traçabilité, cohérent avec les exigences de conformité du dossier de projet.
- Sécurité : un Voter dédié par ressource sensible, jamais une vérification de rôle inline dans le contrôleur.
- Pagination et filtres activés par défaut sur les collections volumineuses (liste des examens par établissement).
