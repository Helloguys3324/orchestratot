# AI Factory Operations

This repository is configured to run Jules as an autonomous GitHub development factory.

## Required GitHub Setup

1. **App Installation:** Install/connect the repository in the Jules web app.
2. **API Key Creation:** Create a Jules API key.
3. **Secret Configuration:** Add repository secrets (navigate to **Settings -> Secrets and variables -> Actions** in your repository):
   - Name: `JULES_API_KEY`
   - Value: your Jules API key
   - Name: `AUTOGEN_API_KEY` (if your models require authentication)
   - Value: your LLM provider API key
4. **Action Verification:** Confirm GitHub Actions are enabled for the repository.
5. **Autopilot Activation:** Remove or rename `AUTOPILOT_STOP` when scheduled autonomous work should start.

**Warning: Infrastructure Lock**
*Infrastructure files including `.github/workflows/`, `.github/scripts/`, and `.github/CODEOWNERS` are securely locked for AI agents. These files must only be modified via human PRs outside of the automated AI Factory framework.*

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

The validation workflow runs the following full suite:

```bash
# Verify Python syntax and compilation
python -m compileall backend skills_library run.py

# Ensure no API keys, credentials, or secrets are accidentally committed
python .github/scripts/scan_secrets.py

# Run all backend unit and integration tests (ensure local testing dependencies are installed)
PYTHONPATH=. python -m pytest -q

# Run frontend tests using native node runner (no extra npm packages required)
node --experimental-test-coverage --test frontend/tests/*.js
```

The pytest step runs when tests exist outside ignored runtime workspace directories.

### Vulnerability Scanning

To evaluate dependencies for known security vulnerabilities, use `pip-audit`. Because `pip-audit` needs to accurately evaluate transitive dependencies, ensure the project core requirements are installed in your local environment first:

```bash
# Ensure core requirements are installed
pip install -r backend/requirements.txt

# Run the security audit
pip install pip-audit
pip-audit -r backend/requirements.txt
```

### Frontend Visual Validation

When frontend files are changed, visual inspection is mandatory. Start the app locally (`python run.py`), open the UI in a browser, and manually walk through the changed flows to ensure no layout breakages or console errors exist.

## Secrets

Never commit real API keys, credentials, or `.env` files to source control.

**CI/CD Environments:**
Use GitHub Actions Secrets (navigate to **Settings -> Secrets and variables -> Actions**) to securely store production and testing keys.

**Local Development:**
Local runtime credentials should use environment variables (e.g., by placing them in a `.env` file at the root of the project, which is automatically parsed by `pydantic-settings`). You can copy the provided `.env.example` file to create your local `.env` configuration:

```bash
cp .env.example .env
```

```bash
AUTOGEN_API_KEY=...
AUTOGEN_DEFAULT_MODEL=gemini-2.5-flash
AUTOGEN_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

The application uses Pydantic `SecretStr` to prevent accidental logging or JSON serialization of secrets loaded from `.env`. Legacy configurations from `data/settings.json` are automatically migrated to `.env` upon startup and securely deleted. Runtime configuration updates via the API directly preserve the ergonomics of the `.env` file by only persisting explicitly updated fields. Empty strings in environment variables are filtered out on load to prevent overwriting valid defaults, however they are allowed during API updates to intentionally clear credentials.

You can verify that no secrets are accidentally committed by running:
```bash
python .github/scripts/scan_secrets.py
```

If a key was committed previously, rotate it immediately.

