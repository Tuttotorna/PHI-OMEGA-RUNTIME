from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def _load_tool_module():
    repo_root = Path(__file__).resolve().parents[2]
    tool_path = repo_root / "tools" / "agent_exchange_loop_eval.py"
    if not tool_path.exists():
        raise SystemExit(f"agent_exchange_loop_eval.py not found at {tool_path}")

    spec = importlib.util.spec_from_file_location("_phi_omega_agent_exchange_loop_eval_tool", tool_path)
    if spec is None or spec.loader is None:
        raise SystemExit("Could not load agent exchange-loop eval tool.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Provide one JSON file path."}, indent=2))
        return 2

    module = _load_tool_module()

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        case = json.load(f)

    result = module.evaluate_agent_exchange_loop(case)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result.get("status") == "INVALID_AGENT_EVAL_INPUT":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
