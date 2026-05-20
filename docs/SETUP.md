# Setup & Operations Guide

## Local Development Setup

To prepare the repository for local development, follow these steps:

### 1. Prerequisites
- **Python 3.12:** The backend is built specifically for Python 3.12. Ensure it is installed and active in your environment.
- **Node.js (v20+):** Ensure Node.js (v20+) is installed to run frontend vanilla JS unit tests using the native test runner.

### 2. Virtual Environment & Dependency Installation
It is highly recommended to use a Python virtual environment to isolate project dependencies.

```bash
# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment (Mac/Linux)
source venv/bin/activate

# Activate the virtual environment (Windows)
venv\Scripts\activate
```

Once activated, install the necessary packages for the backend and testing tools:
```bash
# Core backend dependencies
pip install -r backend/requirements.txt

# Local backend testing dependencies
pip install pytest pytest-cov pytest-asyncio
```

### 3. Secrets & Configuration
Never commit secrets, API keys, or credentials. Follow these steps to configure your local runtime:

1. **Create Environment File**: Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. **Configure Credentials**: Your local `.env` file is meant for development. Key environment variables include:
   - `AUTOGEN_API_KEY`: Your language model API key.
   - `AUTOGEN_DEFAULT_MODEL`: The default model (e.g., `gemini-2.5-flash`).
   - `AUTOGEN_ROUTER_MODEL`: The model to use for the orchestrator router.
   - `AUTOGEN_BASE_URL`: The base URL for the API endpoint (defaults to Google's Gemini API).
   - `AUTOGEN_MAX_ROUNDS`: The maximum number of conversational rounds allowed (defaults to 15).
   - `AUTOGEN_TEMPERATURE`: The temperature parameter for model generation (defaults to 0.7).
   - `AUTOGEN_MAX_TOKENS`: The maximum tokens parameter for model generation (defaults to 4096).
   - `AUTOGEN_DATA_DIR`: The directory where runtime JSON data is stored.
   - `AUTOGEN_SKILLS_DIR`: The directory for built-in skills.
   - `AUTOGEN_CUSTOM_SKILLS_DIR`: The directory for custom skills.
   - `AUTOGEN_WORKSPACE_DIR`: The directory for session workspace files.

   **Configuration Handling Details:**
   - **Environment Variables**: The backend utilizes `pydantic-settings` to safely load configuration, strictly prioritizing environment variables over `.env` variables and JSON defaults. Empty environment variables are intentionally ignored on load, except for path variables (e.g., `AUTOGEN_DATA_DIR`) which explicitly support empty strings to fallback to their defaults.
   - **Legacy Migration**: Legacy JSON configurations (`data/settings.json`) are automatically migrated to the `.env` file upon startup, securing credentials by immediately clearing the legacy JSON file after migration.
   - **UI Updates**: Configuration changes made via the UI will dynamically update the local `.env` file, persisting only the explicitly changed fields to prevent accidental overwrites with defaults.
   - **Clearing Values**: When programmatically clearing configuration values, `dotenv.unset_key` and `os.environ.pop` must be used.
3. **Verify Secrets**: You must verify that no secrets are accidentally committed before submitting PRs by running the repository's secret scanner:
   ```bash
   python .github/scripts/scan_secrets.py
   ```

### 4. Continuous Integration & AI Factory
The repository leverages GitHub Actions to orchestrate the continuous autonomous workflow and validate all code changes automatically.

**Required GitHub Setup:**
1. **App Installation:** Install/connect the repository in the Jules web app.
2. **API Key Creation:** Create a Jules API key.
3. **Secret Configuration:** Add repository secrets (navigate to **Settings -> Secrets and variables -> Actions**):
   - Name: `JULES_API_KEY`
     Value: your Jules API key
   - Name: `AUTOGEN_API_KEY` (if your models require authentication)
     Value: your LLM provider API key
4. **Action Verification:** Confirm GitHub Actions are enabled for the repository.
5. **Autopilot Activation:** Remove or rename `AUTOPILOT_STOP` when scheduled autonomous work should start. (Note: The automated workflow checks for this file in the root directory; if it exists, autonomous execution will safely halt.)

Make sure these setup steps are fully completed to ensure that continuous integration checks and scheduled tasks run properly.

**Authoritative Validation:** GitHub Actions validation is the single source of truth for repository checks. Local validation commands mirror the remote pipeline, but PRs cannot merge if the remote pipeline fails.

For detailed workflows and auto-merge requirements, refer to [AI Factory Operations](docs/AI_FACTORY.md).
*Important: Never modify `.github/workflows`, `.github/scripts`, or `.github/CODEOWNERS` directly, as infrastructure changes require a human PR outside of the AI Factory.*

### 5. Emergency Stop Protocol
If you need to stop autonomous background tasks, create an empty file named `AUTOPILOT_STOP` in the repository root directory:
```bash
touch AUTOPILOT_STOP
```
This halts scheduled execution both locally and on GitHub Actions.

## Starting the Application

To start the local FastAPI server and serve the frontend:

```bash
python run.py
```
This starts the application at `http://localhost:8000`.

*Note: If running the application in the background (e.g., `python run.py > app_output.log 2>&1 &`), you must explicitly remove the generated log files (e.g., `rm app_output.log`) when finished to prevent accidentally committing generated runtime logs.*

## Validation Commands

Running the full validation suite from the **repository root** is **mandatory** before opening a PR or pushing any code changes. This ensures code quality, architectural constraint adherence, and prevents secret leakage. If you make frontend changes, you must also complete the **Frontend Visual Validation** workflow described below.

### Core Validation
```bash
# Verify Python syntax and compilation
python -m compileall backend skills_library run.py

# Ensure no API keys, credentials, or secrets are accidentally committed
python .github/scripts/scan_secrets.py

# Run all backend unit and integration tests (ensure local testing dependencies are installed)
PYTHONPATH=. python -m pytest -q
```

### Frontend Validation
```bash
# Run frontend tests using native node runner (no extra npm packages required)
# Note: Always run the full suite to get accurate coverage. Running a single file will falsely report lower overall coverage.
node --experimental-test-coverage --test frontend/tests/*.test.js
```

### File-Specific Validation
```bash
# Validate JSON syntax (required if any JSON files are modified)
python -m json.tool <filepath>
```

### Vulnerability Scanning
```bash
# Optional: Scan for known vulnerabilities in Python dependencies (requires backend/requirements.txt to be explicitly installed first)
pip install pip-audit
pip-audit -r backend/requirements.txt
```

*Note: To evaluate specific minimum package versions (e.g., those defined with `>=` constraints), you must explicitly install those exact older versions in the local environment (e.g., `pip install "websockets==13.0.0"`) before running `pip-audit`, rather than installing from the requirements file which resolves to the latest compatible versions.*

## Frontend Visual Validation

If any files in `frontend/` are modified, you must visually inspect the UI locally:
1. Start the application: `python run.py`
2. Open `http://localhost:8000` in a browser.
3. Walk through the changed UI area and affected user flows.
4. Check browser console for errors.
5. Check for layout issues (overlapping text, hidden content, etc.) across different viewport sizes (e.g., 1440x900 desktop, 1024x768 tablet, 390x844 mobile).
