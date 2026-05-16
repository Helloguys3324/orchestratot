# AutoGen AI Factory

Welcome to AutoGen AI Factory! This project acts as an autonomous AI orchestration platform that utilizes Directed Acyclic Graph (DAG) task routing, asyncio, and the Model Context Protocol (MCP) to manage a multi-agent continuous workflow.

## Documentation

- [AI Factory Operations](docs/AI_FACTORY.md)
- [API and Architecture Notes](docs/API_NOTES.md)
- [Agent Instructions](AGENTS.md)
- [Mission & Goals](mission.md)

## Starting the Application

To start the local FastAPI server and serve the frontend:

```bash
python run.py
```
This starts the application at `http://localhost:8000`.

## Validation Commands

Before pushing any changes, please run the following validation commands to ensure code quality and prevent secret leakage:

```bash
python -m compileall backend skills_library run.py
python .github/scripts/scan_secrets.py
python -m pytest -q
```
