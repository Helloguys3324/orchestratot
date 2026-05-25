
# Agent Instructions

This repository is maintained by autonomous coding agents and humans.

This file is the operating manual for all autonomous agents working in this repository.

Every agent must read this file before making changes.

Every agent must identify its assigned role and follow the rules for that role.

Every agent must respect task scopes, AI Factory ownership rules, validation requirements, and safety constraints.

---

# Project Shape

- `backend/` contains the FastAPI application and orchestration logic.
- `frontend/` contains static HTML/CSS/JS UI files.
- `skills_library/` and `custom_skills/` contain skill implementations.
- `data/` stores runtime JSON state. Do not commit real secrets.
- `.github/ai-factory/` contains autonomous development state and task planning files.
- `.github/workflows/` contains GitHub Actions workflows. Autonomous agents must not modify this directory unless explicitly assigned by a human-reviewed infrastructure task.
- `.github/scripts/` contains CI/CD helper scripts. Autonomous agents must not modify this directory unless explicitly assigned by a human-reviewed infrastructure task.

---

# Required Checks

Run these before proposing a code PR when practical:

Verify Python syntax, scan for secrets, run tests, and check JSON syntax. Test dependencies must be installed manually first. `PYTHONPATH=.` is required to resolve internal modules during local development. Clean up `.coverage` files to avoid accidentally committing them. Frontend tests use the native Node.js runner.

Note for AI Agents: Do not attempt to use `python -m venv` or source virtual environments within `run_in_bash_session`. Install required dependencies directly into the existing environment instead.

```bash
# Note: If guard_ai_workflows.py fails with an ambiguous Git error, see Troubleshooting Guide for the temporary empty commit workaround.
python -m compileall backend skills_library run.py
python .github/scripts/scan_secrets.py
python .github/scripts/guard_ai_workflows.py
pip install -q -r backend/requirements.txt
pip install -q pytest pytest-asyncio pytest-cov anyio
PYTHONPATH=. python -m pytest -q
node --experimental-test-coverage --test frontend/tests/*.test.js
rm -rf coverage/ frontend/coverage/ .coverage
# python -m json.tool <filepath>  # Run on specific JSON files to check syntax
```
*(Note for AI Agents: Native Node.js tests must always be executed during comprehensive validation, even if no frontend files were modified. Always run the full suite to get accurate coverage. Running a single file will falsely report lower overall coverage. When checking test coverage in an execution plan to verify 'no meaningful change', redirect the output to a temporary file outside the working directory (e.g., `> /tmp/coverage.txt 2>&1 && tail -n 25 /tmp/coverage.txt`) to ensure the coverage summary table is fully visible in the un-truncated bash output and to avoid accidentally modifying tracked repository files.)*

# Note: When exploring or verifying large JSON files, avoid using `cat` as its output may be truncated. Instead, use `jq` or a Python script.

If validation cannot be run, the PR body must clearly explain why.

Do not claim validation passed unless validation was actually run.

GitHub Actions validation is authoritative.

Agent-written validation claims are informational only.

***

# Change Rules

*   Keep changes focused and under 300 changed lines unless the task explicitly requires more.
*   Do not touch `data/settings.json` except to remove secrets or preserve the placeholder structure.
*   Do not create cosmetic-only PRs.
*   Do not update `.github/workflows/`, `.github/scripts/`, or `.github/CODEOWNERS`. AI Factory infrastructure changes require a human-reviewed PR.
*   Document behavior changes in `mission.md`, `README.md`, or `docs/ARCHITECTURE_STATE.md` when relevant.
*   Do not modify AI Factory global config unless the task explicitly allows it.
*   Do not modify task queue files unless the assigned role is `planner`.

***

# Pull Request Rules

Use a clear PR title beginning with one of:

```text
ai-factory(planner):
ai-factory(architect):
ai-factory(implementer):
ai-factory(tester):
ai-factory(reviewer):
ai-factory(refactorer):
ai-factory(documenter):
ai-factory(security):
```

Every PR must include:

```text
summary of changes
reason for changes
files changed
validation commands run
validation results
known limitations if any
```

Add the label:

```text
ai-factory:safe-automerge
```

only for docs-only or tests-only PRs that passed validation.

***

# Autonomous AI Factory Operating Manual

This repository is an autonomous AI Factory experiment.

The goal of this repository is to let multiple AI coding agents continuously improve the project through structured roles, scoped tasks, GitHub Actions, Jules, pull requests, validation workflows, and controlled automerge.

The goal is not to maximize commits.

The goal is not to create noise.

The goal is to maximize long-term project value.

The goal is to continuously make the repository better, safer, more tested, more documented, more maintainable, and more useful.

Every PR must leave the repository better than before.

***

# 1. Core Repository Mission

The repository is an autonomous multi-agent orchestrator project.

The project is expected to evolve through small, focused, reviewable tasks.

The AI Factory should continuously improve:

```text
backend reliability
frontend usability
test coverage
documentation quality
security posture
architecture clarity
skill implementation quality
runtime configuration
developer experience
automation quality
validation reliability
```

The AI Factory must avoid:

```text
chaotic rewrites
broken main branch
repeated duplicate tasks
meaningless cosmetic changes
unsafe automation
secret leaks
uncontrolled workflow changes
huge unreviewable pull requests
agents fighting over the same files
task queue corruption
invalid JSON
fake test results
filler tasks
```

***

# 2. Critical AI Factory Paths

Every agent must know these paths.

The AI Factory task queue is located at:

```text
.github/ai-factory/task_queue.json
```

The AI Factory runtime state is located at:

```text
.github/ai-factory/state.json
```

The AI Factory metrics file is located at:

```text
.github/ai-factory/metrics.json
```

The AI Factory config file is located at:

```text
.github/ai-factory/config.json
```

The emergency stop file is located at:

```text
AUTOPILOT_STOP
```

The architecture state document is located at:

```text
docs/ARCHITECTURE_STATE.md
```

The repository mission file may be located at:

```text
mission.md
```

The main agent instructions file is:

```text
AGENTS.md
```

The most important file for task planning is:

```text
.github/ai-factory/task_queue.json
```

The planner must always read and maintain:

```text
.github/ai-factory/task_queue.json
```

Worker roles must treat:

```text
.github/ai-factory/task_queue.json
```

as read-only unless the assigned role is explicitly `planner`.

***

# 3. Absolute Global Rules

These rules apply to every role.

No agent may ignore these rules.

1.  Keep every change small.
2.  Keep every change focused.
3.  Keep every pull request reviewable.
4.  Do not rewrite the whole project.
5.  Do not create broad unrelated refactors.
6.  Do not perform cosmetic-only changes unless the task explicitly asks for docs, formatting, cleanup, or UI polish.
7.  Do not commit secrets.
8.  Do not commit API keys.
9.  Do not commit passwords.
10. Do not commit tokens.
11. Do not commit cookies.
12. Do not commit private URLs.
13. Do not commit credentials.
14. Do not commit real production configuration.
15. Do not print secret values in logs.
16. Do not expose secrets in documentation.
17. Do not modify `.github/workflows/` unless the assigned task explicitly allows workflow changes.
18. Do not modify `.github/scripts/` unless the assigned task explicitly allows script changes.
19. Do not modify `.github/CODEOWNERS` unless the assigned task explicitly allows ownership changes.
20. Do not modify `data/settings.json` unless the assigned task explicitly allows settings changes.
21. Do not modify AI Factory config unless the assigned task explicitly allows it.
22. Do not change automation budgets unless the assigned task explicitly allows it.
23. Do not change scheduling rules unless the assigned task explicitly allows it.
24. Do not bypass validation.
25. Do not claim tests passed unless tests were actually run.
26. If tests were not run, clearly explain why.
27. Prefer deterministic tests.
28. Avoid external network calls in tests.
29. Mock external dependencies when practical.
30. Preserve existing behavior unless the task explicitly asks for behavior changes.
31. Respect the task `write_scope`.
32. Respect the task `avoid_scope`.
33. If a file is outside `write_scope`, do not modify it.
34. If a file is inside `avoid_scope`, do not modify it.
35. If a task is unclear, make the smallest safe improvement possible.
36. If a task is too broad, complete one useful atomic part and explain what remains.
37. If a change may be risky, keep automerge disabled.
38. Every PR must include a clear summary.
39. Every PR must include validation information.
40. Every PR must leave the repository better than before.
41. Critical: do not modify `.github/workflows/` or `.github/scripts/`. A CI/CD guard script is active. If these paths are touched without explicit permission, the PR may be automatically rejected.

***

# 4. AI Factory Ownership Model

The AI Factory uses strict ownership.

Different roles own different responsibilities.

This prevents chaos when many AI agents run every day.

***

## 4.1 Planner Owns The Backlog

Only the `planner` role may create, delete, archive, deduplicate, reorganize, rewrite, or reprioritize tasks in:

```text
.github/ai-factory/task_queue.json
```

The planner is the backlog owner.

The planner is the only role that should create new tasks.

The planner is the only role that should remove completed tasks.

The planner is the only role that should clean duplicate tasks.

The planner is the only role that should maintain the long-term task supply.

***

## 4.2 Workers Execute Tasks

Worker roles are:

```text
architect
implementer
tester
refactorer
documenter
security
reviewer
```

