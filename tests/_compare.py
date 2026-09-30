"""Output comparison shared by the grader AND the student test runner.

Stdlib only, so it can be copied verbatim into the student repo. Keeping one
copy of this logic means "passes locally" and "passes in grading" agree.
"""
from __future__ import annotations

import re

MODES = (
    "exact",                       # byte-for-byte (after decoding), incl. trailing newline
    "ignore_trailing_whitespace",  # trailing spaces/tabs per line and trailing blank lines ignored
    "normalize_whitespace",        # all runs of whitespace treated as one space
    "ignore_case",                 # exact, but case-insensitive
    "contains",                    # expected text must appear somewhere in output
    "regex",                       # expected is a Python regex that must match the whole output
)


def _rstrip_lines(s: str) -> str:
    lines = [ln.rstrip(" \t\r") for ln in s.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def matches(expected: str, actual: str, mode: str = "exact") -> bool:
    if mode == "exact":
        return expected == actual
    if mode == "ignore_trailing_whitespace":
        return _rstrip_lines(expected) == _rstrip_lines(actual)
    if mode == "normalize_whitespace":
        return expected.split() == actual.split()
    if mode == "ignore_case":
        return expected.casefold() == actual.casefold()
    if mode == "contains":
        return expected in actual
    if mode == "regex":
        return re.fullmatch(expected, actual, re.DOTALL) is not None
    raise ValueError(f"unknown compare mode: {mode}")


def explain(expected: str, actual: str, mode: str = "exact") -> str | None:
    """A one-sentence, human explanation of an 'invisible' difference, or None."""
    if mode in ("contains", "regex"):
        return None
    if actual == "" and expected != "":
        return "Your program printed nothing."
    if "\r\n" in actual and actual.replace("\r\n", "\n") == expected:
        return ("Only difference: your output uses Windows line endings (\\r\\n). "
                "Print \\n only.")
    if actual.rstrip("\n") == expected.rstrip("\n"):
        exp_nl = len(expected) - len(expected.rstrip("\n"))
        act_nl = len(actual) - len(actual.rstrip("\n"))
        if act_nl < exp_nl:
            return ("Only difference: your output is missing the newline (\\n) at the very end. "
                    "Every line of output, including the last one, must end with \\n.")
        return "Only difference: your output has extra blank line(s) at the end."
    if _rstrip_lines(actual) == _rstrip_lines(expected):
        return "Only difference: extra spaces or tabs at the end of a line."
    if actual.split() == expected.split():
        return "Only difference is spacing or blank lines (the words and numbers are right)."
    if actual.casefold() == expected.casefold():
        return "Only difference is upper/lower case."
    return None


def show(s: str, ascii_only: bool = False) -> str:
    """Make whitespace visible. Unicode: space=·  tab=→  newline=↵.
    ASCII fallback (like `cat -A`): tab=^I, CR=^M, end of line=$ ."""
    if ascii_only:
        return s.replace("\t", "^I").replace("\r", "^M").replace("\n", "$")
    return (s.replace(" ", "·").replace("\t", "→").replace("\r", "␍")
            .replace("\n", "↵"))


LEGEND = "Whitespace markers: · = space, → = tab, ↵ = newline (end of line)"
LEGEND_ASCII = "Whitespace markers: $ = newline (end of line), ^I = tab, ^M = carriage return"


def _clip(text: str, width: int) -> str:
    return text if len(text) <= width else text[: width - 3] + "..."


def excerpt(expected: str, actual: str, context: int = 1, max_lines: int = 6,
            width: int = 90, ascii_only: bool = False) -> list[str]:
    """Short expected-vs-actual excerpt around the first differing line."""
    exp = expected.splitlines(keepends=True) or [""]
    act = actual.splitlines(keepends=True) or [""]
    first = 0
    while first < len(exp) and first < len(act) and exp[first] == act[first]:
        first += 1
    start = max(0, first - context)
    out = [f"(first difference at line {first + 1})"]
    for label, lines in (("Expected", exp), ("Got", act)):
        out.append(f"{label}:")
        shown = lines[start:start + max_lines]
        for i, ln in enumerate(shown, start=start + 1):
            if ln == "" and i == 1 and len(lines) == 1:
                out.append("    (no output)")
                continue
            out.append(f"  {i:>3}| " + _clip(show(ln, ascii_only), width))
        rest = len(lines) - (start + len(shown))
        if rest > 0:
            out.append(f"       ... ({rest} more line{'s' if rest != 1 else ''})")
    return out
