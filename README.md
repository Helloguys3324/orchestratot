# AutoGen AI Factory

*The autonomous AI orchestration platform for continuous development.*

Welcome to AutoGen AI Factory! This project acts as an autonomous AI orchestration platform that utilizes Directed Acyclic Graph (DAG) task routing, asyncio, and the Model Context Protocol (MCP) to manage a multi-agent continuous workflow.

## Why this project matters
The AI Factory demonstrates how a team of specialized AI agents can autonomously operate, maintain, and expand a full-stack web application. By operating in a continuous, zero-human-in-the-loop pipeline, it explores the boundaries of long-running autonomous development and self-healing systems.

## Main Features
- **Autonomous Multi-Agent Workflow:** A scheduled GitHub Actions pipeline that orchestrates specialized AI agents (Planner, Implementer, Tester, Reviewer, Documenter, Security, Architect, Refactorer) to continuously improve the codebase.
- **DAG-Based Task Routing:** Dynamic task generation and assignment based on explicit dependencies and capabilities.
- **Model Context Protocol (MCP):** Safe, standardized tool execution and skill integration for agents.
- **Strict Validation Protocol:** Zero-trust verification requiring comprehensive testing, secret scanning, and syntax checks before any change is merged.
- **FastAPI & Asyncio Backend:** A scalable, non-blocking orchestration server built with Python 3.12.
- **Vanilla JS Frontend:** A lightweight, dependency-free frontend with native Node.js testing.

## AI Factory Architecture Summary
The AI Factory runs locally for interactive development and in GitHub Actions for continuous autonomy.
- **The Queue (`task_queue.json`):** Tasks are pulled from a central backlog, defining strict scopes and constraints.
- **The Orchestrator:** The Python backend, driven by Pydantic models and asynchronous session management, manages agent lifecycles, skill execution, and workspace I/O.
- **The Pipeline (`ai-factory-jules.yml`):** The CI/CD workflow dispatches agents sequentially, validates their pull requests, and automerges safe changes.

## Agent Roles
The factory operates using specialized roles, each with defined capabilities and boundaries:
- **Planner:** Manages the task backlog and determines the next priority.
- **Implementer:** Writes backend and frontend application code.
- **Tester:** Improves test coverage and adds validation checks.
- **Reviewer:** Reviews recent PRs for architecture drift and code quality.
- **Documenter:** Maintains and improves documentation and setup guides.
- **Security:** Audits dependencies and hardens application boundaries.
- **Architect:** Updates high-level architecture decisions and state.
- **Refactorer:** Improves code readability and reduces duplication.

## Lifecycle & Automerge Policy
Automerge is intentionally conservative to prevent autonomous regressions:
- A PR can be merged automatically **only** when `AI Factory Validate` passes, it is not a draft, the title starts with `ai-factory(documenter):` or `ai-factory(tester):`, and it has the label `ai-factory:safe-automerge`.
- All implementation, refactor, security, and architecture PRs require human review.

## Screenshots / UI Preview
*(Screenshots are planned.)*

## Quickstart

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
pip install pytest pytest-cov pytest-asyncio  # testing dependencies
cp .env.example .env
python run.py
```
*(Note: See [Local Development Setup](#local-development-setup) for detailed configurations, `PYTHONPATH` instructions for testing, and Windows activation commands.)*

## Documentation

- [AI Factory Operations](docs/AI_FACTORY.md) - Details on GitHub Actions, autonomous roles, and factory workflows.
- [API and Architecture Notes](docs/API_NOTES.md) - High-level overview of backend services, endpoints, and orchestration.
- [Agent Instructions](AGENTS.md) - Core guidelines, constraints, and rules for autonomous AI contributors.
- [Mission & Goals](mission.md) - High-level project objectives and operating principles.
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions for local setup, validation, and operations.

## Project Structure

- `backend/` - FastAPI application and orchestration logic.
- `frontend/` - Static HTML/CSS/JS UI files.
- `skills_library/` and `custom_skills/` - Skill implementations.
- `data/` - Runtime JSON state.
- `.github/ai-factory/` - Autonomous development state, task planning files, and metrics tracking (`metrics.json`).

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
   - `AUTOGEN_ENV_FILE`: The path to the custom .env configuration file (defaults to .env in project root).
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
5. **Autopilot Activation:** The GitHub Actions workflow `AI Factory Tick` runs automatically on a schedule. By default, it will not process tasks if an `AUTOPILOT_STOP` file is present in the repository root. Ensure no `AUTOPILOT_STOP` file exists to allow the autonomous workflows to execute. To safely halt autonomous execution at any time, simply create an empty file named `AUTOPILOT_STOP`.

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
# Note: Using PYTHONPATH=. is required to resolve internal backend/ module imports during local development.
PYTHONPATH=. python -m pytest -q

# Clean up any generated .coverage files or temporary artifacts (e.g. databases, skills)
# created during testing to avoid accidentally committing them.
rm -f .coverage
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

## Limitations
- The orchestrator operates under strict token and round limits.
- Agent tools are confined to the local workspace boundary to prevent arbitrary system modification.
- Only specific backend configurations are accessible via the UI or `.env`.

## Roadmap
- Additional robust UI components and dark-mode themes for the command center.
- Broader MCP plugin integration.
- Stronger agent-to-agent communication pathways and self-correcting review loops.
- Extended metrics dashboard.
