---
name: architecture-review
description: Use when reviewing structural changes in telemedecine-afrique: protect the simple POC architecture and prevent premature target-platform complexity.
---

# Architecture Review

- Check whether the change belongs to the current POC, the post-POC pilot, the target platform or the AI Harness.
- Do not introduce Symfony, React, API Platform, CI, billing, RCP or multi-country architecture unless the task asks for it.
- Prefer a small, demonstrable Orthanc + DICOMweb + OHIF chain for the POC.
- Document structural decisions in product docs or a future ADR.
- Treat `docs/poc/scope.md` as the POC boundary source.
