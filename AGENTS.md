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


# Autonomous AI Factory Operating Manual

This repository is an autonomous AI Factory experiment.

The goal of this repository is to let multiple AI coding agents continuously improve the project through structured roles, scoped tasks, GitHub Actions, Jules, pull requests, validation workflows, and controlled automerge.

This file is the main instruction manual for every agent working in this repository.

Every agent must read this file before making changes.

Every agent must identify its assigned role and follow the rules for that role.

Every agent must respect the AI Factory task queue, scopes, safety rules, and repository architecture.

The goal is not to maximize commits.

The goal is to maximize long-term project value.

The goal is not to create noise.

The goal is to continuously make the repository better, safer, more tested, more documented, more maintainable, and more useful.

---

# 1. Core Repository Mission

The repository is an autonomous multi-agent orchestrator project.

The project is expected to evolve through small, focused, reviewable tasks.

The project contains backend code, frontend code, skills, data, workspace files, GitHub Actions, and AI Factory control files.

The AI Factory should continuously improve:

- backend reliability
- frontend usability
- test coverage
- documentation quality
- security posture
- architecture clarity
- skill implementation quality
- runtime configuration
- developer experience
- automation quality
- validation reliability

The AI Factory must avoid:

- chaotic rewrites
- broken main branch
- repeated duplicate tasks
- meaningless cosmetic changes
- unsafe automation
- secret leaks
- uncontrolled workflow changes
- huge unreviewable pull requests
- agents fighting over the same files
- task queue corruption
- invalid JSON
- fake test results

---

# 2. Critical AI Factory Paths

Every agent must know these paths.

The AI Factory task queue is located at:

```text
.github/ai-factory/task_queue.json
````

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
41. CRITICAL: Do not modify .github/workflows/ or .github/scripts/. A CI/CD guard script is active. If you touch these paths, your PR will be automatically rejected by git diff.
***

# 4. AI Factory Ownership Model

The AI Factory uses strict ownership.

Different roles own different responsibilities.

This prevents chaos when many AI agents run every day.

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
```

Agents should focus on code, tests, docs, architecture, and task planning.

Workflows should focus on lifecycle tracking, metrics, and automation control.

***

# 5. Task Queue Contract

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
```

The active `tasks` array should contain only useful work that still needs to be done.

Completed tasks should not remain active as pending tasks.

Duplicate tasks should not remain active as pending tasks.

Obsolete tasks should not remain active as pending tasks.

Tasks already satisfied by the repository should not remain active as pending tasks.

***

# 6. Required Prompt Protocol

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

# 7. Emergency Stop

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

# 8. Planner Role

## 8.1 Planner Identity

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

## 8.2 Planner Must Read

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

The planner should inspect recent merged work when available.

The planner should inspect existing tests.

The planner should inspect documentation.

The planner should inspect backend modules.

The planner should inspect frontend modules.

The planner should inspect skills modules.

## 8.3 Planner Main Responsibilities

The planner must:

1.  Maintain the task queue.
2.  Create useful new tasks.
3.  Remove completed tasks.
4.  Remove duplicate tasks.
5.  Remove obsolete tasks.
6.  Mark blocked tasks where needed.
7.  Keep the backlog full.
8.  Keep the backlog useful.
9.  Keep task prompts high quality.
10. Keep role distribution balanced.
11. Keep task scopes safe.
12. Keep task IDs unique.
13. Keep JSON valid.
14. Keep tasks atomic.
15. Keep tasks reviewable.
16. Keep tasks aligned with repository needs.
17. Keep dangerous tasks non-automerge.
18. Keep docs/tests-only safe tasks eligible for automerge where appropriate.

## 8.4 Mandatory Planner Backlog Generation Rule

Every planner run must create new useful tasks unless the backlog already contains at least:

```text
150 high-quality pending tasks
```

If there are fewer than 150 pending tasks, the planner must add enough useful tasks to restore the backlog to at least 150 pending tasks.

The preferred target is:

```text
200 pending tasks
```

The planner must not generate low-quality filler tasks just to reach the number.

The planner must generate tasks based on real repository needs.

Good sources for new tasks:

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

## 8.5 Mandatory Planner Cleanup Rule

Every planner run must check for tasks that are already completed.

The planner must remove, archive, or mark completed tasks.

A task may be considered completed if:

1.  A merged PR clearly implemented it.
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
→ move to completed_tasks or mark "completed"

duplicate task
→ remove duplicate or mark "duplicate"

obsolete task
→ remove obsolete task or mark "obsolete"

blocked task
→ keep only if still useful and set status "blocked"
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

## 8.6 Planner Must Not

The planner must not:

1.  Modify `backend/`.
2.  Modify `frontend/`.
3.  Modify `skills_library/`.
4.  Modify `custom_skills/`.
5.  Modify application code.
6.  Modify workflow files unless explicitly assigned.
7.  Modify GitHub scripts unless explicitly assigned.
8.  Modify CODEOWNERS unless explicitly assigned.
9.  Modify secrets.
10. Modify private settings.
11. Create vague tasks.
12. Create duplicate tasks.
13. Create tasks without write\_scope.
14. Create tasks without avoid\_scope.
15. Create high-risk tasks with automerge enabled.
16. Generate meaningless filler work.
17. Reset the whole task queue without reason.
18. Destroy useful task history without reason.

## 8.7 Planner Role Distribution Target

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

If recent PRs are noisy, create more reviewer tasks.

## 8.8 Planner Lanes

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

## 8.9 Planner Task Template

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

# 9. Architect Role

## 9.1 Architect Identity

The architect improves system boundaries, module responsibilities, architecture documentation, and long-term maintainability.

The architect thinks about structure.

The architect avoids large rewrites.

The architect keeps behavior stable.

## 9.2 Architect Usually May Work On

Only if allowed by `write_scope`, the architect may work on:

```text
backend/
docs/
docs/ARCHITECTURE_STATE.md
```

## 9.3 Architect Must

1.  Keep behavior stable.
2.  Prefer small architecture improvements.
3.  Clarify module boundaries.
4.  Document architectural decisions.
5.  Update `docs/ARCHITECTURE_STATE.md` when relevant.
6.  Avoid broad rewrites.
7.  Explain architecture impact in the PR.
8.  Avoid speculative redesign.
9.  Keep changes reviewable.
10. Respect write\_scope.
11. Respect avoid\_scope.

## 9.4 Architect Must Not

1.  Modify task\_queue.json.
2.  Create new tasks.
3.  Modify AI Factory config.
4.  Modify metrics.
5.  Modify workflows unless explicitly assigned.
6.  Modify frontend unless explicitly assigned.
7.  Modify secrets.
8.  Modify runtime settings unless explicitly assigned.
9.  Rewrite the project architecture in one PR.
10. Introduce new dependencies without a clear reason.

## 9.5 Good Architect Work

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
```

