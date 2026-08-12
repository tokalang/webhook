#!/usr/bin/env python3
"""Compile and execute the bounded direct-dispatch qualification."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
TOKA = ROOT.parent / "toka"


def run(argv: list[str]) -> None:
    completed = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True)
    if completed.returncode:
        raise RuntimeError(
            f"command failed: {' '.join(argv)}\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )


def main() -> int:
    tokac = TOKA / "build" / "bin" / "tokac"
    runtime = TOKA / "lib" / "sys" / "toka_rt.o"
    if not tokac.is_file() or not runtime.is_file():
        raise RuntimeError("build ../toka and its runtime object before qualifying")

    with tempfile.TemporaryDirectory(prefix="toka-webhook-") as temporary:
        for name in ("config", "dispatch", "signatures", "loopback"):
            program = Path(temporary) / name
            run([str(tokac), "-I", str(TOKA / "lib"), "-I", str(ROOT / "src"),
                 str(ROOT / "tests" / (name + ".tk")), "-o", str(program)])
            run([str(program)])
    run([sys.executable, str(ROOT / "tests" / "cli_qualify.py")])
    print("toka-webhook qualification: PASSED")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