Worker roles must execute the selected task only.

Worker roles must not create new tasks.

Worker roles must not delete tasks.

Worker roles must not rewrite the task queue.

Worker roles must not change task priorities.

Worker roles must not change AI Factory config.

Worker roles must not change AI Factory schedules.

Worker roles must not change AI Factory global budgets.

Worker roles must not modify metrics unless explicitly assigned.

Worker roles must not modify runtime state unless explicitly assigned.

***

## 4.3 Workflows Record Runtime State

GitHub Actions workflows are responsible for runtime bookkeeping where possible.

Runtime bookkeeping includes:

```text
task_started
task_claimed
task_running
pr_created
validation_passed
validation_failed
pr_merged
pr_rejected
task_completed
task_failed
task_abandoned
```

Agents should focus on code, tests, docs, architecture, and task planning.

Workflows should focus on lifecycle tracking, metrics, and automation control.

***

# 5. Operational Control Protocols

The AI Factory must not rely only on agent honesty.

The AI Factory must use explicit operational protocols for backlog size, task claiming, validation, reviewer triggers, and planner runtime context.

***

## 5.1 Dynamic Backlog Policy

The planner must maintain a useful backlog, not a large backlog full of filler.

Default backlog targets:

```text
minimum_useful_pending_tasks: 30
target_useful_pending_tasks: 75
maximum_pending_tasks: 200
```

Planner rules:

1.  If fewer than 30 useful pending tasks exist, planner must generate new useful tasks.
2.  If 30 or more useful pending tasks exist, planner may generate new tasks only if they are clearly useful.
3.  If 75 or more useful pending tasks exist, planner should prioritize cleanup, deduplication, refinement, and quality improvement over raw generation.
4.  If 200 or more pending tasks exist, planner must stop generating tasks and must clean, merge, deduplicate, archive, or mark obsolete tasks.
5.  Planner must never create filler tasks to satisfy a number.
6.  A smaller backlog of useful tasks is better than a large backlog of vague tasks.
7.  Every new task must be justified by current repository needs.

Useful task sources include:

```text
missing tests
weak documentation
duplicated code
fragile backend logic
frontend UX gaps
security risks
architecture drift
recent merged PRs
TODO comments
missing validation
confusing setup instructions
weak error handling
missing type hints
uncovered edge cases
unhandled exceptions
manual setup pain points
```

***

## 5.2 Task Claim Protocol

Worker agents must not independently select tasks.

Only the orchestrator workflow may claim tasks.

Task lifecycle:

```text
pending -> claimed -> running -> completed
                  \-> failed
                  \-> abandoned
                  \-> blocked
```

Claim rules:

1.  The orchestrator reads `.github/ai-factory/task_queue.json` from `main`.
2.  The orchestrator selects a task with `"status": "pending"`.
3.  The orchestrator marks the task as claimed before launching the worker:
    *   `"status": "claimed"`
    *   `"claimed_by_run_id": "<github.run_id>"`
    *   `"claimed_at": "<current UTC timestamp>"`
4.  The orchestrator commits the claim to `main`.
5.  If the push fails because `main` moved, the orchestrator must pull/rebase and retry task selection.
6.  The worker receives the selected task in the prompt.
7.  The worker must execute only that selected task.
8.  The worker must not select another task.
9.  If the PR is created, the workflow may mark the task as `"running"`.
10. If the PR is merged, the automerge workflow marks the task as `"completed"`.
11. If validation fails, the validation workflow marks the task as `"failed"` or returns it to `"pending"` according to retry policy.
12. If a task remains `"claimed"` or `"running"` longer than the configured timeout, the workflow or planner may mark it `"abandoned"`.

Recommended timeout:

```text
claim_timeout_minutes: 180
```

***

## 5.3 Validation Enforcement Rule

Agent-written claims are not authoritative.

GitHub Actions validation is authoritative.

Rules:

1.  A PR is considered valid only if the validation workflow passes.
2.  Agent statements such as "tests passed" are informational only.
3.  If an agent says tests passed but CI fails, CI wins.
4.  If CI did not run, automerge must not happen unless the task is explicitly docs-only and the automerge workflow allows it.
5.  Automerge must depend on workflow check results, not on PR text.
6.  The validation workflow should enforce:
    *   no secrets committed;
    *   changed files are within `write_scope`;
    *   no `avoid_scope` files are touched;
    *   JSON files are valid;
    *   Python files compile;
    *   tests pass when relevant;
    *   workflow files are not changed unless allowed.
7.  If validation fails, the PR must not automerge.
8.  If validation fails repeatedly for the same lane, planner should create reviewer or tester tasks to investigate.

***

## 5.4 Reviewer Trigger Protocol

The reviewer role exists to detect drift, regressions, missing tests, documentation mismatch, and maintainability issues after changes have landed or after risky work has occurred.

Reviewer should run when one or more of these conditions are true:

1.  A PR was merged without enough tests.
2.  A PR changed backend behavior.
3.  A PR changed security-sensitive code.
4.  A PR touched architecture boundaries.
5.  A validation failure happened recently.
6.  Multiple PRs touched the same area.
7.  Documentation may be stale after recent changes.
8.  Planner detects architecture drift.
9.  Metrics show repeated failed tasks in one lane.
10. A completed task has weak or ambiguous acceptance evidence.
11. A high-risk PR was merged manually.
12. A refactor changed shared code.

Reviewer output must be one of:

```text
small corrective test PR
documentation correction PR
architecture drift note
small regression fix
review-only note if no safe code change is needed
```

Reviewer must not create broad new features.

Reviewer must not duplicate normal validation.

Reviewer should focus on second-order quality after changes have landed.

***

## 5.5 Planner Runtime Context Protocol

The planner must not assume it has direct access to complete GitHub history unless the workflow provides it.

When launching a planner task, the orchestrator should include a runtime context block.

The context should include, when available:

```text
recent merged PR titles
recent merged PR numbers
recent changed files
recent validation failures
current pending task count
current claimed task count
current running task count
current completed task count
current failed task count
recent task IDs
repository tree summary
recent files touched frequently
```

Example runtime context:

```text
[RUNTIME CONTEXT PROVIDED BY WORKFLOW]

Recent merged PRs:
- #16 ai-factory(tester): Add secondary backend smoke tests
- #15 ai-factory(documenter): Document API payload examples

Recent validation failures:
- none

Recently changed files:
- backend/tests/test_smoke.py
- docs/API_NOTES.md

Current queue stats:
- pending: 42
- claimed: 2
- running: 1
- completed: 18
- failed: 3
```

Planner rules:

1.  Planner must use provided runtime context when available.
2.  Planner must not invent PR history.
3.  Planner must not claim a PR was merged unless that information is visible in context or repository state.
4.  If runtime context is missing, planner may still inspect repository files and `task_queue.json`.
5.  If runtime context is insufficient, planner should create conservative tasks based on repository files, not imagined history.

***

# 6. Task Queue Contract

The canonical backlog file is:

```text
.github/ai-factory/task_queue.json
```

The planner must maintain this file.

Worker roles must read selected tasks from this file or from the prompt created by the workflow.

Every active task should have this structure:

```json
{
  "id": "unique-task-id",
  "role": "implementer",
  "lane": "backend",
  "title": "Short task title",
  "status": "pending",
  "priority": 50,
  "created_by": "planner",
  "write_scope": [],
  "avoid_scope": [],
  "risk_level": "low",
  "automerge_allowed": false,
  "prompt": "[INPUT STATE] ...\n[ATOMIC OBJECTIVE] ...\n[CONSTRAINTS] ...\n[ACCEPTANCE CRITERIA] ..."
}
```

Recommended task statuses:

```text
pending
claimed
running
completed
failed
obsolete
duplicate
blocked
abandoned
```

The active `tasks` array should contain only useful work that still needs to be done.

Completed tasks should not remain active as pending tasks.

Duplicate tasks should not remain active as pending tasks.

Obsolete tasks should not remain active as pending tasks.

Tasks already satisfied by the repository should not remain active as pending tasks.

***

# 7. Required Prompt Protocol

Every generated task prompt must follow this exact 4-part structure:

```text
[INPUT STATE]
Describe what repository context the agent should inspect.

[ATOMIC OBJECTIVE]
Describe exactly one focused objective.

[CONSTRAINTS]
Describe allowed files, forbidden files, behavior limits, testing limits, safety limits, and scope limits.

[ACCEPTANCE CRITERIA]
Describe what must be true when the task is complete.
```

Bad task examples:

```text
Improve code.
Fix everything.
Make project better.
Optimize backend.
Refactor frontend.
Clean the repo.
Improve tests.
Improve docs.
Make security better.
```

Good task examples:

```text
Add deterministic tests for backend/skills/manager.py invalid skill metadata handling.
Document request and response payload examples for session creation API.
Refactor duplicated frontend modal error rendering into a shared helper.
Harden path validation in skills_library/file_manager.py.
Add smoke tests for backend model registry retrieval.
Document local development setup for FastAPI backend.
Improve error response formatting for one backend endpoint.
Add validation test for missing runtime configuration.
```

Every task must be atomic.

Every task must be scoped.

Every task must be useful.

Every task must have clear acceptance criteria.

***

# 8. Emergency Stop

If this file exists:

```text
AUTOPILOT_STOP
```

AI Factory automation must stop spawning new tasks.

Agents must not remove:

```text
AUTOPILOT_STOP
```

unless explicitly instructed by the repository owner.

If an agent sees `AUTOPILOT_STOP`, the agent must treat it as a hard stop signal.

The existence of `AUTOPILOT_STOP` means:

```text
Do not spawn new autonomous work.
Do not continue autonomous loops.
Do not bypass the stop.
```

***

# 9. Planner Role

## 9.1 Planner Identity

The planner is the backlog owner.

The planner manages the task supply.

The planner does not build application features directly.

The planner does not write backend code.

The planner does not write frontend code.

The planner does not write skill code.

The planner maintains the AI Factory backlog.

The planner's main file is:

```text
.github/ai-factory/task_queue.json
```

***

## 9.2 Planner Must Read

The planner must inspect these files when available:

```text
mission.md
AGENTS.md
.github/ai-factory/task_queue.json
.github/ai-factory/state.json
.github/ai-factory/metrics.json
.github/ai-factory/config.json
docs/ARCHITECTURE_STATE.md
README.md
```

The planner should inspect repository structure.

The planner should inspect runtime context provided by workflow when available.

The planner should inspect recent merged work only when that information is available in runtime context, repository state, or visible files.

The planner must not invent merged PR history.

The planner should inspect existing tests.

The planner should inspect documentation.

The planner should inspect backend modules.

The planner should inspect frontend modules.

The planner should inspect skills modules.

***

## 9.3 Planner Main Responsibilities

The planner must:

1.  Maintain the task queue.
2.  Create useful new tasks only when justified by Dynamic Backlog Policy.
3.  Remove completed tasks.
4.  Remove duplicate tasks.
5.  Remove obsolete tasks.
6.  Mark blocked tasks where needed.
7.  Keep the backlog useful.
8.  Keep task prompts high quality.
9.  Keep role distribution balanced.
10. Keep task scopes safe.
11. Keep task IDs unique.
12. Keep JSON valid.
13. Keep tasks atomic.
14. Keep tasks reviewable.
15. Keep tasks aligned with repository needs.
16. Keep dangerous tasks non-automerge.
17. Keep docs/tests-only safe tasks eligible for automerge where appropriate.
18. Avoid filler work.

***

## 9.4 Planner Backlog Generation Rule

The planner must follow the Dynamic Backlog Policy.

Default backlog targets:

```text
minimum_useful_pending_tasks: 30
target_useful_pending_tasks: 75
maximum_pending_tasks: 200
```

Planner behavior:

1.  If fewer than 30 useful pending tasks exist, add useful tasks until the backlog reaches at least 30 useful pending tasks.
2.  If 30 or more useful pending tasks exist, add new tasks only if they are clearly useful and grounded in repository needs.
3.  If 75 or more useful pending tasks exist, prioritize cleanup, deduplication, refinement, and quality improvement over generation.
4.  If 200 or more pending tasks exist, do not generate new tasks. Clean, deduplicate, archive, or mark obsolete tasks instead.
5.  Never create filler tasks just to satisfy a number.
6.  A smaller backlog of useful tasks is better than a larger backlog of vague tasks.

Good sources for new tasks:

```text
missing tests
weak documentation
duplicated code
fragile backend logic
frontend UX gaps
security risks
architecture drift
recent merged PRs from provided runtime context
TODO comments
missing validation
confusing setup instructions
weak error handling
missing type hints
uncovered edge cases
unhandled exceptions
manual setup pain points
```

***

## 9.5 Mandatory Planner Cleanup Rule

Every planner run must check for tasks that are already completed.

The planner must remove, archive, or mark completed tasks.

A task may be considered completed if:

1.  A merged PR clearly implemented it and that merged PR is visible in runtime context or repository state.
2.  The repository already contains the requested tests.
3.  The repository already contains the requested docs.
4.  The repository already contains the requested feature.
5.  The repository already contains the requested refactor.
6.  The repository already contains the requested security fix.
7.  The acceptance criteria are already satisfied.
8.  A newer task made it obsolete.
9.  It duplicates another active or completed task.

The planner must not keep completed work active as pending work.

Recommended cleanup strategy:

```text
completed task
-> move to completed_tasks or mark "completed"

duplicate task
-> remove duplicate or mark "duplicate"

obsolete task
-> remove obsolete task or mark "obsolete"

blocked task
-> keep only if still useful and set status "blocked"
```

If useful, planner may maintain:

```json
"completed_tasks": []
```

Completed task archive entries should be compact:

```json
{
  "id": "tester-backend-smoke-v2",
  "completed_at": "2026-05-16T00:00:00Z",
  "reason": "Smoke tests already added and merged",
  "source": "planner-cleanup"
}
```

Do not let `completed_tasks` grow forever without compaction.

***

## 9.6 Planner Must Not

The planner must not:

1.  Modify `backend/`.
2.  Modify `frontend/`.
3.  Modify `skills_library/`.
4.  Modify `custom_skills/`.
5.  Modify application code.
6.  Modify workflow files unless explicitly assigned by a human-reviewed infrastructure task.
7.  Modify GitHub scripts unless explicitly assigned by a human-reviewed infrastructure task.
8.  Modify CODEOWNERS unless explicitly assigned.
9.  Modify secrets.
10. Modify private settings.
11. Create vague tasks.
12. Create duplicate tasks.
13. Create tasks without `write_scope`.
14. Create tasks without `avoid_scope`.
15. Create high-risk tasks with automerge enabled.
16. Generate meaningless filler work.
17. Reset the whole task queue without reason.
18. Destroy useful task history without reason.
19. Invent PR history.
20. Claim a task is completed by a merged PR unless that PR is visible in runtime context or repository state.

***

## 9.7 Planner Role Distribution Target

Planner should maintain this approximate backlog distribution:

```text
implementer: 35%
tester: 20%
documenter: 10%
refactorer: 10%
security: 10%
architect: 10%
reviewer: 5%
```

Planner may adjust the distribution based on actual repository needs.

If test coverage is weak, create more tester tasks.

If documentation is weak, create more documenter tasks.

If backend structure is unstable, create more architect and refactorer tasks.

If security posture is weak, create more security tasks.

If recent PRs are noisy or risky, create reviewer tasks only when Reviewer Trigger Protocol applies.

***

## 9.8 Planner Lanes

Planner should distribute work across lanes:

```text
backend
frontend
skills
tests
docs
security
architecture
workflow
```

Workflow tasks must be rare.

Workflow tasks must have:

```json
"automerge_allowed": false
```

Workflow tasks must have a very narrow write scope.

Workflow tasks require human review.

***

## 9.9 Planner Task Template

New tasks should look like this:

```json
{
  "id": "tester-skills-manager-errors-v1",
  "role": "tester",
  "lane": "tests",
  "title": "Add deterministic tests for skills manager errors",
  "status": "pending",
  "priority": 70,
  "created_by": "planner",
  "write_scope": [
    "tests/",
    "backend/skills/"
  ],
  "avoid_scope": [
    "frontend/",
    ".github/workflows/",
    ".github/scripts/",
    ".github/CODEOWNERS",
    "data/settings.json"
  ],
  "risk_level": "low",
  "automerge_allowed": true,
  "prompt": "[INPUT STATE] Current backend/skills/manager.py behavior and existing tests.\n[ATOMIC OBJECTIVE] Add deterministic unit tests for skill loading error handling.\n[CONSTRAINTS] Touch only tests/ and backend/skills/. Avoid external network calls. Preserve behavior.\n[ACCEPTANCE CRITERIA] Tests cover missing skill, invalid skill metadata, and successful skill loading without external dependencies."
}
```

***

# 10. Architect Role

## 10.1 Architect Identity

The architect improves system boundaries, module responsibilities, architecture documentation, and long-term maintainability.

The architect thinks about structure.

The architect avoids large rewrites.

The architect keeps behavior stable.

***

## 10.2 Architect Usually May Work On

Only if allowed by `write_scope`, the architect may work on:

```text
backend/
docs/
docs/ARCHITECTURE_STATE.md
```

***

## 10.3 Architect Must

1.  Keep behavior stable.
2.  Prefer small architecture improvements.
3.  Clarify module boundaries.
4.  Document architectural decisions.
5.  Update `docs/ARCHITECTURE_STATE.md` when relevant.
6.  Avoid broad rewrites.
7.  Explain architecture impact in the PR.
8.  Avoid speculative redesign.
9.  Keep changes reviewable.
10. Respect `write_scope`.
11. Respect `avoid_scope`.

***

## 10.4 Architect Must Not

1.  Modify `task_queue.json`.
2.  Create new tasks.
3.  Modify AI Factory config.
4.  Modify metrics.
5.  Modify workflows unless explicitly assigned by a human-reviewed infrastructure task.
6.  Modify frontend unless explicitly assigned.
7.  Modify secrets.
8.  Modify runtime settings unless explicitly assigned.
9.  Rewrite the project architecture in one PR.
10. Introduce new dependencies without a clear reason.

***

## 10.5 Good Architect Work

Good architect work includes:

```text
small module boundary improvement
ADR documentation
architecture state update
dependency direction clarification
responsibility cleanup
removing circular dependency
clarifying service ownership
documenting orchestration flow
architecture drift correction
```

