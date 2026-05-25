# AutoGen Mission

Build and continuously improve AutoGen as an autonomous AI orchestration platform.

Primary goals:

- Keep the FastAPI backend stable, secure, and easy to operate.
- Improve the frontend workflow for creating agents, sessions, skills, and model settings.
- Expand test coverage around routing, sessions, skills, settings, and websocket behavior.
- Keep secrets out of source control and move runtime credentials to environment variables (e.g. using local `.env` files).
- Make every autonomous change small, reviewable, measurable, and reversible.
- Ensure documentation accurately reflects the current state of local setup, workflows, and validation commands.

Operating rules:

- Prefer small pull requests with one clear purpose.
- Run the repository validation commands (including mandatory JSON syntax validation if JSON files were changed) before opening a PR.
  - `python -m compileall backend skills_library run.py`
  - `python .github/scripts/scan_secrets.py`
  - `python .github/scripts/guard_ai_workflows.py` (see Troubleshooting Guide for the temporary empty commit workaround if this fails with an ambiguous Git error)
  - `pip install -q -r backend/requirements.txt`
  - `pip install -q pytest pytest-asyncio pytest-cov anyio`
  - `PYTHONPATH=. python -m pytest -q`
  - `node --experimental-test-coverage --test frontend/tests/*.test.js`
  - `rm -rf coverage/ frontend/coverage/ .coverage`
  - `python -m json.tool <filepath>` (run individually on changed JSON files)
- Do not commit API keys, tokens, credentials, `.env` files, local databases, or generated caches.
- Do not modify unrelated files.
- Do not rewrite project history.
- Treat `AUTOPILOT_STOP` as a hard stop for autonomous work. To resume, delete the `AUTOPILOT_STOP` file.
- Ensure local setup and operations documentation is always accurate, clear, and reflects the current repository state.
- Visually inspect and validate frontend UI changes locally before opening a PR.
