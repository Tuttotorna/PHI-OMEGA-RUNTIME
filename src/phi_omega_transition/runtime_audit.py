from __future__ import annotations

import runpy
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    script = repo_root / "run_phi_omega.py"
    if not script.exists():
        raise SystemExit(f"run_phi_omega.py not found at {script}")
    runpy.run_path(str(script), run_name="__main__")


if __name__ == "__main__":
    main()
