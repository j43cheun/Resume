#!/usr/bin/env python3
"""
ATS compliance checks for the compiled resume PDF.

Guards against the specific structural/text-extraction issues found (and fixed)
during development. This only checks that the PDF's text layer is sound and
machine-readable — it does not validate anything about what the content actually
says:
  - Multi-page overflow
  - Non-embedded fonts (portability across ATS parsers/viewers)
  - Missing-space run-on words (a justification/text-layer bug)
  - Small-caps fonts silently corrupting capital "I" into lowercase "i"

Usage:
    python3 scripts/validate_ats.py resume.pdf [--max-pages N]

Exits non-zero (failing CI) if any check fails.
"""
import argparse
import re
import subprocess
import sys


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout


def check_page_count(pdf_path, max_pages):
    info = run(["pdfinfo", pdf_path])
    match = re.search(r"^Pages:\s*(\d+)", info, re.MULTILINE)
    if not match:
        return False, "Could not determine page count"
    pages = int(match.group(1))
    if pages > max_pages:
        return False, f"Resume is {pages} page(s), expected at most {max_pages}"
    return True, f"{pages} page(s)"


def check_fonts_embedded(pdf_path):
    fonts = run(["pdffonts", pdf_path])
    lines = fonts.strip().split("\n")[2:]  # skip the two header rows
    not_embedded = []
    for line in lines:
        parts = line.split()
        if len(parts) < 5:
            continue
        # Columns are: name type encoding emb sub uni object ID
        # "type" and "name" can each contain a variable number of words, but
        # emb/sub/uni/object/ID are always the last 5 whitespace-separated tokens.
        emb = parts[-5]
        name = parts[0]
        if emb != "yes":
            not_embedded.append(name)
    if not_embedded:
        return False, f"Font(s) not embedded: {', '.join(not_embedded)}"
    return True, "All fonts embedded"


def check_no_runon_words(text, max_word_len=25):
    words = re.findall(r"[A-Za-z]+", text)
    offenders = sorted({w for w in words if len(w) > max_word_len})
    if offenders:
        return False, (
            f"Suspiciously long word(s) found, likely a missing-space/justification "
            f"bug: {offenders[:5]}"
        )
    return True, "No run-on words detected"


def check_no_smallcaps_corruption(text):
    # Catches the specific bug this resume hit: a font's small-caps feature
    # substituting the lowercase "i" glyph for a stylized capital I, which then
    # extracts as lowercase. Heuristic: an otherwise-all-caps word containing a
    # lone lowercase "i".
    pattern = r"\b(?:[A-Z]{2,}i[A-Z]*|[A-Z]*i[A-Z]{2,})\b"
    offenders = sorted(set(re.findall(pattern, text)))
    if offenders:
        return False, f"Possible small-caps corruption (capital I read as 'i'): {offenders[:5]}"
    return True, "No small-caps corruption detected"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path")
    parser.add_argument("--max-pages", type=int, default=1)
    args = parser.parse_args()

    # Deliberately not "-raw": that mode dumps text in raw content-stream order and
    # infers word boundaries purely from the size of the TJ-array position number
    # between glyph runs. This template's embedded CID-keyed OpenType fonts never
    # emit an actual space glyph (xdvipdfmx encodes word gaps as pure positioning,
    # not characters), so -raw's threshold is the only thing standing between a
    # word gap and "missing-space run-on words" — and that threshold differs across
    # poppler versions, so the identical PDF can pass on one machine and fail on
    # another (confirmed: poppler 22.02 vs 26.07 disagreed on this exact file).
    # Default (layout) mode instead reconstructs word gaps from glyph geometry
    # across the whole line, which is what real ATS parsers and copy/paste
    # actually approximate, and agrees with pdfminer.six's independent geometric
    # extraction on this file where -raw does not. See the comment above
    # \XeTeXgenerateactualtext in resume.tex for the full investigation.
    text = run(["pdftotext", args.pdf_path, "-"])

    checks = [
        ("Page count", check_page_count(args.pdf_path, args.max_pages)),
        ("Font embedding", check_fonts_embedded(args.pdf_path)),
        ("No run-on words", check_no_runon_words(text)),
        ("No small-caps corruption", check_no_smallcaps_corruption(text)),
    ]

    failed = False
    for name, (ok, message) in checks:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {name}: {message}")
        if not ok:
            failed = True

    if failed:
        print("\nATS validation FAILED.")
        sys.exit(1)
    print("\nATS validation passed.")


if __name__ == "__main__":
    main()
