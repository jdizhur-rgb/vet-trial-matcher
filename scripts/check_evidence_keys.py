"""Redact copied Google API keys and reject them before publication.

Public source HTML/JSON can contain third-party browser keys. Their presence
on a public page is not permission to republish them in audit evidence.
This targeted gate is not a replacement for GitHub secret scanning.
"""
import argparse
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
GOOGLE_API_KEY = re.compile(r"AIza[A-Za-z0-9_-]{35}")
REPLACEMENT = "[REDACTED_GOOGLE_API_KEY]"


def redact_text(text):
    """Preserve evidence content except for credential-shaped values."""
    return GOOGLE_API_KEY.sub(REPLACEMENT, text)


def repository_files(root):
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=root, check=True, stdout=subprocess.PIPE,
    )
    return sorted({root / name.decode() for name in result.stdout.split(b"\0") if name})


def check_files(paths, *, redact=False):
    findings = 0
    for path in paths:
        if path.is_symlink() or not path.is_file():
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        matches = list(GOOGLE_API_KEY.finditer(original))
        if not matches:
            continue
        findings += len(matches)
        # Never print the value, surrounding text or credential-bearing URLs.
        lines = sorted({original.count("\n", 0, m.start()) + 1 for m in matches})
        print(f"{path}: {len(matches)} Google API key occurrence(s); lines {lines}")
        if redact:
            path.write_text(redact_text(original), encoding="utf-8")
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--redact", action="store_true", help="Redact only explicit files/directories")
    args = parser.parse_args()
    if args.redact and not args.paths:
        parser.error("--redact requires explicit evidence paths")
    paths = []
    for path in args.paths:
        if not path.exists():
            parser.error(f"path does not exist: {path}")
        paths.extend(path.rglob("*") if path.is_dir() else [path])
    findings = check_files(paths if args.paths else repository_files(ROOT), redact=args.redact)
    if findings and not args.redact:
        print(f"FAIL: {findings} unredacted Google API key occurrence(s).")
        return 1
    print(f"PASS: {'redacted ' + str(findings) + ' occurrence(s)' if args.redact else 'no unredacted Google API keys'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
