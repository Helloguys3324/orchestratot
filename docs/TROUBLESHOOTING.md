# Troubleshooting Guide

This guide provides solutions to common issues encountered while setting up and running the AutoGen AI Factory locally or in GitHub Actions.

## Local Development Setup

### Issue: `python run.py` fails with "ModuleNotFoundError"
**Symptom:** You attempt to start the backend but Python cannot find certain modules (e.g., `fastapi`, `pydantic`).
**Solution:** Ensure you have activated your virtual environment (if using one) and installed all required dependencies.
```bash
pip install -q -r backend/requirements.txt
```

### Issue: `pytest` cannot find the `backend` module
**Symptom:** Running `python -m pytest` or `pytest` results in an `ImportError` or `ModuleNotFoundError` for internal project modules.
**Solution:** You need to specify the Python path so it can resolve the `backend` directory correctly from the project root.
```bash
PYTHONPATH=. python -m pytest -q
```
Also, ensure the testing dependencies are installed:
```bash
pip install -q pytest pytest-cov
```
*Note: For async tests in pytest, prefer using `@pytest.mark.anyio` instead of `@pytest.mark.asyncio`. The `anyio` plugin is natively available via the project's FastAPI/HTTPX dependencies, ensuring tests run successfully in CI environments where `pytest-asyncio` might not be installed.*

### Issue: Validation commands fail due to missing `node` or test runner issues
**Symptom:** Frontend validation fails when running `node --experimental-test-coverage --test frontend/tests/*.test.js`.
**Solution:** Ensure you have Node.js version 20 or higher installed, as it natively includes the `node:test` module. You do not need to `npm install` anything for standard test runs. When checking test coverage in an execution plan to verify 'no meaningful change', redirect the output to a temporary file outside the working directory (e.g., `> /tmp/coverage.txt 2>&1 && tail -n 25 /tmp/coverage.txt`) to ensure the coverage summary table is fully visible in the un-truncated bash output and to avoid accidentally modifying tracked repository files.

### Issue: `pip-audit` reports false positives or missing dependencies
**Symptom:** Running `pip-audit -r backend/requirements.txt` fails or flags vulnerabilities for package versions that aren't actually installed in the target environment.
**Solution:** Ensure you have installed the project core requirements locally first (`pip install -q -r backend/requirements.txt`). To evaluate specific minimum package versions (e.g., those defined with `>=` constraints), you must explicitly install those exact older versions in the local environment (e.g., `pip install -q "websockets==13.0.0"`) before running `pip-audit`, rather than installing from the requirements file which resolves to the latest compatible versions. Use the `-q` flag for `pip install` in automated bash sessions to prevent verbose logs from truncating subsequent output. Note that PyAutoGen v0.4.x introduces breaking API changes and cannot be used to mitigate CVE-2025-69872 without a complete application rewrite.

## Secrets and Configuration

### Issue: "Secret Scanner Failed" during validation
**Symptom:** Running `python .github/scripts/scan_secrets.py` reports that a secret or an API key has been committed.
**Solution:**
1. Check the output of the scanner to locate the file and line containing the exposed secret.
2. Remove the secret from the code immediately.
3. If the file is `data/settings.json`, replace the real key with an empty string or a placeholder (note: `data/settings.json` is automatically cleared on startup as part of the migration to `.env`, so it should generally remain an empty object `{}`).
4. Move your real credentials into your local `.env` file, which is ignored by Git.

### Issue: Configuration defaults are not being overridden by environment variables
**Symptom:** The backend starts, but it is ignoring your `.env` variables or system environment variables.
**Solution:** The system uses `pydantic-settings`. Ensure your `.env` variables are correctly formatted and are not empty strings or whitespace-only strings (except for path variables like `AUTOGEN_DATA_DIR`, which explicitly support empty or whitespace strings to fallback to defaults). The configuration is set to ignore empty strings on load (`env_ignore_empty=True`) for credentials and general settings. However, you can deliberately clear API keys or other fields out by updating settings through the UI, which programmatically removes the key from the `.env` file (via `unset_key`) and the runtime environment (via `os.environ.pop`).

### Issue: JSON files appear truncated or incomplete in terminal output
**Symptom:** When reading large JSON files (like `task_queue.json`) using `cat`, the output is truncated, missing the end of the file.
**Solution:** Avoid using `cat` for large JSON files. Instead, use `jq` (e.g., `jq . file.json`) or a Python script to ensure the full, un-truncated structure is correctly read and validated.

### Issue: JSON files fail validation or cause errors
**Symptom:** You encounter JSONDecodeError or the AI Factory reports JSON validation failures.
**Solution:** The AI Factory orchestrator enforces strict JSON syntax for its state and planning files. Run the built-in JSON tool to identify the exact line containing the syntax error:
```bash
python -m json.tool <filepath>
```

## GitHub Actions & Autonomous Workflows

### Issue: "Infrastructure Lock" PR rejection
**Symptom:** The AI Factory bots or GitHub Actions are rejecting a pull request because it modifies `.github/workflows/`, `.github/scripts/`, or `.github/CODEOWNERS`.
**Solution:** AI agents are strictly forbidden from modifying these files. If infrastructure changes are required, a human must create a separate PR outside of the automated AI Factory framework.

### Issue: GitHub Actions fails to push branch or create PR
**Symptom:** The autonomous workflow runs successfully but fails at the final git push or gh pr create step with a "403 Forbidden" or permission error.
**Solution:** The default GitHub Actions token might lack write permissions to your repository. Navigate to **Settings -> Actions -> General -> Workflow permissions**. Ensure **Read and write permissions** is selected, and check **Allow GitHub Actions to create and approve pull requests**.

### Issue: AI tasks are repeatedly failing or getting stuck
**Symptom:** You notice that AI tasks in the queue are failing consecutively without making progress.
**Solution:**
1. Stop the autonomous background processes by creating a file named `AUTOPILOT_STOP` in the repository root directory.
   ```bash
   touch AUTOPILOT_STOP
   ```
2. Manually inspect the recent GitHub Actions logs to identify the root cause.
3. Once resolved, you can resume the process by deleting or renaming the `AUTOPILOT_STOP` file.

### Issue: Safe Automerge is not triggering
**Symptom:** A PR created by the AI Factory has passed validation but is not automatically merging.
**Solution:** Review the safe automerge criteria documented in [AI_FACTORY.md](AI_FACTORY.md). Ensure:
- The `AI Factory Validate` checks have successfully passed.
- The PR is not marked as a draft.
- The PR title starts with `ai-factory(documenter):` or `ai-factory(tester):`.
- The PR has the label `ai-factory:safe-automerge`.

## User Interface

### Issue: UI changes do not appear visually correct or the layout breaks
**Symptom:** After modifying files in `frontend/`, the UI looks distorted, cards overlap, or layout breaks at different viewport sizes.
**Solution:** Complete the **Frontend Visual Validation** protocol:
1. Start the app using `python run.py`.
2. Navigate to `http://localhost:8000`.
3. Visually inspect the changes across different viewport sizes (e.g., 1440x900, 1024x768, 390x844).
4. Check the browser console for any runtime errors and fix them before opening a PR.

