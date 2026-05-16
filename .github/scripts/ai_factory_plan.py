#!/usr/bin/env python3
"""Build a Jules matrix for the AI Factory workflow."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FACTORY_DIR = ROOT / ".github" / "ai-factory"


ROLE_PROMPTS = {
    "planner": "You are the planner. Update only planning files unless the task explicitly says otherwise.",
    "architect": "You are the architect. Improve one architectural weakness with a small, measurable change.",
    "implementer": "You are the implementer. Build one focused feature or fix from the queue.",
    "tester": "You are the tester. Add or improve tests without changing production behavior unless required.",
    "reviewer": "You are the reviewer. Find one concrete defect or regression risk and create a corrective PR.",
    "refactorer": "You are the refactorer. Improve one small area while preserving behavior.",
    "documenter": "You are the documenter. Improve docs and setup clarity without touching application code.",
    "security": "You are the security engineer. Fix one concrete security risk and avoid committing secrets.",
}


LANE_RULES = {
    "backend": "Prefer backend/ and backend tests. Avoid frontend-only edits.",
    "frontend": "Prefer frontend/ files. Avoid backend behavior changes.",
    "skills": "Prefer skills_library/ and custom_skills/. Keep skill interfaces stable.",
    "tests": "Prefer tests and lightweight test infrastructure.",
    "docs": "Prefer Markdown and .github/ai-factory planning files.",
    "security": "Prefer configuration, validation, and targeted security fixes.",
}


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def output(name: str, value: str) -> None:
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as handle:
            handle.write(f"{name}={value}\n")
    else:
        print(f"{name}={value}")


def main() -> int:
    if (ROOT / "AUTOPILOT_STOP").exists() and os.environ.get("EMERGENCY_OVERRIDE") != "true":
        output("enabled", "false")
        output("matrix", "[]")
        output("batch_size", "0")
        return 0

    config = load_json(FACTORY_DIR / "config.json", {})
    queue = load_json(FACTORY_DIR / "task_queue.json", {"tasks": []})
    tasks = queue.get("tasks", [])

    event_name = os.environ.get("GITHUB_EVENT_NAME", "")
    schedule = os.environ.get("GITHUB_EVENT_SCHEDULE", "")
    requested_batch = os.environ.get("REQUESTED_BATCH_SIZE", "").strip()
    requested_role = os.environ.get("REQUESTED_ROLE", "").strip()

    if requested_batch:
        batch_size = int(requested_batch)
    elif event_name == "schedule" and schedule == "37 1 * * *":
        batch_size = int(config.get("meta_batch_size", 4))
    else:
        batch_size = int(config.get("main_batch_size", 12))

    max_concurrent = int(config.get("max_concurrent", 12))
    batch_size = max(0, min(batch_size, max_concurrent))

    role_cycle = config.get("role_cycle") or list(ROLE_PROMPTS)
    lanes = config.get("lanes") or ["backend", "frontend", "tests", "docs"]
    now = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")

    matrix = []
    for index in range(batch_size):
        queued = tasks[index % len(tasks)] if tasks else {}
        role = requested_role or queued.get("role") or role_cycle[index % len(role_cycle)]
        lane = queued.get("lane") or lanes[index % len(lanes)]
        title = queued.get("title") or f"{role.title()} improvement {index + 1}"
        task_prompt = queued.get("prompt") or "Find one meaningful improvement and implement it safely."
        task_id = queued.get("id") or f"{role}-{lane}-{index + 1}"

        matrix.append(
            {
                "slot": index + 1,
                "task_id": f"{task_id}-{now}-{index + 1}",
                "role": role,
                "lane": lane,
                "title": title,
                "role_prompt": ROLE_PROMPTS.get(role, ROLE_PROMPTS["implementer"]),
                "lane_rules": LANE_RULES.get(lane, "Keep changes focused and small."),
                "task_prompt": task_prompt,
            }
        )

    output("enabled", "true")
    output("matrix", json.dumps(matrix, separators=(",", ":")))
    output("batch_size", str(batch_size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

