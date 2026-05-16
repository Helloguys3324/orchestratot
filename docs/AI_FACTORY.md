# AI Factory Operations

This repository is configured to run Jules as an autonomous GitHub development factory.

## Required GitHub Setup

1. Install/connect the repository in the Jules web app.
2. Create a Jules API key.
3. Add a repository secret:
   - Name: `JULES_API_KEY`
   - Value: your Jules API key
4. Confirm GitHub Actions are enabled for the repository.
5. Remove `AUTOPILOT_STOP` when scheduled autonomous work should start.

## Schedule

The workflow `.github/workflows/ai-factory-jules.yml` targets 100 Jules tasks per day:

- 12 tasks every 3 hours: 96 tasks/day
- 4 daily meta tasks: 4 tasks/day
- Maximum parallel tasks per run: 12

This stays below the Pro concurrency ceiling of 15 while targeting the 100 task daily budget.

## Emergency Stop

Create or keep this file in the repository root:

```text
AUTOPILOT_STOP
```

When the file exists, scheduled and normal dispatch runs produce no Jules tasks. Manual dispatch can still run with `emergency_override=true`.

## Safe Automerge

Automerge is intentionally conservative. A PR can be merged automatically only when:

- `AI Factory Validate` passed.
- The PR is not a draft.
- The PR title starts with `ai-factory(documenter):` or `ai-factory(tester):`.
- The PR has label `ai-factory:safe-automerge`.

All implementation, refactor, security, and architecture PRs require human review.

## Validation

The validation workflow runs:

```bash
python -m compileall backend skills_library run.py
python .github/scripts/scan_secrets.py
python -m pytest -q
```

The pytest step runs when tests exist outside ignored runtime workspace directories.

## Secrets

Never commit real API keys. Local runtime credentials should use environment variables:

```bash
AUTOGEN_API_KEY=...
AUTOGEN_DEFAULT_MODEL=gemini-2.5-flash
AUTOGEN_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

If a key was committed previously, rotate it immediately.

