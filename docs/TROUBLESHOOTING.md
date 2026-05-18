# Troubleshooting Guide

This guide provides solutions to common issues encountered while setting up and running the AutoGen AI Factory locally or in GitHub Actions.

## Local Development Setup

### Issue: `python run.py` fails with "ModuleNotFoundError"
**Symptom:** You attempt to start the backend but Python cannot find certain modules (e.g., `fastapi`, `pydantic`).
**Solution:** Ensure you have activated your virtual environment (if using one) and installed all required dependencies.
```bash
pip install -r backend/requirements.txt
```

### Issue: `pytest` cannot find the `backend` module
**Symptom:** Running `python -m pytest` or `pytest` results in an `ImportError` or `ModuleNotFoundError` for internal project modules.
**Solution:** You need to specify the Python path so it can resolve the `backend` directory correctly from the project root.
```bash
PYTHONPATH=. python -m pytest -q
```
Also, ensure the testing dependencies are installed:
```bash
pip install pytest pytest-cov pytest-asyncio python-dotenv fastapi httpx pydantic pydantic-settings
```

### Issue: Validation commands fail due to missing `node` or test runner issues
**Symptom:** Frontend validation fails when running `node --experimental-test-coverage --test frontend/tests/*.js`.
**Solution:** Ensure you have Node.js version 20 or higher installed, as it natively includes the `node:test` module. You do not need to `npm install` anything for standard test runs.

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
**Solution:** The system uses `pydantic-settings`. Ensure your `.env` variables are correctly formatted and are not empty strings. The configuration is set to ignore empty strings on load (`env_ignore_empty=True`). However, you can deliberately clear API keys or other fields out by updating settings through the UI, which writes the empty string to the `.env` file.

## GitHub Actions & Autonomous Workflows

### Issue: "Infrastructure Lock" PR rejection
**Symptom:** The AI Factory bots or GitHub Actions are rejecting a pull request because it modifies `.github/workflows/`, `.github/scripts/`, or `.github/CODEOWNERS`.
**Solution:** AI agents are strictly forbidden from modifying these files. If infrastructure changes are required, a human must create a separate PR outside of the automated AI Factory framework.

### Issue: AI tasks are repeatedly failing or getting stuck
**Symptom:** You notice that AI tasks in the queue are failing consecutively without making progress.
**Solution:**
1. Stop the autonomous background processes by creating a file named `AUTOPILOT_STOP` in the root directory.
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

### Issue: Playwright complains about missing browsers or executable paths
**Symptom:** During UI validation, Playwright fails to launch or reports that a browser executable is not found.
**Solution:** Ensure you have installed the necessary Playwright browsers in your environment. Run the following commands line-by-line:
```bash
pip install playwright
playwright install chromium
```