***

# 11. Implementer Role

## 11.1 Implementer Identity

The implementer builds focused functionality.

The implementer changes backend, frontend, skills, or runtime behavior only when assigned.

The implementer does exactly one selected task.

***

## 11.2 Implementer Usually May Work On

Only if allowed by `write_scope`, the implementer may work on:

```text
backend/
frontend/
skills_library/
custom_skills/
tests/
.env.example
```

***

## 11.3 Implementer Must

1.  Implement exactly the selected task.
2.  Keep the diff small.
3.  Preserve existing behavior unless explicitly changing behavior.
4.  Add tests when practical.
5.  Avoid unrelated cleanup.
6.  Avoid broad refactors.
7.  Document non-obvious behavior.
8.  Keep public APIs stable unless explicitly assigned.
9.  Explain behavior changes in the PR.
10. Respect `write_scope`.
11. Respect `avoid_scope`.
12. Avoid network-dependent tests.
13. Avoid real credentials.
14. Use simple maintainable code.
15. Prefer type hints in Python where practical.

***

## 11.4 Implementer Must Not

1.  Modify `task_queue.json`.
2.  Create new tasks.
3.  Modify global metrics.
4.  Modify `state.json`.
5.  Modify `config.json`.
6.  Modify workflows unless explicitly assigned by a human-reviewed infrastructure task.
7.  Change AI Factory scheduling.
8.  Change AI Factory budgets.
9.  Touch files outside `write_scope`.
10. Touch files inside `avoid_scope`.
11. Add hidden background network behavior.
12. Add secret-like placeholder values that look real.

***

# 12. Tester Role

## 12.1 Tester Identity

The tester improves deterministic validation and test coverage.

The tester adds tests.

The tester improves test reliability.

The tester does not do broad production rewrites.

***

## 12.2 Tester Usually May Work On

Only if allowed by `write_scope`, the tester may work on:

```text
tests/
backend/tests/
frontend tests if present
backend/ testability helpers if explicitly allowed
```

***

## 12.3 Tester Must

1.  Prefer deterministic tests.
2.  Avoid external network calls.
3.  Avoid real credentials.
4.  Mock external dependencies.
5.  Keep production behavior unchanged unless a tiny testability fix is necessary and allowed.
6.  Explain what behavior is covered.
7.  Avoid flaky timing-sensitive tests.
8.  Keep tests focused.
9.  Run relevant tests when practical.
10. Respect `write_scope`.
11. Respect `avoid_scope`.
12. Use meaningful assertions.
13. Avoid tests that only check implementation details.
14. Avoid tests that require local private state.

***

## 12.4 Tester Must Not

1.  Modify `task_queue.json`.
2.  Create new tasks.
3.  Modify workflows unless explicitly assigned by a human-reviewed infrastructure task.
4.  Make large production code changes.
5.  Add flaky tests.
6.  Depend on local-only state.
7.  Require private environment variables.
8.  Fake test results.
9.  Claim validation passed if validation did not run.
10. Touch AI Factory metrics unless explicitly assigned.

***

## 12.5 Tester Automerge

Tester PRs may be automerged only if:

```text
automerge_allowed = true
validation passes
changed files are within write_scope
no avoid_scope paths are touched
no secrets are added
no risky production behavior changes are included
```

***

# 13. Refactorer Role

## 13.1 Refactorer Identity

The refactorer improves readability, maintainability, structure, and duplication without changing behavior.

The refactorer does not add features.

The refactorer does not change behavior unless explicitly assigned.

***

## 13.2 Refactorer Usually May Work On

Only if allowed by `write_scope`, the refactorer may work on:

```text
backend/
frontend/
skills_library/
tests/
```

***

## 13.3 Refactorer Must

1.  Preserve behavior.
2.  Keep changes small.
3.  Avoid large rewrites.
4.  Add or update tests when practical.
5.  Explain why the refactor reduces complexity.
6.  Avoid mixing refactor with feature work.
7.  Keep public APIs stable unless explicitly assigned.
8.  Respect `write_scope`.
9.  Respect `avoid_scope`.
10. Avoid formatting-only rewrites across many files.
11. Avoid unrelated cleanup.
12. Keep naming consistent.
13. Keep imports clean.
14. Keep code simple.

***

## 13.4 Refactorer Must Not

1.  Modify `task_queue.json`.
2.  Create new tasks.
3.  Modify workflows unless explicitly assigned by a human-reviewed infrastructure task.
4.  Change public APIs unless explicitly assigned.
5.  Change settings.
6.  Change secrets.
7.  Rewrite entire modules without reason.
8.  Mix unrelated refactors.
9.  Introduce new dependencies without reason.
10. Touch AI Factory state unless explicitly assigned.

***

# 14. Documenter Role

## 14.1 Documenter Identity

The documenter improves documentation.

The documenter improves README files, setup guides, API examples, architecture docs, and operational instructions.

The documenter does not change application code.

***

## 14.2 Documenter Usually May Work On

Only if allowed by `write_scope`, the documenter may work on:

```text
README.md
docs/
AGENTS.md
mission.md
.env.example
```

***

## 14.3 Documenter Must

1.  Keep documentation accurate.
2.  Reflect current repository state.
3.  Include commands only if valid for the repo.
4.  Avoid inventing features.
5.  Document setup clearly.
6.  Document validation clearly.
7.  Document secrets handling clearly.
8.  Document operations clearly.
9.  Avoid changing application code.
10. Keep docs concise but complete.
11. Update examples only when supported by implementation.
12. Respect `write_scope`.
13. Respect `avoid_scope`.
14. Avoid misleading claims.
15. Avoid stale instructions.
16. Document the existence and purpose of `AUTOPILOT_STOP` clearly in setup guides.

***

## 14.4 Documenter Must Not

1.  Modify `task_queue.json` unless role is planner.
2.  Modify backend code.
3.  Modify frontend code.
4.  Modify workflows unless explicitly assigned by a human-reviewed infrastructure task.
5.  Create new tasks.
6.  Invent unsupported API behavior.
7.  Document non-existent commands as working.
8.  Modify metrics.
9.  Modify runtime state.
10. Change budgets or schedules.

***

## 14.5 Documenter Automerge

Documenter PRs may be automerged only if:

```text
automerge_allowed = true
only docs files changed
validation passes
no misleading instructions are added
no application code is changed
```

***

# 15. Security Role

## 15.1 Security Identity

The security role finds and fixes narrow security risks.

Security changes must be careful.

Security changes must be scoped.

Security changes should usually not automerge.

***

## 15.2 Security Usually May Work On

Only if allowed by `write_scope`, the security role may work on:

```text
backend/
skills_library/
tests/
.env.example
```

***

## 15.3 Security Must

1.  Focus on one concrete risk per task.
2.  Avoid broad rewrites.
3.  Add tests for security-sensitive behavior when practical.
4.  Never commit secrets.
5.  Never expose secrets in logs.
6.  Avoid unsafe shell execution.
7.  Harden path handling where relevant.
8.  Harden file access where relevant.
9.  Harden input validation where relevant.
10. Harden command execution where relevant.
11. Keep automerge disabled for high-risk changes.
12. Prefer narrow testable fixes.
13. Explain risk and mitigation in the PR.
14. Respect `write_scope`.
15. Respect `avoid_scope`.
16. Avoid adding hidden network behavior.
17. Avoid over-restricting behavior without tests.

***

## 15.4 Security Must Not

1.  Modify `task_queue.json`.
2.  Create new tasks.
3.  Modify workflows unless explicitly assigned by a human-reviewed infrastructure task.
4.  Add aggressive restrictions that break normal behavior without tests.
5.  Commit real credentials.
6.  Commit secret-like values.
7.  Print secret values.
8.  Add hidden network behavior.
9.  Modify global AI Factory config.
10. Touch files outside scope.

***

# 16. Reviewer Role

## 16.1 Reviewer Identity

The reviewer checks recent changes for regressions, drift, missing tests, documentation mismatch, and maintainability issues.

The reviewer makes small corrective PRs or review-only notes.

The reviewer does not create broad new features.

The reviewer is not a duplicate of CI validation.

The reviewer focuses on second-order quality after changes have landed or after risky work occurred.

***

## 16.2 Reviewer Trigger Rules

Reviewer should run only when there is a concrete reason.

Reviewer triggers:

1.  A PR was merged without enough tests.
2.  A PR changed backend behavior.
3.  A PR changed security-sensitive code.
4.  A PR touched architecture boundaries.
5.  A validation failure happened recently.
6.  Multiple PRs touched the same area.
7.  Documentation may be stale after recent changes.
8.  Planner detects architecture drift.
9.  Metrics show repeated failed tasks in one lane.
10. A completed task has weak or ambiguous acceptance evidence.
11. A high-risk PR was merged manually.
12. A refactor changed shared code.

Reviewer output must be one of:

```text
small corrective test PR
documentation correction PR
architecture drift note
small regression fix
review-only note if no safe code change is needed
```

***

## 16.3 Reviewer Usually May Work On

Only if allowed by `write_scope`, the reviewer may work on:

```text
docs/
tests/
small corrective files if explicitly allowed
```

***

## 16.4 Reviewer Must

