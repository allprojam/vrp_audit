"""Preregistration hash lock (invariants I-5, I-6).

lock  : sha256 a preregistration document, store it in runs/<name>_prereg.lock
verify: recompute and compare; exit non-zero on mismatch (I-5)
re-lock is deliberately not an option (I-6). Write an addendum instead.

Usage:
  python3 src/prereg.py lock   docs/HYPOTHESIS.md
  python3 src/prereg.py verify docs/HYPOTHESIS.md
"""
import hashlib, pathlib, sys, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent


def digest(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


def lock_name(p):
    stem = pathlib.Path(p).stem.lower()
    return ROOT / "runs" / f"{stem}_prereg.lock"


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("lock", "verify"):
        print(__doc__)
        return 2
    cmd, path = sys.argv[1], sys.argv[2]
    if not (ROOT / path).exists():
        print(f"no such prereg: {path}")
        return 2

    lock = lock_name(path)
    h = digest(path)

    if cmd == "lock":
        if lock.exists():
            # I-6: refuse to overwrite a lock. This is the guard, not a formality.
            old = lock.read_text().strip().splitlines()[0].split()[0]
            if old == h:
                print(f"already locked, identical hash: {lock.relative_to(ROOT)}")
                return 0
            print(f"REFUSING TO RE-LOCK {path}\n"
                  f"  existing lock: {old}\n  current hash : {h}\n"
                  f"I-6: a prereg is locked once. If it was wrong, write an addendum.")
            return 1
        lock.parent.mkdir(parents=True, exist_ok=True)
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        lock.write_text(f"{h}  {path}\nlocked {stamp}\n")
        print(f"locked {path}\n  {h}\n  -> {lock.relative_to(ROOT)}")
        return 0

    # verify
    if not lock.exists():
        print(f"NO LOCK for {path} - this is not a preregistered result (I-5)")
        return 1
    old = lock.read_text().strip().splitlines()[0].split()[0]
    ok = old == h
    print(f"{'OK' if ok else 'MISMATCH'}  {path}")
    print(f"  locked : {old}")
    print(f"  current: {h}")
    if not ok:
        print("I-5: the prereg changed after locking. Any result derived from it is not valid.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
