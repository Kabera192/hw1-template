#!/usr/bin/env python3
"""Run the VISIBLE tests for this assignment on your own computer.

    python3 tests/run_tests.py            build, then run every visible test
    python3 tests/run_tests.py basic      run just one test (by name)
    python3 tests/run_tests.py --no-build use the program you already compiled

Works on Linux, macOS and Windows (needs gcc on your PATH: on Windows use WSL
or MSYS2/MinGW). The instructor's grader uses exactly the same comparison
code (tests/_compare.py), plus some HIDDEN tests you can't see.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import _compare as compare  # noqa: E402

try:
    "·↵".encode(sys.stdout.encoding or "ascii")
    ASCII = False
except (UnicodeEncodeError, LookupError):
    ASCII = True


def main():
    spec = json.loads((HERE / "visible_tests.json").read_text(encoding="utf-8"))
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    exe = spec["executable"] + (".exe" if os.name == "nt" else "")
    exe_path = ROOT / exe
    c = spec["compile"]
    if "--no-build" not in sys.argv:
        cmd = [c["compiler"]] + c["flags"] + c["sources"] + ["-o", exe] + c["ldlibs"]
        print("Compiling: " + " ".join(cmd))
        try:
            r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        except FileNotFoundError:
            print(f"Could not run '{c['compiler']}'. Is it installed and on your PATH?")
            return 2
        if r.returncode != 0:
            print(r.stderr or r.stdout)
            print("DOES NOT COMPILE. In grading this means 0 for every test.")
            if "-Werror" in c["flags"]:
                print("(Remember: in this course every warning counts as an error.)")
            return 1
        print("Compiled OK.\n")
    if not exe_path.exists():
        print(f"{exe} not found; build it first.")
        return 1
    tests = [t for t in spec["tests"] if not args or t["id"] in args]
    passed = 0
    for t in tests:
        stdin = t["stdin"].encode()
        try:
            r = subprocess.run([str(exe_path)] + t["args"], input=stdin, capture_output=True,
                               timeout=t["timeout"], cwd=ROOT)
            out = r.stdout.decode("utf-8", errors="replace")
            timed_out = False
        except subprocess.TimeoutExpired:
            timed_out, out, r = True, "", None
        mode = t["compare"]
        if timed_out:
            ok, why = False, f"Time limit exceeded ({t['timeout']}s): infinite loop, or waiting for input?"
        elif r.returncode < 0 or (os.name == "nt" and r.returncode >= 0xC0000000):
            ok, why = False, f"Crashed (exit status {r.returncode})."
        elif not compare.matches(t["expected"], out, mode):
            ok, why = False, compare.explain(t["expected"], out, mode) or "Output did not match."
        elif t["expected_exit"] not in (None, "any") and r.returncode != int(t["expected_exit"]):
            ok, why = False, f"Output correct, but exit status {r.returncode} (expected {t['expected_exit']})."
        else:
            ok, why = True, ""
        print(f"[{'PASS' if ok else 'FAIL'}] {t['id']}: {t['description']}")
        if ok:
            passed += 1
            continue
        print("       " + why)
        if not timed_out and mode not in ("contains", "regex") and not compare.matches(t["expected"], out, mode):
            for ln in compare.excerpt(t["expected"], out, ascii_only=ASCII):
                print("       " + ln)
        if t.get("hint") and not why.startswith("Only difference"):
            print("       Hint: " + t["hint"])
    print(f"\n{passed}/{len(tests)} visible tests passed.")
    if spec.get("hidden_count"):
        print(f"Note: grading also uses {spec['hidden_count']} hidden tests, so passing everything here "
              "does not guarantee full marks. Think about edge cases!")
    print(compare.LEGEND_ASCII if ASCII else compare.LEGEND)
    return 0 if passed == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())
