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


DEFAULT_HOURLY_ROLE_PLAN = [
    ["planner", "implementer", "tester", "reviewer"],
    ["implementer", "implementer", "tester", "documenter"],
    ["implementer", "refactorer", "tester", "security"],
    ["architect", "implementer", "tester", "reviewer"],
    ["planner", "implementer", "tester", "security"],
    ["implementer", "refactorer", "documenter", "tester"],
]


DEFAULT_QUARTER_HOUR_ROLE_SEQUENCE = [
    "planner",
    "implementer",
    "tester",
    "reviewer",
    "implementer",
    "implementer",
    "tester",
    "documenter",
    "implementer",
    "refactorer",
    "tester",
    "security",
    "architect",
    "implementer",
    "tester",
    "reviewer",
    "planner",
    "implementer",
    "tester",
    "security",
    "implementer",
    "refactorer",
    "documenter",
    "tester",
]


DEFAULT_META_ROLE_PLAN = ["planner", "architect", "reviewer", "documenter"]


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


def task_matches(task: dict, role: str) -> bool:
    return task.get("role") == role


def select_task(tasks: list[dict], role: str, global_index: int) -> dict:
    matching = [task for task in tasks if task_matches(task, role)]
    if matching:
        return matching[global_index % len(matching)]

    if tasks:
        return tasks[global_index % len(tasks)]

    return {}


def build_role_slots(config: dict, batch_size: int, schedule: str, requested_role: str) -> list[str]:
    if requested_role:
        return [requested_role] * batch_size

    if schedule == "37 1 * * *":
        meta_roles = config.get("meta_role_plan") or DEFAULT_META_ROLE_PLAN
        return [meta_roles[index % len(meta_roles)] for index in range(batch_size)]

    quarter_sequence = config.get("quarter_hour_role_sequence") or DEFAULT_QUARTER_HOUR_ROLE_SEQUENCE
    if batch_size == 1 and schedule != "7 * * * *":
        now = datetime.now(timezone.utc)
        quarter_index = (now.hour * 4) + (now.minute // 15)
        return [quarter_sequence[quarter_index % len(quarter_sequence)]]

    hourly_plan = config.get("hourly_role_plan") or DEFAULT_HOURLY_ROLE_PLAN
    hour = datetime.now(timezone.utc).hour
    hour_roles = hourly_plan[hour % len(hourly_plan)]
    return [hour_roles[index % len(hour_roles)] for index in range(batch_size)]


def format_scope(value) -> str:
    if not value:
        return "No extra scope specified. Follow the lane constraints and AGENTS.md."
    if isinstance(value, list):
        return ", ".join(value)
    return str(value)


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

    role_slots = build_role_slots(config, batch_size, schedule, requested_role)
    lanes = config.get("lanes") or ["backend", "frontend", "tests", "docs"]
    now = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    global_index = int(datetime.now(timezone.utc).strftime("%j%H")) * max(batch_size, 1)

    matrix = []
    for index in range(batch_size):
        role = role_slots[index]
        queued = select_task(tasks, role, global_index + index)
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
                "write_scope": format_scope(queued.get("write_scope")),
                "avoid_scope": format_scope(queued.get("avoid_scope")),
                "risk_level": queued.get("risk_level", "medium"),
                "automerge_allowed": str(queued.get("automerge_allowed", False)).lower(),
            }
        )

    output("enabled", "true")
    output("matrix", json.dumps(matrix, separators=(",", ":")))
    output("batch_size", str(batch_size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