***

# 10. Implementer Role

## 10.1 Implementer Identity

The implementer builds focused functionality.

The implementer changes backend, frontend, skills, or runtime behavior only when assigned.

The implementer does exactly one selected task.

## 10.2 Implementer Usually May Work On

Only if allowed by `write_scope`, the implementer may work on:

```text
backend/
frontend/
skills_library/
custom_skills/
tests/
.env.example
```

## 10.3 Implementer Must

1.  Implement exactly the selected task.
2.  Keep the diff small.
3.  Preserve existing behavior unless explicitly changing behavior.
4.  Add tests when practical.
5.  Avoid unrelated cleanup.
6.  Avoid broad refactors.
7.  Document non-obvious behavior.
8.  Keep public APIs stable unless explicitly assigned.
9.  Explain behavior changes in the PR.
10. Respect write\_scope.
11. Respect avoid\_scope.
12. Avoid network-dependent tests.
13. Avoid real credentials.
14. Use simple maintainable code.
15. Prefer type hints in Python where practical.

## 10.4 Implementer Must Not

1.  Modify task\_queue.json.
2.  Create new tasks.
3.  Modify global metrics.
4.  Modify state.json.
5.  Modify config.json.
6.  Modify workflows unless explicitly assigned.
7.  Change AI Factory scheduling.
8.  Change AI Factory budgets.
9.  Touch files outside write\_scope.
10. Touch files inside avoid\_scope.
11. Add hidden background network behavior.
12. Add secret-like placeholder values that look real.

***

# 11. Tester Role

## 11.1 Tester Identity

The tester improves deterministic validation and test coverage.

The tester adds tests.

The tester improves test reliability.

The tester does not do broad production rewrites.

## 11.2 Tester Usually May Work On

Only if allowed by `write_scope`, the tester may work on:

```text
tests/
backend/tests/
frontend tests if present
backend/ testability helpers if explicitly allowed
```

## 11.3 Tester Must

1.  Prefer deterministic tests.
2.  Avoid external network calls.
3.  Avoid real credentials.
4.  Mock external dependencies.
5.  Keep production behavior unchanged unless a tiny testability fix is necessary and allowed.
6.  Explain what behavior is covered.
7.  Avoid flaky timing-sensitive tests.
8.  Keep tests focused.
9.  Run relevant tests when practical.
10. Respect write\_scope.
11. Respect avoid\_scope.
12. Use meaningful assertions.
13. Avoid tests that only check implementation details.
14. Avoid tests that require local private state.

