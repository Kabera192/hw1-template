#!/usr/bin/env python3
"""Create your submission zip with the right name and the right files.

    python3 tests/make_zip.py 12345          (use YOUR numeric student ID)
    make zip ID=12345                         (same thing, if you have make)

It checks that the required files exist, that your code compiles with the
course flags, and then writes the zip in this folder. Upload that zip to the
Google Form. (Pushing to GitHub is NOT a submission.)
"""
import json
import subprocess
import sys
import zipfile
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    spec = json.loads((HERE / "visible_tests.json").read_text(encoding="utf-8"))
    if len(sys.argv) != 2 or not re.fullmatch(r"[A-Za-z0-9-]+", sys.argv[1]):
        print("Usage: python3 tests/make_zip.py <your numeric student ID>")
        return 2
    sid = sys.argv[1]
    missing = [f for f in spec["required"] if not (ROOT / f).exists()]
    if missing:
        print("Missing required file(s): " + ", ".join(missing))
        return 1
    c = spec["compile"]
    try:
        r = subprocess.run([c["compiler"]] + c["flags"] + c["sources"] + ["-o", spec["executable"] + "_zipcheck"]
                           + c["ldlibs"], cwd=ROOT, capture_output=True, text=True)
        for p in ROOT.glob(spec["executable"] + "_zipcheck*"):
            p.unlink()
        if r.returncode != 0:
            print(r.stderr)
            print("WARNING: your code does NOT compile with the course flags. It would score 0 on all tests.")
            if input("Create the zip anyway? [y/N] ").strip().lower() != "y":
                return 1
    except FileNotFoundError:
        print(f"(could not find {c['compiler']} to check compilation; continuing)")
    name = spec["zip_name"].format(assignment_id=spec["assignment_id"], student_id=sid)
    with zipfile.ZipFile(ROOT / name, "w", zipfile.ZIP_DEFLATED) as z:
        for f in spec["required"] + [f for f in spec.get("optional_present", []) if (ROOT / f).exists()]:
            z.write(ROOT / f, arcname=f)
    with zipfile.ZipFile(ROOT / name) as z:
        print(f"Created {name} containing: " + ", ".join(z.namelist()))
    print("Now upload it to the Google Form: " + (spec.get("form_url") or "(see the assignment write-up)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
