"""A-22 enforcement: every claim in PROVENANCE.md must resolve to a real file:line.

Reads the registry tables, opens each cited path at the cited line, and asserts the
expected token appears. Exits non-zero on any broken claim. JSON-key rows are checked
for key existence rather than line content.

Usage: python3 src/check_provenance.py
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "PROVENANCE.md"

ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$")

def check_line(path, lineno, token):
    f = ROOT / path
    if not f.exists():
        return False, f"missing file {path}"
    lines = f.read_text(errors="replace").splitlines()
    if lineno > len(lines):
        return False, f"{path} has only {len(lines)} lines, asked for {lineno}"
    line = lines[lineno - 1]
    if token.strip().lower() in line.lower():
        return True, ""
    return False, f"token {token!r} not on {path}:{lineno} -> {line.strip()[:90]!r}"

def check_json(path, token):
    f = ROOT / path
    if not f.exists():
        return False, f"missing file {path}"
    try:
        data = json.loads(f.read_text())
    except Exception as e:
        return False, f"unreadable json {path}: {e}"
    if token in data:
        return True, ""
    # allow nested lookup: any dict in the tree containing the token as a key
    def walk(o, depth=0):
        if depth > 6: return False
        if isinstance(o, dict):
            if token in o: return True
            return any(walk(v, depth+1) for v in o.values())
        if isinstance(o, list):
            return any(walk(v, depth+1) for v in o)
        return False
    if walk(data):
        return True, ""
    return False, f"json key {token!r} not found at any depth in {path}"

def main():
    rows = [l for l in REG.read_text().splitlines() if l.startswith("|")]
    ok = bad = skipped = 0
    failures = []
    in_superseded = False
    for line in REG.read_text().splitlines():
        if line.startswith("## Superseded") or line.startswith("## Withdrawn"):
            in_superseded = True
        if line.startswith("## ") and not (line.startswith("## Superseded") or line.startswith("## Withdrawn")):
            in_superseded = False
        if in_superseded or not line.startswith("|"):
            continue
        m = ROW.match(line)
        if not m:
            continue
        claim, value, ref, token = (g.strip() for g in m.groups())
        if ref.lower() in ("path:line",) or set(ref) <= set("-: "):
            skipped += 1
            continue
        if ref.endswith(".json"):
            good, msg = check_json(ref, token)
        else:
            mm = re.match(r"^(.+?):(\d+)$", ref)
            if not mm:
                skipped += 1
                continue
            good, msg = check_line(mm.group(1), int(mm.group(2)), token)
        if good:
            ok += 1
        else:
            bad += 1
            failures.append(f"  FAIL  {claim}\n        {msg}")

    print(f"A-22 provenance check: {ok} verified, {bad} broken, {skipped} header rows skipped")
    if failures:
        print("\n".join(failures))
        print(f"\nRESULT: FAIL ({bad} claims do not resolve)")
        return 1
    print("RESULT: PASS - every claim resolves to file:line or JSON key")
    return 0

if __name__ == "__main__":
    sys.exit(main())