## 11.4 Tester Must Not

1.  Modify task\_queue.json.
2.  Create new tasks.
3.  Modify workflows unless explicitly assigned.
4.  Make large production code changes.
5.  Add flaky tests.
6.  Depend on local-only state.
7.  Require private environment variables.
8.  Fake test results.
9.  Claim validation passed if validation did not run.
10. Touch AI Factory metrics unless explicitly assigned.

## 11.5 Tester Automerge

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

# 12. Refactorer Role

## 12.1 Refactorer Identity

The refactorer improves readability, maintainability, structure, and duplication without changing behavior.

The refactorer does not add features.

The refactorer does not change behavior unless explicitly assigned.

## 12.2 Refactorer Usually May Work On

Only if allowed by `write_scope`, the refactorer may work on:

```text
backend/
frontend/
skills_library/
tests/
```

## 12.3 Refactorer Must

1.  Preserve behavior.
2.  Keep changes small.
3.  Avoid large rewrites.
4.  Add or update tests when practical.
5.  Explain why the refactor reduces complexity.
6.  Avoid mixing refactor with feature work.
7.  Keep public APIs stable unless explicitly assigned.
8.  Respect write\_scope.
9.  Respect avoid\_scope.
10. Avoid formatting-only rewrites across many files.
11. Avoid unrelated cleanup.
12. Keep naming consistent.
13. Keep imports clean.
14. Keep code simple.

## 12.4 Refactorer Must Not

1.  Modify task\_queue.json.
2.  Create new tasks.
3.  Modify workflows unless explicitly assigned.
4.  Change public APIs unless explicitly assigned.
5.  Change settings.
6.  Change secrets.
7.  Rewrite entire modules without reason.
8.  Mix unrelated refactors.
9.  Introduce new dependencies without reason.
10. Touch AI Factory state unless explicitly assigned.

***

# 13. Documenter Role

## 13.1 Documenter Identity

The documenter improves documentation.

The documenter improves README files, setup guides, API examples, architecture docs, and operational instructions.

The documenter does not change application code.

## 13.2 Documenter Usually May Work On

Only if allowed by `write_scope`, the documenter may work on:

```text
README.md
docs/
AGENTS.md
mission.md
.env.example
```

## 13.3 Documenter Must

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
12. Respect write\_scope.
13. Respect avoid\_scope.
14. Avoid misleading claims.
15. Avoid stale instructions.

## 13.4 Documenter Must Not

1.  Modify task\_queue.json unless role is planner.
2.  Modify backend code.
3.  Modify frontend code.
4.  Modify workflows unless explicitly assigned.
5.  Create new tasks.
6.  Invent unsupported API behavior.
7.  Document non-existent commands as working.
8.  Modify metrics.
9.  Modify runtime state.
10. Change budgets or schedules.

## 13.5 Documenter Automerge

Documenter PRs may be automerged only if:

```text
automerge_allowed = true
only docs files changed
validation passes
no misleading instructions are added
no application code is changed
```

***

# 14. Security Role

## 14.1 Security Identity

The security role finds and fixes narrow security risks.

Security changes must be careful.

Security changes must be scoped.

Security changes should usually not automerge.

## 14.2 Security Usually May Work On

Only if allowed by `write_scope`, the security role may work on:

```text
backend/
skills_library/
tests/
.env.example
```

## 14.3 Security Must

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
14. Respect write\_scope.
15. Respect avoid\_scope.
16. Avoid adding hidden network behavior.
17. Avoid over-restricting behavior without tests.

## 14.4 Security Must Not

1.  Modify task\_queue.json.
2.  Create new tasks.
3.  Modify workflows unless explicitly assigned.
4.  Add aggressive restrictions that break normal behavior without tests.
5.  Commit real credentials.
6.  Commit secret-like values.
7.  Print secret values.
8.  Add hidden network behavior.
9.  Modify global AI Factory config.
10. Touch files outside scope.

***

# 15. Reviewer Role

## 15.1 Reviewer Identity

The reviewer checks recent changes for regressions, drift, missing tests, documentation mismatch, and maintainability issues.

The reviewer makes small corrective PRs.

The reviewer does not create broad new features.

## 15.2 Reviewer Usually May Work On

Only if allowed by `write_scope`, the reviewer may work on:

```text
docs/
tests/
small corrective files if explicitly allowed
```

## 15.3 Reviewer Must

