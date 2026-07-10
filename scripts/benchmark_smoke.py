import importlib
import sys
import time
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))


MODULES = (
    "core_settings",
    "gorev_modeli",
    "hatirlatici_modeli",
    "gorev_servisi",
    "hatirlatici_servisi",
    "bildirim_servisi",
)


def main():
    results = []
    total_start = time.perf_counter()
    for name in MODULES:
        start = time.perf_counter()
        importlib.import_module(name)
        results.append((name, (time.perf_counter() - start) * 1000))

    total_ms = (time.perf_counter() - total_start) * 1000
    print(f"Benchmark imports: {len(MODULES)} modules in {total_ms:.1f} ms")
    for name, ms in results:
        print(f"- {name}: {ms:.1f} ms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
