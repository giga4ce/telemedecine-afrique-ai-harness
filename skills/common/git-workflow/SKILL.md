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

## Branch + PR flow per Jira ticket (product repo only)

This flow applies to the telemedecine-afrique product repository only, never to the AI Harness repository, whose workflow is unchanged.

- Any change tied to a Jira ticket (`KAN-XXX`) is done on a branch named `feature/KAN-XXX`, never directly on `main`.
- Once the work is finished and validated by the user, and only then:
  1. push the branch;
  2. open a Pull Request with the `gh` CLI (see the section above for `gh` usage), describing the change and referencing the Jira ticket `KAN-XXX`;
  3. never merge autonomously — the user reviews and merges the PR themselves, exactly like a `git commit` or `git push`. The autonomy limit above extends to PR merges.
