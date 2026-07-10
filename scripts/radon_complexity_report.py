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


def main():
    parser = argparse.ArgumentParser(description="Dry-run Radon complexity report. No refactor is performed.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--threshold", type=int, default=10)
    args = parser.parse_args()

    files = python_files(Path(args.root).resolve())
    code, output = run_cmd(["radon", "cc", "-a", "-s", *map(str, files)])
    if code != 0:
        print(output.strip())
        return code

    item_re = re.compile(r"^\s+(.+?)\s+-\s+([A-F])\s+\((\d+)\)")
    high = []
    current_file = ""
    for line in output.splitlines():
        if line.endswith(".py"):
            current_file = line.strip()
            continue
        match = item_re.match(line)
        if match and int(match.group(3)) >= args.threshold:
            high.append((current_file, match.group(1), match.group(2), match.group(3)))

    print(f"Radon high complexity >= {args.threshold}: {len(high)}")
    for path, member, grade, score in high[:30]:
        print(f"HIGH {path}: {member} {grade}({score})")
    print("No refactor performed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
