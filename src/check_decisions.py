"""Check that every decision ID cited in this repo is defined in this repo.

Cross-repo IDs are not portable: gold_macro and falsifier share an A-NN identifier space
with partial overlap and divergent definitions (A-06..A-08 were rewritten, not copied;
gold_macro owns A-09..A-20; falsifier owns A-24). A bare `A-23` is therefore ambiguous the
moment a second repo exists.

Rule: cite cross-project IDs as `repo:A-NN`. Any bare `A-NN` found here must be defined here.

Usage: python3 src/check_decisions.py
"""
import re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEC = ROOT / "DECISIONS.md"
SCAN_SUFFIXES = {".md", ".py"}
SKIP_DIRS = {".git", "__pycache__"}

DEF = re.compile(r"^###\s+(A-\d{2})\b", re.M)
CITE = re.compile(r"(?<![A-Za-z0-9_:-])(A-\d{2})(?![0-9])")


def main():
    if not DEC.exists():
        print("no DECISIONS.md")
        return 1
    defined = set(DEF.findall(DEC.read_text()))

    orphans = []
    for f in ROOT.rglob("*"):
        if not f.is_file() or f.suffix not in SCAN_SUFFIXES:
            continue
        if SKIP_DIRS & set(f.parts):
            continue
        for i, line in enumerate(f.read_text(errors="replace").splitlines(), 1):
            for m in CITE.finditer(line):
                # `repo:A-NN` is an explicit cross-project reference, not this repo's
                if ":" in line[max(0, m.start() - 24):m.start()]:
                    continue
                # the ID-map table lists foreign ranges on purpose
                if "gold_macro" in line or "falsifier" in line:
                    continue
                if m.group(1) not in defined:
                    orphans.append(f"  ORPHAN  {f.relative_to(ROOT)}:{i}  cites {m.group(1)} (not defined here)")

    print(f"decision-ID check: {len(defined)} IDs defined, {len(orphans)} orphan citation(s)")
    if orphans:
        print("\n".join(orphans))
        print("\nRESULT: FAIL - cite cross-project IDs as repo:A-NN")
        return 1
    print("RESULT: PASS - every bare A-NN cited here is defined here")
    return 0


if __name__ == "__main__":
    sys.exit(main())