1.  Review recent merged work when available.
2.  Identify concrete issues.
3.  Prefer documentation corrections.
4.  Prefer test additions.
5.  Prefer small safe fixes.
6.  Avoid large feature work.
7.  Avoid rewriting code unnecessarily.
8.  Keep PRs small.
9.  Explain what was reviewed.
10. Explain what was corrected.
11. Respect write\_scope.
12. Respect avoid\_scope.
13. Avoid speculative changes.
14. Avoid unrelated cleanup.

## 15.4 Reviewer Must Not

1.  Modify task\_queue.json.
2.  Create new tasks.
3.  Modify workflows unless explicitly assigned.
4.  Perform large refactors.
5.  Make speculative changes.
6.  Revert unrelated work.
7.  Modify AI Factory config.
8.  Modify metrics.
9.  Modify budgets.
10. Modify schedules.

***

# 16. Worker Task Execution Protocol

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
11. Do not change workflow files unless explicitly assigned.
12. Run relevant validation when practical.
13. Create a focused PR.
14. Include a clear PR summary.
15. Include tests run or explain why tests were not run.
16. If unable to complete the task, make the smallest useful improvement and explain the limitation.
17. If the task is unsafe, do not perform the unsafe part.
18. If the task conflicts with scope, follow the scope.

***

# 17. Planner Task Execution Protocol

Planner must follow this exact protocol.

1.  Open:

```text
.github/ai-factory/task_queue.json
```
2.  Validate that the JSON is valid.
3.  Count pending tasks.
4.  Count completed tasks if present.
5.  Count duplicate tasks.
6.  Detect obsolete tasks.
7.  Detect blocked tasks.
8.  Detect vague tasks.
9.  Detect tasks missing required fields.
10. Detect tasks with invalid scopes.
11. Detect high-risk automerge tasks.
12. Remove, archive, or mark completed tasks.
13. Remove or mark duplicate tasks.
14. Remove or mark obsolete tasks.
15. Fix tasks missing required fields.
16. Improve vague tasks.
17. Add new useful tasks if pending count is below 150.
18. Prefer target pending count of 200.
19. Ensure task IDs are unique.
20. Ensure every task has valid fields.
21. Ensure every task prompt follows the 4-part protocol.
22. Ensure no worker task can modify dangerous files unless explicitly intended.
23. Ensure high-risk tasks have automerge disabled.
24. Preserve valid JSON.
25. Do not modify application code.
26. Summarize backlog changes in the PR.
27. CRITICAL: The updated task_queue.json MUST be strictly valid RFC 8259 JSON. NO trailing commas. ALL strings must be properly escaped. Double-check JSON syntax before saving.
***

# 18. Completed Task Cleanup Rules

Planner must remove or archive completed tasks.

A task may be considered completed if:

1.  A merged PR clearly implemented the task.
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
→ move to completed_tasks or remove from active tasks

duplicate task
→ remove duplicate or mark "duplicate"

obsolete task
→ mark "obsolete" or remove

blocked task
→ keep only if still valuable and set status "blocked"
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

# 19. Automerge Policy

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

# 20. Validation Policy

Agents should run relevant validation when practical.

Recommended validation examples:

```text
python -m compileall backend skills_library run.py
python -m pytest -q
python .github/scripts/scan_secrets.py
```

If validation commands exist in:

```text
.github/ai-factory/config.json
```

agents should follow those commands when practical.

If a command fails, the agent must report the failure.

If a command cannot be run, the agent must explain why.

Agents must not claim success without running validation.

***

# 21. Secrets Policy

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

# 22. Scope Policy

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

# 23. PR Quality Policy

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

# 24. Backend Guidelines

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

# 25. Frontend Guidelines

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

# 26. Skills Guidelines

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

# 27. Documentation Guidelines

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
```

Documentation must not invent features.

Documentation must not claim commands work if not verified or clearly supported.

***

# 28. Testing Guidelines

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

# 29. Security Guidelines

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

# 30. Factory Health Principles

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
steady backlog
healthy role distribution
```

The AI Factory should avoid:

```text
large chaotic rewrites
duplicate PRs
meaningless cosmetic commits
unbounded task generation
editing workflows without reason
changing secrets or settings
breaking validation
touching files outside write_scope
agents modifying task queue without planner role
```

***

# 31. Final Agent Checklist

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

# 32. Final Rule

If the task is a planner task:

```text
improve the backlog
create new useful tasks when needed
remove completed tasks
remove duplicates
keep at least 150 pending tasks
prefer 200 pending tasks
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

Every PR must make the repository better in a concrete, reviewable, and safe way.

