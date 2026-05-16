"""
AutoGen AI Orchestrator — Entry Point.
Run with: python run.py
"""
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("  AutoGen AI Orchestrator")
    print("  Starting server at http://localhost:8000")
    print("=" * 60)
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["backend"],
    )
