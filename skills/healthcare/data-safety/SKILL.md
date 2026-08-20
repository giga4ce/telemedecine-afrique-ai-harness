---
name: data-safety
description: Use when a task touches health data, DICOM test data, logs, fixtures, screenshots or medical AI output in telemedecine-afrique.
---

# Data Safety

- Never introduce real patient data in code, fixtures, logs, screenshots, demos or test datasets.
- Use anonymized or synthetic DICOM data only.
- Do not expose secrets, credentials, tokens or private keys.
- Do not log medical data or patient identity in clear text.
- Check access-control implications before exposing any exam, report or medical metadata.
- Treat `docs/domain/legal-reserves-by-country.md` in the product repository as the source for regulatory caveats.
- Any AI output that touches image interpretation must remain a suggestion requiring human validation.

If unsure, stop and request a security/compliance review.
