#!/usr/bin/env python3
"""Block AI Factory PRs from changing GitHub workflow files."""

from __future__ import annotations

import os
import subprocess
import sys


PROTECTED_PREFIXES = (
    ".github/workflows/",
)
AI_BRANCH_MARKERS = (
    "ai-factory/",
    "jules/",
)


def changed_files() -> list[str]:
    base_ref = os.environ.get("GITHUB_BASE_REF")
    if base_ref:
        subprocess.run(["git", "fetch", "origin", base_ref, "--depth=1"], check=False)
        diff_base = f"origin/{base_ref}"
        raw = subprocess.check_output(["git", "diff", "--name-only", f"{diff_base}...HEAD"], text=True)
        return [line.strip() for line in raw.splitlines() if line.strip()]

    raw = subprocess.check_output(["git", "diff", "--name-only", "HEAD~1..HEAD"], text=True)
    return [line.strip() for line in raw.splitlines() if line.strip()]


def is_ai_change() -> bool:
    head_ref = os.environ.get("GITHUB_HEAD_REF", "")
    actor = os.environ.get("GITHUB_ACTOR", "")
    event_name = os.environ.get("GITHUB_EVENT_NAME", "")
    return (
        event_name == "pull_request"
        and (head_ref.startswith(AI_BRANCH_MARKERS) or "jules" in actor.lower())
    )


def main() -> int:
    files = changed_files()
    protected = [path for path in files if path.startswith(PROTECTED_PREFIXES)]

    if protected and is_ai_change():
        print("AI Factory PRs are not allowed to modify GitHub workflow files:")
        print("\n".join(protected))
        print("Create a human-reviewed infrastructure PR instead.")
        return 1

    print("Workflow guard passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

