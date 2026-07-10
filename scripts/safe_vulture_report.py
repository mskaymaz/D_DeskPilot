import argparse
import re
import subprocess
import sys
from pathlib import Path


IGNORED_DIRS = {".git", ".venv", "venv", "__pycache__", "dist", "build"}


def python_files(root):
    return [
        path
        for path in root.rglob("*.py")
        if not any(part in IGNORED_DIRS for part in path.parts)
    ]


def run_cmd(cmd):
    proc = subprocess.run(cmd, text=True, capture_output=True)
    return proc.returncode, proc.stdout + proc.stderr


def parse_vulture_line(line):
    match = re.match(r"^(.*?):(\d+): unused .*?'([^']+)'", line)
    if not match:
        return None
    return Path(match.group(1)), int(match.group(2)), match.group(3)


def has_project_reference(files, symbol, definition_file, definition_line):
    pattern = re.compile(rf"\b{re.escape(symbol)}\b")
    for path in files:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = path.read_text(encoding="utf-8-sig").splitlines()
        for line_no, text in enumerate(lines, 1):
            if path == definition_file and line_no == definition_line:
                continue
            if pattern.search(text):
                return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Dry-run Vulture report with project-wide reference verification.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    files = python_files(root)
    code, output = run_cmd(["vulture", *map(str, files), "--min-confidence", "0"])
    if code not in (0, 1) and "unused" not in output:
        print(output.strip())
        return code

    candidates = [item for item in (parse_vulture_line(line) for line in output.splitlines()) if item]
    safe = []
    skipped = []
    for path, line_no, symbol in candidates:
        if has_project_reference(files, symbol, path.resolve(), line_no):
            skipped.append((path, line_no, symbol))
        else:
            safe.append((path, line_no, symbol))

    print(f"Vulture candidates: {len(candidates)}")
    print(f"Safe after reference check: {len(safe)}")
    print(f"Skipped referenced: {len(skipped)}")
    for path, line_no, symbol in safe[:20]:
        print(f"SAFE {path}:{line_no}: {symbol}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