1.  Review recent merged work when available in runtime context or repository state.
2.  Identify concrete issues.
3.  Prefer documentation corrections.
4.  Prefer test additions.
5.  Prefer small safe fixes.
6.  Avoid large feature work.
7.  Avoid rewriting code unnecessarily.
8.  Keep PRs small.
9.  Explain what was reviewed.
10. Explain what was corrected.
11. Respect `write_scope`.
12. Respect `avoid_scope`.
13. Avoid speculative changes.
14. Avoid unrelated cleanup.
15. Produce one of the approved reviewer outputs.

***

## 16.5 Reviewer Must Not

1.  Modify `task_queue.json`.
2.  Create new tasks.
3.  Modify workflows unless explicitly assigned by a human-reviewed infrastructure task.
4.  Perform large refactors.
5.  Make speculative changes.
6.  Revert unrelated work.
7.  Modify AI Factory config.
8.  Modify metrics.
9.  Modify budgets.
10. Modify schedules.
11. Duplicate normal CI validation.

***

# 17. Worker Task Execution Protocol

All non-planner roles must follow this protocol.

1.  Read the selected task.
2.  Identify:

```text
id
role
lane
title
write_scope
avoid_scope
risk_level
automerge_allowed
prompt
```

3.  Confirm the assigned role matches the task role.
4.  Modify only files in `write_scope`.
5.  Avoid all paths in `avoid_scope`.
6.  Do not modify:

```text
.github/ai-factory/task_queue.json
.github/ai-factory/state.json
.github/ai-factory/metrics.json
.github/ai-factory/config.json
```

unless the assigned role is `planner`.

7.  Do not create new tasks.
8.  Do not delete tasks.
9.  Do not change global budgets.
10. Do not change schedules.
11. Do not change workflow files unless explicitly assigned by a human-reviewed infrastructure task.
12. Run relevant validation when practical.
13. Create a focused PR.
14. Include a clear PR summary.
15. Include tests run or explain why tests were not run.
16. If unable to complete the task, make the smallest useful improvement and explain the limitation.
17. If the task is unsafe, do not perform the unsafe part.
18. If the task conflicts with scope, follow the scope.
19. Do not independently select another task.
20. Execute only the task selected by the workflow.

***

# 18. Planner Task Execution Protocol

Planner must follow this exact protocol.

1.  Open:

```text
.github/ai-factory/task_queue.json
```

2.  Validate that the JSON is valid.
3.  Use runtime context if provided by workflow.
4.  Do not invent missing runtime context.
5.  Count pending tasks.
6.  Count claimed tasks.
7.  Count running tasks.
8.  Count completed tasks if present.
9.  Count failed tasks if present.
10. Count duplicate tasks.
11. Detect obsolete tasks.
12. Detect blocked tasks.
13. Detect vague tasks.
14. Detect tasks missing required fields.
15. Detect tasks with invalid scopes.
16. Detect high-risk automerge tasks.
17. Remove, archive, or mark completed tasks.
18. Remove or mark duplicate tasks.
19. Remove or mark obsolete tasks.
20. Fix tasks missing required fields.
21. Improve vague tasks.
22. Add new useful tasks only according to Dynamic Backlog Policy.
23. Ensure task IDs are unique.
24. Ensure every task has valid fields.
25. Ensure every task prompt follows the 4-part protocol.
26. Ensure no worker task can modify dangerous files unless explicitly intended.
27. Ensure high-risk tasks have automerge disabled.
28. Preserve valid JSON.
29. Do not modify application code.
30. Summarize backlog changes in the PR.
31. Critical: the updated `task_queue.json` must be strictly valid RFC 8259 JSON.
32. No trailing commas.
33. All strings must be properly escaped.
34. Double-check JSON syntax before saving.

***

# 19. Completed Task Cleanup Rules

Planner must remove or archive completed tasks.

A task may be considered completed if:

1.  A merged PR clearly implemented the task and that merged PR is visible in runtime context or repository state.
2.  The repository already contains the requested tests.
3.  The repository already contains the requested docs.
4.  The repository already contains the requested feature.
5.  The repository already contains the requested refactor.
6.  The repository already contains the requested security fix.
7.  The task acceptance criteria are already satisfied.
8.  The task is made obsolete by newer implementation.
9.  The task duplicates another completed or pending task.

Planner must not keep completed tasks active as pending.

Recommended cleanup strategy:

```text
pending task completed by repo state
-> move to completed_tasks or remove from active tasks

duplicate task
-> remove duplicate or mark "duplicate"

obsolete task
-> mark "obsolete" or remove

blocked task
-> keep only if still valuable and set status "blocked"
```

If `completed_tasks` does not exist and historical tracking is useful, planner may add:

```json
"completed_tasks": []
```

Completed task archive entries should be compact:

```json
{
  "id": "tester-backend-smoke-v2",
  "completed_at": "2026-05-16T00:00:00Z",
  "reason": "Smoke tests already added and merged",
  "source": "planner-cleanup"
}
```

The planner should compact completed task history when it becomes too large.

***

# 20. Automerge Policy

Automerge is allowed only for low-risk work.

Usually safe for automerge:

```text
docs-only tasks
tests-only tasks
small deterministic test additions
minor documentation updates
small non-runtime metadata updates
```

Usually not safe for automerge:

```text
security changes
runtime config changes
backend behavior changes
frontend behavior changes
workflow changes
architecture changes
large refactors
dependency changes
settings changes
```

A PR may be automerged only if all conditions are true:

```text
validation passes
changed files are within write_scope
no avoid_scope paths are touched
no secrets are added
risk_level is low
automerge_allowed is true
PR is small and focused
```

If unsure, set:

```json
"automerge_allowed": false
```

***

# 21. Validation Policy

Agents should run relevant validation when practical.

Recommended validation examples:

```text
# Note: If guard_ai_workflows.py fails with an ambiguous Git error, see Troubleshooting Guide for the temporary empty commit workaround.
python -m compileall backend skills_library run.py
python .github/scripts/scan_secrets.py
python .github/scripts/guard_ai_workflows.py

# Note for AI Agents: Do not attempt to use `python -m venv` or source virtual environments within `run_in_bash_session`.
# Install required dependencies directly into the existing environment instead:
pip install -q -r backend/requirements.txt
pip install -q pytest pytest-asyncio pytest-cov anyio
PYTHONPATH=. python -m pytest -q
node --experimental-test-coverage --test frontend/tests/*.test.js
rm -rf coverage/ frontend/coverage/ .coverage
# python -m json.tool <filepath>  # Run on specific JSON files to check syntax
```

If validation commands exist in:

```text
.github/ai-factory/config.json
```

agents should follow those commands when practical.

If a command fails, the agent must report the failure.

If a command cannot be run, the agent must explain why.

Agents must not claim success without running validation.

GitHub Actions validation is authoritative.

Agent statements are not final proof of correctness.

***

# 22. Secrets Policy

Never commit real secrets.

Never commit API keys.

Never commit tokens.

Never commit passwords.

Never commit cookies.

Never commit private URLs.

Never log secret values.

Never include secrets in examples.

Use placeholders like:

```text
YOUR_API_KEY_HERE
EXAMPLE_TOKEN
REPLACE_ME
```

Do not use realistic-looking secret values.

Do not modify secret-handling logic unless assigned.

Security-sensitive changes should include tests.

***

# 23. Scope Policy

Every task has `write_scope`.

Every task has `avoid_scope`.

Agents must obey both.

If a file is not in `write_scope`, do not edit it.

If a file is in `avoid_scope`, do not edit it.

If the task requires editing a file outside `write_scope`, do not edit it unless the prompt explicitly allows it.

If scope conflicts with the task objective, do the safe scoped portion and explain the limitation.

Worker roles must not modify:

```text
.github/ai-factory/task_queue.json
.github/ai-factory/state.json
.github/ai-factory/metrics.json
.github/ai-factory/config.json
```

Planner may modify:

```text
.github/ai-factory/task_queue.json
```

Planner should not modify runtime metrics unless explicitly assigned.

***

# 24. PR Quality Policy

Every PR should include:

```text
summary of changes
reason for changes
files changed
tests run
validation result
known limitations if any
```

Good PRs are:

```text
small
focused
scoped
safe
tested when practical
easy to review
aligned with task
```

Bad PRs are:

```text
huge
unrelated
untested
vague
cosmetic-only without reason
outside scope
workflow-changing without permission
secret-leaking
```

***

# 25. Backend Guidelines

Backend changes should be:

```text
typed when practical
small
tested when practical
compatible with existing API behavior
clear about error handling
safe with user input
careful with file access
careful with command execution
```

Backend agents should avoid:

```text
large rewrites
hidden global state
silent exception swallowing
unvalidated input
unsafe shell commands
hardcoded secrets
network-dependent tests
breaking public endpoints without reason
```

***

# 26. Frontend Guidelines

Frontend changes should be:

```text
small
visual-layout-preserving unless UI task
clear in error handling
consistent with existing JS structure
compatible with existing backend API
safe for missing or malformed API responses
```

Frontend agents should avoid:

```text
large rewrites
unrelated styling changes
breaking existing interactions
inventing backend endpoints
duplicating utility logic
hiding errors without explanation
```

***

# 27. Skills Guidelines

Skill changes should be:

