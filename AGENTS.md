# Agent Instructions

This repository is maintained by autonomous coding agents and humans.

## Project Shape

- `backend/` contains the FastAPI application and orchestration logic.
- `frontend/` contains static HTML/CSS/JS UI files.
- `skills_library/` and `custom_skills/` contain skill implementations.
- `data/` stores runtime JSON state. Do not commit real secrets.
- `.github/ai-factory/` contains autonomous development state and task planning files.

## Required Checks

Run these before proposing a code PR:

```bash
python -m compileall backend skills_library run.py
python .github/scripts/scan_secrets.py
```

If tests are added or available, also run:

```bash
python -m pytest -q
```

## Change Rules

- Keep changes focused and under 300 changed lines unless the task explicitly requires more.
- Do not touch `data/settings.json` except to remove secrets or preserve the placeholder structure.
- Do not create cosmetic-only PRs.
- Do not update `.github/workflows/`, `.github/scripts/`, or `.github/CODEOWNERS`. AI Factory infrastructure changes require a human-reviewed PR.
- Document behavior changes in `mission.md`, `README.md`, or `.github/ai-factory/state.json` when relevant.

## Pull Request Rules

- Use a clear PR title beginning with one of:
  - `ai-factory(planner):`
  - `ai-factory(architect):`
  - `ai-factory(implementer):`
  - `ai-factory(tester):`
  - `ai-factory(reviewer):`
  - `ai-factory(refactorer):`
  - `ai-factory(documenter):`
  - `ai-factory(security):`
- Include validation commands and results in the PR body.
- Add the label `ai-factory:safe-automerge` only for docs-only or tests-only PRs that passed validation.

