import os
files = [f for f in os.listdir('/tmp') if f.startswith('chunk_agents_')]
filenames = ' '.join([f'/tmp/{f}' for f in files])
with open("plan.txt", "w") as f:
    f.write(f"1. rm -rf {filenames} chunk_agents.py plan_script.py plan.txt\n")
    f.write("2. python -m compileall backend skills_library run.py\n")
    f.write("3. python .github/scripts/scan_secrets.py\n")
    f.write("4. python -m pytest -q\n")
    f.write("5. Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.\n")
    f.write("6. Call the `done` tool to report that no meaningful safe change exists, placing the complete, single-sentence justification synthesizing all executed tools and explored files within this step.\n")
