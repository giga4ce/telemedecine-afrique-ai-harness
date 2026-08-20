---
name: react-conventions
description: Conditional Claude skill for future React work in telemedecine-afrique. Use only after the product repository initializes that stack or the user explicitly asks for it.
---

# Conventions React conditionnelles

Statut : future / conditional / stack not initialized.

Ne pas introduire React pendant le POC documentaire ou le POC Orthanc/OHIF, sauf demande explicite.

- Un client API centralisé (ex. `apiClient.ts`) : aucun `fetch`/`axios` direct dispersé dans les composants.
- Composants organisés par domaine métier (`etablissements/`, `examens/`, `experts/`, `vacations/`) plutôt que par type technique.
- Tout composant affichant une donnée médicale ou un statut d'examen gère explicitement trois états : chargement, erreur réseau, succès — pas d'état implicite.
- Les suggestions produites par un agent IA fonctionnel (ex. second regard IA) sont affichées dans un composant visuellement distinct (bordure, étiquette "Suggestion IA — à valider"), jamais fondues dans le contenu validé.
