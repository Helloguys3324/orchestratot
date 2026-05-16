#!/usr/bin/env python3
"""Decide whether a PR is safe for AI Factory automerge."""

from __future__ import annotations

import json
import os
import subprocess
import sys


SAFE_PREFIXES = (
    "ai-factory(documenter):",
    "ai-factory(tester):",
)
SAFE_LABEL = "ai-factory:safe-automerge"


def run_json(args: list[str]):
    raw = subprocess.check_output(args, text=True)
    return json.loads(raw)


def output(name: str, value: str) -> None:
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as handle:
            handle.write(f"{name}={value}\n")
    else:
        print(f"{name}={value}")


def main() -> int:
    sha = os.environ["WORKFLOW_HEAD_SHA"]
    prs = run_json([
        "gh",
        "api",
        f"/repos/{os.environ['GITHUB_REPOSITORY']}/commits/{sha}/pulls",
        "-H",
        "Accept: application/vnd.github+json",
    ])

    if not prs:
        output("allowed", "false")
        output("reason", "no_pr_for_sha")
        return 0

    pr = prs[0]
    title = pr.get("title", "")
    labels = [label.get("name", "") for label in pr.get("labels", [])]
    number = str(pr["number"])

    allowed = (
        not pr.get("draft", False)
        and SAFE_LABEL in labels
        and title.startswith(SAFE_PREFIXES)
    )

    output("pr", number)
    output("allowed", "true" if allowed else "false")
    output("reason", "allowed" if allowed else "missing_safe_title_or_label")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