```text
guarded
testable
safe with file paths
safe with user input
clear about errors
deterministic where possible
```

Skill agents should avoid:

```text
unsafe code execution
unsafe path traversal
uncontrolled network calls
secret leaks
silent failures
unbounded file access
```

***

# 28. Documentation Guidelines

Documentation should be:

```text
accurate
current
clear
useful
not misleading
not overpromising
```

Documentation should include:

```text
setup instructions
run commands
validation commands
environment variable guidance
secrets handling
architecture notes
API examples when supported
GitHub Actions and CI/CD context
```

Documentation must not invent features.

Documentation must not claim commands work if not verified or clearly supported.

***

# 29. Testing Guidelines

Tests should be:

```text
deterministic
focused
fast when possible
mocked when needed
clear in assertions
safe for CI
not dependent on private state
not dependent on external network
```

Tests should avoid:

```text
real API calls
real credentials
timing flakiness
environment-specific assumptions
hidden dependencies
```

***

# 30. Security Guidelines

Security changes must be narrow.

Security changes must be testable when practical.

Security changes must not silently break expected behavior.

Security changes must not expose secrets.

Security changes must be extra careful around:

```text
path traversal
file access
command execution
environment variables
logs
API keys
user input
uploads
dynamic imports
code execution
web search
external processes
```

***

# 31. Factory Health Principles

The AI Factory should optimize for:

```text
useful improvements
small PRs
clear tests
clear documentation
safe automation
low conflict rate
high merge quality
minimal duplicated work
stable main branch
steady useful backlog
healthy role distribution
technical quality
```

The AI Factory should avoid:

```text
large chaotic rewrites
duplicate PRs
meaningless cosmetic commits
unbounded task generation
filler tasks
editing workflows without reason
changing secrets or settings
breaking validation
touching files outside write_scope
agents modifying task queue without planner role
```

***

# 32. Final Agent Checklist

Before finishing, every agent must ask:

```text
Did I follow my assigned role?
Did I modify only allowed files?
Did I avoid forbidden files?
Did I keep the change small?
Did I avoid secrets?
Did I preserve behavior unless assigned otherwise?
Did I run relevant validation when practical?
Did I explain tests run?
Did I explain what changed?
Did I avoid changing task_queue unless planner?
Did I leave the repository better than before?
```

If the answer is no, fix the issue before finishing.

***

# 33. Final Rule

If the task is a planner task:

```text
improve the backlog
apply Dynamic Backlog Policy
create new useful tasks only when needed
remove completed tasks
remove duplicates
remove obsolete tasks
avoid filler tasks
preserve valid JSON
```

If the task is a worker task:

```text
execute only the selected task
do not create new tasks
do not modify task_queue.json
respect write_scope
respect avoid_scope
```

If the task is unsafe or unclear:

```text
make the smallest safe improvement
explain the uncertainty
do not perform unsafe actions
```


# 34. World-Class Product Quality Directive

This repository must be treated as a serious product, not as a toy experiment.

Every agent should aim for the quality level expected from a top-tier product engineering team.

The goal is to make this project feel like a premium autonomous AI orchestration platform.

The product should feel:

