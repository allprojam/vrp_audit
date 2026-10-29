"""Run every executable invariant check. Exit non-zero if any fails."""
import subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECKS = [("provenance (A-22/A-23)", ["src/check_provenance.py"]),
          ("decision IDs (repo:A-NN)", ["src/check_decisions.py"]),
          ("prereg hash (I-5/I-6)", ["src/prereg.py", "verify", "docs/HYPOTHESIS.md"])]

failed = 0
for name, cmd in CHECKS:
    r = subprocess.run([sys.executable] + cmd, cwd=ROOT, capture_output=True, text=True)
    last = [l for l in r.stdout.strip().splitlines() if l.strip()]
    print(f"[{'PASS' if r.returncode == 0 else 'FAIL'}] {name}")
    if last:
        print(f"        {last[-1]}")
    failed += r.returncode != 0

print(f"\n{len(CHECKS) - failed}/{len(CHECKS)} checks passed")
sys.exit(1 if failed else 0)
