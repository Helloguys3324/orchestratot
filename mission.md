# AutoGen Mission

Build and continuously improve AutoGen as an autonomous AI orchestration platform.

Primary goals:

- Keep the FastAPI backend stable, secure, and easy to operate.
- Improve the frontend workflow for creating agents, sessions, skills, and model settings.
- Expand test coverage around routing, sessions, skills, settings, and websocket behavior.
- Keep secrets out of source control and move runtime credentials to environment variables (e.g. using local `.env` files). When adding new configuration, always map it in `backend/config.py` and document it in `.env.example`.
- Make every autonomous change small, reviewable, measurable, and reversible.
- Ensure documentation accurately reflects the current state of local setup, workflows, and validation commands.

Operating rules:

- Prefer small pull requests with one clear purpose.
- Run the repository validation commands (including mandatory JSON syntax validation if JSON files were changed) before opening a PR.
  - `pip install -q -r backend/requirements.txt && pip install -q pytest pytest-cov anyio httpx && python -m compileall backend skills_library run.py && python .github/scripts/scan_secrets.py && PYTHONPATH=. python -m pytest -q && node --experimental-test-coverage --test frontend/tests/*.test.js > /tmp/coverage.txt 2>&1 && (git rm -r --cached frontend/coverage/ .coverage || true) && rm -rf frontend/coverage/ .coverage`
  - `python -m json.tool <filepath> > /dev/null` (run individually on changed JSON files)
  - (See docs/LOCAL_DEVELOPMENT.md for the complete validation suite and docs/TROUBLESHOOTING.md for Git errors)
- Do not commit API keys, tokens, credentials, `.env` files, local databases, or generated caches.
- Do not modify unrelated files.
- Do not rewrite project history.
- Treat `AUTOPILOT_STOP` as a hard stop for autonomous work. To resume, delete the `AUTOPILOT_STOP` file.
- Ensure local setup and operations documentation is always accurate, clear, and reflects the current repository state.
- Visually inspect and validate frontend UI changes locally before opening a PR.
