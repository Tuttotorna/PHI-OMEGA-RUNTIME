
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data" / "runtime_failure_map.json"


def test_runtime_failure_map_exists_and_has_cases():
    assert MAP_PATH.exists()
    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))

    assert data["map_id"] == "phi_omega_runtime_failure_map_001"
    assert data["status"] == "field_map_not_endorsement"
    assert "Valid(tau)" in data["core_invariant"]
    assert len(data["cases"]) >= 10


def test_runtime_failure_map_cases_have_required_shape():
    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))

    required = {
        "system",
        "repository",
        "issue",
        "title",
        "url",
        "observed_failure_class",
        "transition_tau",
        "required_tau",
        "supported_tau",
        "missing_support",
        "runtime_decision",
        "minimal_gate",
        "phi_omega_mapping",
    }

    valid_decisions = {"ALLOW", "REPAIR", "SOFT_BLOCK", "HARD_BLOCK"}

    for case in data["cases"]:
        assert required.issubset(case.keys())
        assert case["url"].startswith("https://github.com/")
        assert case["runtime_decision"] in valid_decisions
        assert isinstance(case["required_tau"], list)
        assert isinstance(case["supported_tau"], list)
        assert isinstance(case["missing_support"], list)


def test_runtime_failure_map_has_hard_block_cases():
    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    hard_blocks = [case for case in data["cases"] if case["runtime_decision"] == "HARD_BLOCK"]

    assert len(hard_blocks) >= 3
    assert any("hard" in " ".join(case["minimal_gate"].lower().split()) or "block" in case["minimal_gate"].lower() for case in hard_blocks)


def test_runtime_failure_map_summary_tool_runs():
    result = subprocess.run(
        [sys.executable, "tools/runtime_failure_map.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert output["case_count"] >= 10
    assert output["hard_block_count"] >= 3
    assert output["status"] == "field_map_not_endorsement"
