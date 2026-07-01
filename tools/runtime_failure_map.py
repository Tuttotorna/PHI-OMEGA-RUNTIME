
from __future__ import annotations

import json
from pathlib import Path
from collections import Counter


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data" / "runtime_failure_map.json"


def load_map(path: Path = MAP_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_failure_map(data: dict) -> dict:
    cases = data.get("cases", [])
    decisions = Counter(case.get("runtime_decision", "UNKNOWN") for case in cases)
    systems = sorted({case.get("system", "") for case in cases if case.get("system")})
    hard_blocks = [
        case for case in cases
        if case.get("runtime_decision") == "HARD_BLOCK"
    ]

    return {
        "map_id": data.get("map_id"),
        "case_count": len(cases),
        "systems": systems,
        "decision_counts": dict(decisions),
        "hard_block_count": len(hard_blocks),
        "core_invariant": data.get("core_invariant"),
        "status": data.get("status"),
    }


def main() -> int:
    data = load_map()
    print(json.dumps(summarize_failure_map(data), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
