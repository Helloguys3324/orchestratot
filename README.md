# AutoGen AI Factory

Welcome to AutoGen AI Factory! This project acts as an autonomous AI orchestration platform that utilizes Directed Acyclic Graph (DAG) task routing, asyncio, and the Model Context Protocol (MCP) to manage a multi-agent continuous workflow.

## Documentation

- [AI Factory Operations](docs/AI_FACTORY.md) - Details on GitHub Actions, autonomous roles, and factory workflows.
- [API and Architecture Notes](docs/API_NOTES.md) - High-level overview of backend services, endpoints, and orchestration.
- [Agent Instructions](AGENTS.md) - Core guidelines, constraints, and rules for autonomous AI contributors.
- [Mission & Goals](mission.md) - High-level project objectives and operating principles.

## Local Development Setup

To prepare the repository for local development, follow these steps:

1. **Install Python 3.12**
   The backend is built specifically for Python 3.12. Ensure it is installed and active in your environment.

2. **Install Backend Dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Configure Environment Variables**
   Never commit secrets or API keys. Copy the example environment file and add your credentials:
   ```bash
   cp .env.example .env
   ```
   *Note: Never commit your `.env` file to source control.*

4. **Frontend & Testing Dependencies**
   - **Frontend Tests:** Ensure **Node.js** is installed to run frontend vanilla JS unit tests via `node --test`.
   - **UI Validation:** If you make UI changes, ensure Playwright is installed via `pip install playwright && playwright install chromium`.

## Starting the Application

To start the local FastAPI server and serve the frontend:

```bash
python run.py
```
This starts the application at `http://localhost:8000`.

## Validation Commands

Before pushing any changes, please run the following validation commands to ensure code quality and prevent secret leakage:

```bash
# Verify Python syntax and compilation
python -m compileall backend skills_library run.py

# Ensure no API keys, credentials, or secrets are accidentally committed
python .github/scripts/scan_secrets.py

# Run all backend unit and integration tests
python -m pytest -q
```
