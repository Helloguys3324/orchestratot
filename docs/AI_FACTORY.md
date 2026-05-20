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

## Validation & Secrets

Please refer to [docs/SETUP.md](SETUP.md) for detailed validation commands and secrets management instructions.

## Metrics Tracking

The `.github/ai-factory/metrics.json` file tracks various metrics related to the AI Factory's operation, such as `task_started`, `task_claimed`, `pr_created`, `validation_passed`, `pr_merged`, and `task_completed`. When updating these metrics, logical consistency must be maintained across interdependent fields. For example, if `pr_merged` is greater than zero, `pr_created` and `validation_passed` must logically be at least equal to that number. Note that empty PRs (where no code modifications were made due to no meaningful safe change existing) are included in the counts for `pr_merged` and `task_completed`, as they still progress through the full task and PR lifecycle.

## Workflows & Diagrams

### Task Lifecycle

```mermaid
stateDiagram-v2
    [*] --> pending: Planner creates task
    pending --> claimed: Orchestrator assigns task
    claimed --> running: Agent begins execution
    running --> completed: PR merged or goal satisfied
    running --> failed: Validation or execution error
    failed --> pending: Task returned for retry
    claimed --> abandoned: Timeout reached
    running --> abandoned: Timeout reached
    pending --> obsolete: Deprecated by planner
    pending --> duplicate: Merged by planner
    pending --> blocked: Awaiting dependencies
    completed --> [*]
    abandoned --> [*]
    obsolete --> [*]
    duplicate --> [*]
```

### PR Lifecycle

```mermaid
stateDiagram-v2
    [*] --> PR_Created: Agent pushes branch
    PR_Created --> ValidationChecks: Trigger GitHub Actions
    ValidationChecks --> SecretsScan: scan_secrets.py
    ValidationChecks --> PythonCompile: compileall
    ValidationChecks --> BackendTests: pytest
    ValidationChecks --> FrontendTests: node --test
    SecretsScan --> PR_Passed: All Pass
    PythonCompile --> PR_Passed: All Pass
    BackendTests --> PR_Passed: All Pass
    FrontendTests --> PR_Passed: All Pass
    SecretsScan --> PR_Failed: Any Fail
    PythonCompile --> PR_Failed: Any Fail
    BackendTests --> PR_Failed: Any Fail
    FrontendTests --> PR_Failed: Any Fail
    PR_Failed --> [*]: Agent notified to fix
    PR_Passed --> WaitReview: Requires review
    PR_Passed --> AutoMerge: Has safe-automerge label
    WaitReview --> [*]: Human merges
    AutoMerge --> [*]: Workflow merges
```

### GitHub Actions Workflow

```mermaid
flowchart TD
    A[Tick Schedule: 15 min] -->|Dispatches| B(ai-factory-jules.yml)
    B --> C{Check AUTOPILOT_STOP}
    C -- Exists --> D[Halt Execution]
    C -- Not Found --> E[Determine Role based on hour]
    E --> F[Pop Task from task_queue.json]
    F --> G[Run Jules Agent]
    G --> H{Changes made?}
    H -- Yes --> I[Create PR & Run Validation]
    H -- No --> J[Mark as Completed Empty]
    I --> K[Check Safe Automerge]
    K -- Yes --> L[Merge PR]
    K -- No --> M[Wait for Review]
```