```text
polished
fast
trustworthy
clear
beautiful
developer-grade
AI-native
well-documented
well-tested
architecturally understandable
impressive to first-time visitors
````

Agents should not only ask:

```text
Does this work?
```

Agents must also ask:

```text
Is this clear?
Is this maintainable?
Is this visually polished?
Is this understandable?
Is this safe?
Is this impressive?
Is this useful?
Would a strong engineer respect this implementation?
Would a first-time visitor understand why this project matters?
```

The repository should gradually evolve into something that makes a visitor think:

```text
This is not just an automation test.
This is a serious autonomous AI engineering system.
The UI is polished.
The docs are clear.
The architecture is visible.
The automation is impressive.
The project feels alive.
```

***

# 35. Product Experience Vision

The product experience should communicate that this repository is an autonomous AI software factory.

A first-time visitor should quickly understand:

```text
what the project does
why the project is interesting
how autonomous agents work
how tasks are planned
how tasks are executed
how PRs are validated
how automerge is controlled
how safety is enforced
how the system can run continuously
how humans can supervise it
```

The project should eventually have a strong product surface, including:

```text
premium dashboard UI
clear README
architecture diagrams
agent role diagrams
task lifecycle diagrams
workflow diagrams
automation health views
task queue visibility
metrics visibility
developer setup clarity
security boundaries
validation flow explanation
```

Every agent should help move the repository toward that vision.

***

# 36. Product Quality Levels

Agents should think in quality levels.

## Level 1: Functional

The feature works.

This is the minimum acceptable level.

## Level 2: Reliable

The feature works consistently, has validation, and handles errors.

This is the expected level for backend, tests, and security work.

## Level 3: Understandable

The feature is documented, named clearly, and fits the architecture.

This is expected for maintainable work.

## Level 4: Polished

The feature has good UX, good visual hierarchy, clear states, and a professional feel.

This is expected for frontend and docs work.

## Level 5: World-Class

The feature feels like a premium product experience.

It is useful, polished, fast, clear, safe, well-documented, and impressive.

This is the long-term target.

Agents should always try to move work one level higher without creating unnecessary complexity.

***

# 37. Inspiration Policy

Agents may use public products and design references as inspiration for quality standards.

Agents must not clone any product.

Agents must not copy exact layouts, copywriting, colors, icons, illustrations, animations, brand identity, or trade dress.

Use references only as quality inspiration.

Acceptable inspiration categories:

```text
premium SaaS dashboards
developer tools
AI command centers
analytics dashboards
observability products
automation platforms
documentation sites
award-level web design
modern product landing pages
real-world app UI patterns
```

Acceptable quality references:

```text
Linear-style clarity and productivity
Stripe-style trust and documentation polish
Vercel-style developer experience
Raycast-style command center feel
Notion-style information organization
Figma-style collaboration clarity
GitHub-style developer workflow clarity
modern SaaS dashboard visual hierarchy
award-level web design ambition
```

Agents must create an original design language for this repository.

The project must look like itself.

The project must not look like a copy of another product.

***

# 38. UI/UX North Star

The UI should eventually feel like a premium AI Factory command center.

The UI should make complex automation understandable.

The UI should help users answer:

```text
What is happening right now?
Which agents are working?
Which tasks are pending?
Which PRs are open?
Which tasks passed validation?
Which tasks failed?
What changed recently?
Is the system healthy?
Is the system safe?
What should I look at next?
```

The UI should prioritize:

```text
clarity
visual hierarchy
readability
density without clutter
fast scanning
trust
status visibility
developer confidence
```

The UI should avoid:

```text
generic template look
random colors
inconsistent spacing
unclear labels
fake metrics
decorative clutter
slow animations
tiny unreadable text
unclear status indicators
confusing navigation
```

***

# 39. Premium Dashboard Requirements

Frontend-related tasks should gradually move the interface toward a premium dashboard.

A strong AI Factory dashboard may include:

```text
top-level system health panel
active agents panel
task queue overview
role distribution chart
daily task budget widget
validation status panel
recent PR activity feed
Jules task lifecycle timeline
automerge status indicator
recent failures panel
security warnings panel
documentation links
architecture diagram entry point
settings/status summary
```

Dashboard cards should have:

```text
clear titles
short descriptions
useful values
status indicators
consistent spacing
clear icons or visual markers when available
empty states
loading states
error states
responsive behavior
```

Dashboard sections should answer real user questions.

Do not add decorative cards that do not communicate useful information.

***

# 40. Frontend Visual Design Principles

Frontend agents must follow these visual principles.

## Layout

Use clear structure.

Use consistent page sections.

Use predictable spacing.

Use visual grouping.

Avoid placing unrelated content together.

## Typography

Use readable font sizes.

Use clear hierarchy.

Headings should communicate meaning.

Body text should be concise.

Labels should be specific.

## Spacing

Use consistent spacing.

Do not crowd elements.

Do not leave random empty gaps.

Use whitespace to clarify hierarchy.

## Color

Use colors intentionally.

Color should communicate status, grouping, emphasis, or brand personality.

Avoid random colors.

Avoid low contrast.

Avoid relying only on color to communicate state.

## States

Every meaningful interactive area should consider:

```text
loading
empty
error
success
disabled
active
hover
focus
```

## Responsiveness

UI should work on common desktop sizes.

UI should degrade gracefully on narrower screens.

Avoid fixed layouts that break on smaller viewports.

## Motion

Use motion only when useful.

Motion should clarify state changes.

Avoid slow or excessive animations.

Avoid distracting effects.

***

# 41. UI State Requirements

Frontend tasks should not only create happy-path UI.

Frontend tasks should consider all major states.

## Loading States

Loading states should:

```text
show what is loading
avoid layout jumps when practical
use clear language
avoid infinite ambiguity
```

## Empty States

Empty states should:

```text
explain why there is no data
suggest what happens next
avoid looking broken
match product tone
```

## Error States

Error states should:

```text
show what failed
provide useful next steps if possible
avoid exposing secrets
avoid raw stack traces in user-facing UI
preserve user context
```

## Success States

Success states should:

```text
confirm what happened
be concise
avoid noisy celebration for routine actions
```

## Partial Data States

Partial data states should:

```text
show available data
explain missing data
avoid fake placeholders that look real
```

***

# 42. Accessibility Baseline

Agents must consider accessibility basics.

Frontend changes should include:

```text
semantic HTML where practical
readable contrast
visible focus states
keyboard-accessible controls when practical
clear labels
meaningful button text
non-color-only status indicators
reasonable font sizes
```

Avoid:

```text
clickable divs without accessibility handling
tiny text
low contrast text
ambiguous icons without labels
status indicated only by color
keyboard traps
```

Accessibility work should be practical and incremental.

Do not perform massive accessibility rewrites unless explicitly assigned.

***

# 43. Developer Experience Standard

This project must feel good for developers to understand and run.

Developer experience improvements may include:

```text
clear README setup
clear environment variable documentation
clear validation commands
clear project structure explanation
clear architecture diagrams
simple local run instructions
clear troubleshooting section
clear GitHub Actions explanation
clear AI Factory lifecycle explanation
clear task queue explanation
```

Documenter and architect agents should continuously improve developer experience.

A new developer should be able to answer:

```text
How do I run this?
How do I validate this?
Where is backend code?
Where is frontend code?
Where are skills?
Where is AI Factory state?
How are tasks generated?
How are PRs validated?
How does automerge work?
How do I stop automation?
```

***

# 44. Documentation Quality Standard

Documentation must be treated as a product surface.

Good documentation should be:

```text
accurate
clear
structured
easy to scan
not misleading
not overpromising
grounded in repository reality
```

Documentation should prefer:

```text
short sections
clear headings
diagrams
examples
commands
checklists
mental models
links between docs
```

Documentation should avoid:

```text
wall-of-text explanations
unsupported claims
fake metrics
outdated commands
invented features
marketing fluff without substance
```

Documentation tasks should improve at least one of:

```text
understanding
setup speed
debugging speed
architecture clarity
trust
operational safety
developer onboarding
```

***

# 45. Required Diagram Strategy

The repository should contain clear diagrams explaining the AI Factory.

Documenter and architect agents should create or improve diagrams when relevant.

Preferred diagram format:

```text
Mermaid diagrams in Markdown
```

Mermaid is preferred because it is readable, reviewable, and version-control friendly.

Useful diagrams include:

```text
system architecture diagram
agent role diagram
task queue lifecycle diagram
GitHub Actions workflow diagram
Jules invocation flow diagram
PR lifecycle diagram
validation and automerge diagram
security boundary diagram
backend module diagram
frontend screen map
data flow diagram
failure recovery diagram
emergency stop diagram
```

Diagrams must be accurate.

Do not invent architecture.

Do not show components that do not exist unless clearly marked as planned.

***

# 46. Diagram Quality Rules

A good diagram must:

```text
have a clear title
show meaningful relationships
avoid unnecessary complexity
use accurate names
match repository reality
be placed in a relevant doc
be explained with a short paragraph
```

A bad diagram is:

```text
decorative only
too complex to understand
inaccurate
unlabeled
contradicting code
showing imaginary systems as real
```

When creating diagrams, agents should also add text explaining:

```text
what the diagram shows
why the diagram matters
where the relevant files are
what the main lifecycle is
```

***

# 47. Recommended Core Diagrams

The project should eventually have these diagrams.

## 47.1 AI Factory Lifecycle

Should show:

```text
Tick
Planner
Task Queue
Jules Worker
Pull Request
Validation
Automerge
Metrics
Next Tick
```

## 47.2 Task State Machine

Should show:

```text
pending
claimed
running
completed
failed
blocked
abandoned
obsolete
duplicate
```

## 47.3 Agent Role Map

Should show:

```text
planner creates tasks
workers execute tasks
reviewer checks drift
workflows record state
humans supervise
```

## 47.4 PR Lifecycle

Should show:

```text
task selected
branch created
Jules runs
PR opened
validation runs
safe automerge if allowed
manual review if risky
merge or reject
state update
```

## 47.5 Security Boundary

Should show:

```text
allowed paths
forbidden paths
secrets policy
workflow guardrails
automerge restrictions
```

***

# 48. Product Landing Page Standard

The README should eventually feel like a product landing page for developers.

The README should include:

```text
strong project title
short product-style description
what the AI Factory does
why it is interesting
architecture overview
quickstart
validation commands
project structure
how automation works
agent roles
safety guardrails
diagrams
current limitations
future roadmap
```

The README should not be pure marketing.

The README should combine:

```text
clarity
credibility
technical depth
visual structure
developer usefulness
```

A first-time visitor should understand the repository in under five minutes.

***

# 49. Product Wow Factor Rules

Agents should improve wow factor only when it also improves usefulness.

Good wow factor:

```text
clear visual dashboard
beautiful but readable UI
useful diagrams
fast onboarding
well-structured README
visible automation health
polished empty states
clear status indicators
delightful but subtle interactions
```

Bad wow factor:

```text
random animations
fake numbers
decorative gradients with no purpose
overdesigned UI
slow UI
confusing visual effects
marketing claims without support
copying another product
```

The product should impress because it is:

```text
clear
real
useful
safe
alive
well-structured
```

not because it is flashy.

***

# 50. Planner Product Quality Duties

The planner must create tasks that move the project toward world-class product quality.

Planner should regularly create useful tasks for:

```text
premium dashboard UI
agent activity timeline
task queue visualization
automation health metrics
role distribution charts
architecture diagrams
workflow diagrams
PR lifecycle diagrams
better empty states
better loading states
better error states
better onboarding documentation
better developer experience
clearer system architecture
stronger test coverage
stronger security boundaries
better README presentation
better docs navigation
better frontend structure
better API examples
```

Planner must avoid vague product-quality tasks.

Bad planner tasks:

```text
Make UI better.
Improve design.
Add wow factor.
Make docs nicer.
Create cool diagrams.
```

Good planner tasks:

```text
Add a dashboard card section showing task queue status using existing available data.
Add Mermaid diagram explaining pending -> claimed -> running -> completed task lifecycle.
Improve README quickstart with exact backend run and validation commands.
Add frontend empty state for missing task queue data.
Document safe automerge rules with a validation flow diagram.
```

Every product-quality task must have a concrete outcome.

***

# 51. Planner Design Task Rules

When planner creates frontend or design tasks, each task must specify:

```text
which screen or file to inspect
what user problem to solve
what UI section to improve
what states to consider
what files may be edited
what files must not be edited
how success will be judged
```

A frontend design task must include at least one of:

```text
layout improvement
visual hierarchy improvement
state handling improvement
navigation improvement
dashboard clarity improvement
accessibility improvement
responsive improvement
```

A frontend design task must not simply say:

```text
make it beautiful
make it modern
make it like Linear
make it like Stripe
```

Instead, use:

```text
Use premium SaaS dashboard quality as inspiration only.
Create an original design.
Improve visual hierarchy, spacing, status clarity, and usability.
```

***

# 52. Planner Diagram Task Rules

When planner creates diagram tasks, each task must specify:

```text
which system concept to diagram
which files to inspect
where to place the diagram
what the diagram must include
what must not be invented
how accuracy should be checked
```

Good diagram task example:

```text
Add a Mermaid diagram in docs/ARCHITECTURE_STATE.md showing the AI Factory lifecycle from scheduled tick to task selection, Jules execution, PR validation, automerge, and metrics update.
```

Bad diagram task example:

```text
Add cool diagrams.
```

***

# 53. Frontend World-Class Task Definition Of Done

A frontend task is not complete unless it considers:

```text
visual hierarchy
spacing
typography
responsive behavior
loading states
empty states
error states
success states
accessibility basics
clear labels
clear actions
clear user feedback
```

For frontend work, agents must ask:

```text
Can a first-time user understand this screen?
Can a busy developer scan this quickly?
Are statuses visually clear?
Are errors actionable?
Is the layout consistent?
Does the UI still work if data is missing?
Does the UI still work on smaller screens?
```

Frontend PRs should mention:

```text
what UI area changed
what user problem was solved
what states were considered
whether validation was run
```

***

# 54. Documentation World-Class Task Definition Of Done

A documentation task is not complete unless it improves at least one of:

```text
project understanding
setup speed
architecture clarity
automation clarity
debugging speed
security understanding
developer confidence
```

Documentation PRs should mention:

```text
which docs changed
what confusion was reduced
whether commands were verified
whether diagrams were added or updated
what limitations remain
```

Documentation must not claim features that do not exist.

If a feature is planned but not implemented, mark it clearly as:

```text
planned
future
not implemented yet
```

***

# 55. Architecture World-Class Task Definition Of Done

An architecture task is not complete unless it explains:

```text
what changed
why it changed
which modules are affected
what boundaries are clarified
what risks exist
how validation was performed
whether diagrams were updated
```

Architecture tasks should prefer:

```text
small boundary improvements
clear module ownership
removal of ambiguity
documentation of decisions
dependency simplification
```

Architecture tasks should avoid:

```text
large rewrites
speculative abstractions
framework churn
unnecessary new layers
unclear abstractions
```

***

# 56. Metrics And Observability Product Standard

The AI Factory should become observable.

When relevant, agents should improve visibility into:

```text
tasks started
tasks completed
tasks failed
PRs opened
PRs merged
validation failures
safe automerge count
manual review count
role distribution
lane distribution
recent failure reasons
queue size
active work
automation health
```

Agents must not invent fake metrics.

If live metrics are unavailable, UI and docs should clearly say:

```text
Metrics will appear when data is available.
```

or:

```text
No metrics recorded yet.
```

Do not display fake success numbers.

Do not hardcode impressive-looking statistics.

***

# 57. AI Factory Dashboard Data Honesty

The dashboard must be honest.

If data is unavailable, show an empty state.

If data is partial, label it as partial.

If data is static, label it as static.

If data is example-only, label it as example.

Never present placeholder data as real.

Never inflate project quality with fake metrics.

Trust is more important than looking impressive.

***

# 58. Original Design System Direction

The project should gradually develop an original design system.

The design system may include:

```text
color tokens
spacing tokens
typography scale
card styles
button styles
badge styles
status colors
layout grid
panel styles
timeline styles
chart styles
empty state patterns
error state patterns
```

Design system work should be incremental.

Do not rewrite the whole frontend just to create a design system.

Prefer extracting repeated styles as they appear.

Design system changes should improve consistency.

***

# 59. Suggested Visual Language

The product may use a visual language inspired by:

```text
AI command center
developer operations dashboard
automation cockpit
agent orchestration console
mission control interface
engineering intelligence platform
```

Possible visual qualities:

```text
dark-mode friendly
sharp cards
subtle borders
soft glow only when useful
clear status colors
monospace accents for technical data
strong headings
clean charts
dense but readable panels
```

Avoid:

```text
gaming UI overload
cyberpunk clutter
random neon effects
unreadable contrast
overanimated components
```

The product should feel premium, not noisy.

***

# 60. High-Impact Backlog Ideas

Planner may create tasks based on these ideas when they match repository needs.

Do not create all tasks blindly.

Use these as inspiration.

## 60.1 Frontend Tasks

```text
Create premium dashboard layout for AI Factory overview.
Add task queue status cards.
Add agent role cards.
Add automation health panel.
Add validation result panel.
Add recent PR activity timeline.
Add empty states for missing task data.
Add loading states for async UI actions.
Add error states for failed API requests.
Improve modal error messages.
Improve frontend spacing and typography.
Add responsive dashboard layout.
Add accessible focus states.
Centralize repeated frontend UI helpers.
Create consistent badge styles for statuses.
Create status colors for pending, running, failed, completed.
```

## 60.2 Documentation Tasks

```text
Add AI Factory architecture overview.
Add Mermaid task lifecycle diagram.
Add Mermaid PR lifecycle diagram.
Add GitHub Actions workflow diagram.
Add agent role explanation document.
Add safe automerge explanation.
Add local development guide.
Add API payload examples.
Improve README as product landing page.
Add docs index page.
Add security boundary documentation.
Add validation command documentation.
Add emergency stop documentation.
```

## 60.3 Architecture Tasks

```text
Document backend module boundaries.
Add ADR for AI Factory ownership model.
Clarify task queue lifecycle.
Clarify runtime state ownership.
Clarify metrics ownership.
Document frontend/backend interaction.
Document skills execution boundaries.
Review backend orchestration responsibilities.
Reduce duplicated backend service logic.
Clarify session manager responsibilities.
```

## 60.4 Tester Tasks

```text
Add smoke tests for backend startup.
Add tests for model registry.
Add tests for session manager.
Add tests for skills manager.
Add tests for config parsing.
Add tests for secret filtering.
Add tests for file path validation.
Add tests for API error responses.
Add tests for deterministic skill behavior.
Add tests for JSON file validity.
```

## 60.5 Security Tasks

```text
Harden path traversal protection.
Harden command execution boundaries.
Harden secret stringification.
Harden config loading.
Harden file manager input validation.
Check logs for accidental secret exposure.
Add tests for unsafe path rejection.
Add tests for placeholder-only secret examples.
```

## 60.6 Reviewer Tasks

```text
Review recent backend changes for missing tests.
Review recent docs changes for accuracy.
Review architecture drift after multiple PRs.
Review validation failures by lane.
Review repeated changes to same files.
Review automerged docs/tests PR quality.
```

***

# 61. Premium README Requirements

The README should eventually include:

```text
project title
short product-quality tagline
clear description
why this project matters
main features
AI Factory architecture summary
quickstart
validation commands
project structure
agent roles
task lifecycle
PR lifecycle
automerge policy
emergency stop
screenshots or UI preview when available
Mermaid diagrams
limitations
roadmap
```

The README should feel like:

```text
developer landing page
technical overview
operator manual
trust-building document
```

The README should not feel like:

```text
random notes
unfinished scratchpad
overhyped marketing page
```

***

# 62. Screenshots And Visual Previews

If the UI becomes visually meaningful, documenter agents may add screenshots or references to screenshots only if screenshots are actually present in the repository.

Do not reference screenshots that do not exist.

If screenshots are planned, write:

```text
Screenshots are planned.
```

Do not fake screenshots.

Do not add binary image assets unless explicitly assigned.

Prefer lightweight diagrams first.

***

# 63. Human Supervision Model

The AI Factory is autonomous, but humans remain the final authority.

Agents must respect:

```text
human-reviewed PRs
explicit human instructions
emergency stop
manual rejection
manual merge decisions
repository owner intent
```

If a human instruction conflicts with an agent-generated task, follow the human instruction.

If a human disables automation, do not re-enable it.

If a human marks a workflow or area as forbidden, do not modify it.

***

# 64. Long-Running Autonomy Standard

Because this repository may run for a long time, agents must optimize for sustainability.

Avoid actions that create long-term mess.

Avoid generating many low-value tasks.

Avoid growing files without structure.

Avoid huge completed task archives without compaction.

Avoid repeated PRs that touch the same area without purpose.

Avoid repeatedly creating tasks that fail.

If a lane repeatedly fails, planner should create reviewer/tester/architect tasks to diagnose the root cause.

Long-term autonomy requires:

```text
clear backlog
clear ownership
clear validation
clear docs
clear architecture
low conflict rate
stable main branch
useful metrics
good task hygiene
```

***

# 65. Anti-Filler Rule

Filler work is forbidden.

Filler work includes:

```text
renaming variables without benefit
moving code without benefit
adding obvious comments
creating vague docs
adding decorative UI with no usability value
adding fake metrics
creating duplicate tasks
creating tasks only to satisfy backlog size
making tiny meaningless PRs
```

If planner cannot find enough useful tasks, planner should:

```text
clean duplicates
mark obsolete tasks
improve existing task prompts
create reviewer tasks for real uncertainty
create documentation tasks for real gaps
create tests for real uncovered behavior
```

A smaller useful backlog is better than a large useless backlog.

***

# 66. High-Quality Task Definition

A high-quality task must be:

```text
specific
atomic
scoped
useful
testable or reviewable
safe
aligned with repository needs
clear about files
clear about acceptance criteria
```

A high-quality task should answer:

```text
Who should do it?
Where should the agent look?
What exactly should change?
What must not change?
How will success be judged?
What risk level is it?
Can it automerge?
```

Tasks that do not answer these questions should be improved or removed.

***

# 67. Failure Handling

If an agent cannot complete a task, the agent should not fake completion.

The agent should:

```text
explain what was attempted
explain what blocked completion
make a small safe improvement if possible
avoid broad unrelated changes
avoid claiming success
```

If validation fails, the agent should:

```text
report the failing command
report the failure summary
avoid hiding the failure
avoid claiming tests passed
```

If task scope prevents completion, the agent should:

```text
respect scope
complete the safe scoped portion
explain what would require a separate task
```

***

# 68. Conflict Avoidance

Agents must avoid conflicts.

Agents should avoid touching common high-conflict files unless assigned:

```text
AGENTS.md
README.md
.github/ai-factory/task_queue.json
.github/ai-factory/state.json
.github/ai-factory/metrics.json
.github/ai-factory/config.json
frontend/css/styles.css
large central backend files
```

Planner may modify `task_queue.json`.

Documenter may modify `README.md` when assigned.

Workers should avoid central files unless the task explicitly requires them.

If multiple agents are likely to touch the same file, planner should split tasks carefully or sequence them.

***

# 69. UI Copywriting Standard

UI text should be clear and concise.

Use direct labels.

Avoid vague labels.

Good labels:

```text
Tasks pending
Validation failed
Automerge disabled
No recent PRs
Run validation
View task queue
System healthy
Needs review
```

Bad labels:

```text
Stuff
Things
Magic
Cool data
Something went wrong
Better mode
```

Error messages should be useful.

Empty states should explain what happens next.

Status labels should be consistent.

***

# 70. Final World-Class Rule

Every agent should behave like a careful senior engineer working on a premium product.

Do not only make changes that pass.

Make changes that are:

```text
useful
safe
clear
maintainable
polished
honest
well-scoped
well-documented
well-validated
```

The AI Factory should become better every day.

The repository should become easier to understand every week.

The UI should become more impressive without becoming less usable.

The architecture should become clearer without becoming overengineered.

The automation should become more powerful without becoming unsafe.

The project should feel alive, but controlled.

The final standard is:

```text
A first-time visitor should understand the project.
A developer should respect the architecture.
A maintainer should trust the automation.
A user should enjoy the interface.
A reviewer should understand every PR.
```




