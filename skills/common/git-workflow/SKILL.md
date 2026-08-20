---
name: git-workflow
description: Use when working with Git in the telemedecine-afrique product repository or AI Harness: inspect status, preserve local changes, follow ticket-based branch conventions, and avoid unsafe history changes.
---

# Git Workflow

- Start with `git status --short --branch`, `git branch -vv`, and the relevant recent log.
- Do not create a `TEL-*` branch unless the ticket is verified.
- Never force-push, reset hard, or discard local changes without explicit user approval.
- Keep product and harness commits separate.
- Before a commit, verify the diff matches the requested scope.
- For product work, prefer branches like `docs/TEL-123-short-description` only when the ticket exists.
