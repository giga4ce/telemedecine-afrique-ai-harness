---
name: environment-check
description: Use at the start of any work session on telemedecine-afrique, before a multi-step task, a PO/PM pipeline run, or a multi-file implementation. Read-only preflight that verifies Git state of both repositories, the Atlassian MCP server auth, gh CLI auth, and Docker daemon reachability, then reports a checklist with the exact command to run for each failure. It never mutates anything and never attempts authentication.
---

# Environment Check

Read-only preflight. Run it at the start of a work session, before starting any real task. It only inspects and reports — it changes nothing, and it never attempts any authentication (OAuth cannot be automated anyway). For each failing item it prints the exact command the user must run, then stops so the user acts before real work begins.

Run the four checks below in order, then produce the checklist.

## a. Git state — both repositories

For the product repository (`telemedecine-afrique`) and the harness repository (`telemedecine-afrique-ai-harness`):

- `git status --short --branch` — working tree must be clean.
- `git branch -vv` — current branch must track `origin/main` and not be behind.
- If behind or ahead of `origin/main`, or if the tree is dirty, mark ❌ and report which repository.

Do not fetch, pull, stash, commit, or clean. Only observe.

## b. Atlassian MCP server — loaded and authenticated

- Check that an `mcp__atlassian__*` tool is available in the session (tool search, or the tool list).
- If present, confirm auth with a lightweight read (e.g. `getAccessibleAtlassianResources` / `atlassianUserInfo`).
- If the tool is absent or the read fails on auth, mark ❌. Do not attempt any workaround or automatic login. Report the exact command:
  - Claude: `claude mcp login atlassian`
  - Codex: `codex mcp login atlassian`

## c. gh CLI — authenticated

- `gh auth status`.
- If not logged in, mark ❌ and report: `gh auth login`.
- Never print, echo, or log any token; `gh` handles its own credentials.

## d. Docker daemon — reachable

Useful before any task touching `poc/docker-compose.yml`.

- `docker info` (or `docker version`).
- If the daemon is unreachable, mark ❌ and report the command to start it (e.g. `sudo systemctl start docker`, or start Docker Desktop).

## e. Summary checklist

Report one line per item, ✅ or ❌. For each ❌, give the exact command to run. Do not start any real task until the blocking items are green.

```text
Environment check — telemedecine-afrique
- [ ] Git product repo clean & up to date with origin/main
- [ ] Git harness repo clean & up to date with origin/main
- [ ] Atlassian MCP loaded & authenticated
- [ ] gh CLI authenticated
- [ ] Docker daemon reachable
```

Replace each `[ ]` with ✅ or ❌. Under any ❌, print its fix command. End with a clear go / no-go: proceed only when every blocking item is ✅.
