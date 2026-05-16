# AI Factory Operations

This repository is configured to run Jules as an autonomous GitHub development factory.

## Required GitHub Setup

1. Install/connect the repository in the Jules web app.
2. Create a Jules API key.
3. Add a repository secret:
   - Name: `JULES_API_KEY`
   - Value: your Jules API key
4. Confirm GitHub Actions are enabled for the repository.
5. Remove or rename `AUTOPILOT_STOP` when scheduled autonomous work should start.

## Schedule

The workflow `.github/workflows/ai-factory-tick.yml` targets 100 Jules tasks per day by dispatching `.github/workflows/ai-factory-jules.yml`:

- 1 task every 15 minutes: 96 tasks/day
- 4 daily meta tasks: 4 tasks/day
- Maximum parallel tasks per run: 1 for normal runs, 4 for the daily meta run

This keeps the factory active around the clock with lower conflict risk while targeting the 100 task daily budget. It also reduces the impact of a delayed or skipped GitHub schedule event.

`AI Factory Jules` is intentionally `workflow_dispatch` only. This prevents duplicate Jules tasks: `AI Factory Tick` is the single scheduled heartbeat, and it dispatches normal and daily meta Jules runs through the GitHub API.

## Role Routing

Normal runs use a weighted 15-minute role sequence instead of taking the first tasks from the queue. The six-hour cycle is:

```text
Q00: planner
Q01: implementer
Q02: tester
Q03: reviewer
Q04: implementer
Q05: implementer
Q06: tester
Q07: documenter
Q08: implementer
Q09: refactorer
Q10: tester
Q11: security
Q12: architect
Q13: implementer
Q14: tester
Q15: reviewer
Q16: planner
Q17: implementer
Q18: tester
Q19: security
Q20: implementer
Q21: refactorer
Q22: documenter
Q23: tester
```

- `implementer` gets the most slots for product/backend/frontend/skills work.
- `tester` appears every hour to keep validation improving.
- `documenter`, `security`, `reviewer`, and `refactorer` rotate through smaller but regular slots.
- `architect` runs occasionally in hourly work and again in the daily meta batch.
- `planner` appears twice per six-hour cycle plus the daily meta batch, where it updates the task queue instead of touching app code.

The task planner reads `.github/ai-factory/task_queue.json`. Each task can define:

- `role`
- `lane`
- `write_scope`
- `avoid_scope`
- `risk_level`
- `automerge_allowed`
- `prompt`

Jules receives these fields directly in the prompt, so each task has a role, a purpose, and path boundaries.

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

