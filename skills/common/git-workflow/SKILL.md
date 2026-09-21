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

## GitHub operations (gh CLI)

- Use the `gh` CLI via Bash for every GitHub operation — create a pull request, list or read issues, check CI/workflow status. Do not look for or add a GitHub MCP server; `gh` is the supported path.
- `gh` is already authenticated on the machine through its own keyring. Never manipulate, print, echo, or log an authentication token or credential in a `gh` command; `gh` handles auth by itself and no token ever needs to appear in clear text.
- Autonomy limit, consistent with the git rules above: never create a pull request, open an issue, commit, or push on your own. Each of these actions requires explicit user validation beforehand, exactly like `git commit` / `git push`.
