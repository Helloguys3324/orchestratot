1. rm -rf plan.txt plan.md
2. python -m compileall backend skills_library run.py
3. python .github/scripts/scan_secrets.py
4. python -m pytest -q
5. Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
6. Call the `done` tool to report that no meaningful safe change exists, placing the complete, single-sentence justification synthesizing all executed tools and explored files within this step.
