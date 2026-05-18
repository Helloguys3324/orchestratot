# AutoGen AI Factory

Welcome to AutoGen AI Factory! This project acts as an autonomous AI orchestration platform that utilizes Directed Acyclic Graph (DAG) task routing, asyncio, and the Model Context Protocol (MCP) to manage a multi-agent continuous workflow.

## Documentation

- [AI Factory Operations](docs/AI_FACTORY.md) - Details on GitHub Actions, autonomous roles, and factory workflows.
- [API and Architecture Notes](docs/API_NOTES.md) - High-level overview of backend services, endpoints, and orchestration.
- [Agent Instructions](AGENTS.md) - Core guidelines, constraints, and rules for autonomous AI contributors.
- [Mission & Goals](mission.md) - High-level project objectives and operating principles.

## Project Structure

- `backend/` - FastAPI application and orchestration logic.
- `frontend/` - Static HTML/CSS/JS UI files.
- `skills_library/` and `custom_skills/` - Skill implementations.
- `data/` - Runtime JSON state.
- `.github/ai-factory/` - Autonomous development state and task planning files.

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
pip install pytest pytest-cov pytest-asyncio python-dotenv fastapi httpx pydantic pydantic-settings

# UI testing dependencies (Optional, only needed if making UI changes)
pip install playwright
playwright install chromium
```

### 3. Secrets & Configuration
Never commit secrets or API keys. Copy the example environment file to configure your local runtime:
```bash
cp .env.example .env
```
*Note: Your `.env` file should include runtime credentials like `AUTOGEN_API_KEY`. The backend uses `pydantic-settings` to automatically load these variables safely, prioritizing environment variables over `.env` variables and JSON defaults. Empty environment variables are intentionally ignored.*

You can verify that no secrets are accidentally committed by running the secret scanner:
```bash
python .github/scripts/scan_secrets.py
```

### 4. Continuous Integration & AI Factory
The repository leverages GitHub Actions to orchestrate the continuous autonomous workflow and validate all code changes automatically.

**Required GitHub Setup:**
1. **App Installation:** Install/connect the repository in the Jules web app.
2. **API Key Creation:** Create a Jules API key.
3. **Secret Configuration:** Add repository secrets (navigate to **Settings -> Secrets and variables -> Actions**):
   - `JULES_API_KEY` (your Jules API key)
   - `AUTOGEN_API_KEY` (if your models require authentication)
4. **Action Verification:** Confirm GitHub Actions are enabled for the repository.

For detailed workflows and auto-merge requirements, refer to [AI Factory Operations](docs/AI_FACTORY.md).
*Important: Never modify `.github/workflows`, `.github/scripts`, or `.github/CODEOWNERS` directly, as infrastructure changes require a human PR outside of the AI Factory.*

### 5. Emergency Stop Protocol
If you need to stop autonomous background tasks, create an empty file named `AUTOPILOT_STOP` in the root directory. This halts scheduled execution both locally and on GitHub Actions.

## Starting the Application

To start the local FastAPI server and serve the frontend:

```bash
python run.py
```
This starts the application at `http://localhost:8000`.

## Validation Commands

Running the full validation suite is **mandatory** before opening a PR or pushing any code changes. This ensures code quality, architectural constraint adherence, and prevents secret leakage. If you make frontend changes, you must also complete the **Frontend Visual Validation** workflow described below.

```bash
# Verify Python syntax and compilation
python -m compileall backend skills_library run.py

# Ensure no API keys, credentials, or secrets are accidentally committed
python .github/scripts/scan_secrets.py

# Run all backend unit and integration tests (ensure local testing dependencies are installed)
PYTHONPATH=. python -m pytest -q

# Run frontend tests using native node runner (no extra npm packages required)
node --experimental-test-coverage --test frontend/tests/*.js

# Optional: Scan for known vulnerabilities in Python dependencies (requires backend/requirements.txt to be installed)
pip-audit -r backend/requirements.txt
```

## Frontend Visual Validation

If any files in `frontend/` are modified, you must visually inspect the UI locally:
1. Start the application: `python run.py`
2. Open `http://localhost:8000` in a browser.
3. Walk through the changed UI area and affected user flows.
4. Check browser console for errors.
5. Check for layout issues (overlapping text, hidden content, etc.) across different viewport sizes.
