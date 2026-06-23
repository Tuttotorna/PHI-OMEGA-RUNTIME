import json
import subprocess
import sys
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "agent_exchange_loop_eval.py"
DOC = ROOT / "AGENT_EXCHANGE_LOOP_EVAL.md"
VALID = ROOT / "examples" / "agent_exchange_loop_valid_case.json"
FALSE_SUFF = ROOT / "examples" / "agent_false_sufficiency_case.json"
FIELD_FAIL = ROOT / "examples" / "agent_local_pass_field_fail_case.json"

def load_tool():
    spec = importlib.util.spec_from_file_location("agent_exchange_loop_eval", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_agent_exchange_loop_doc_contains_core_entry():
    assert DOC.exists()
    text = DOC.read_text(encoding="utf-8")
    assert "PHI-OMEGA-RUNTIME:AGENT_EXCHANGE_LOOP_EVAL:v0.1.3" in text
    assert "An agent run is treated as a state-change cycle" in text
    assert "PHI-OMEGA Agent Exchange-Loop Eval checks whether an AI agent has a real give/receive loop" in text

def test_valid_agent_exchange_loop_case_passes():
    mod = load_tool()
    result = mod.evaluate_agent_exchange_loop(read_json(VALID))
    assert result["status"] == "AGENT_EXCHANGE_LOOP_VALID"
    assert result["exchange_assessment"]["has_field_return"] is True
    assert result["exchange_assessment"]["field_incompatibility_detected"] is False
    assert not result["errors"]

def test_false_sufficiency_without_return_signal_is_detected():
    mod = load_tool()
    result = mod.evaluate_agent_exchange_loop(read_json(FALSE_SUFF))
    assert result["status"] == "FALSE_SUFFICIENCY_RISK"
    assert "Err_AGENT_NO_RETURN_SIGNAL" in result["errors"]
    assert "Err_AGENT_HIGH_CONFIDENCE_WITHOUT_FIELD_RETURN" in result["errors"]

def test_local_pass_field_failure_is_detected():
    mod = load_tool()
    result = mod.evaluate_agent_exchange_loop(read_json(FIELD_FAIL))
    assert result["status"] == "FALSE_SUFFICIENCY_RISK"
    assert "Err_AGENT_LOCAL_OUTPUT_FIELD_FAILURE" in result["errors"]
    assert result["exchange_assessment"]["field_incompatibility_detected"] is True

def test_safe_regression_language_is_not_field_failure():
    mod = load_tool()
    text = "Regression test passed. The parser now handles the edge case without API regression. No public API change."
    assert mod.has_field_incompatibility(text) is False

def test_missing_required_fields_invalid_input():
    mod = load_tool()
    result = mod.evaluate_agent_exchange_loop({
        "agent": "Incomplete agent case",
        "task_received": "Do something."
    })
    assert result["status"] == "INVALID_AGENT_EVAL_INPUT"
    assert "Err_AGENT_EVAL_SCHEMA_INCOMPLETE" in result["errors"]

def test_cli_valid_case_outputs_json():
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(VALID)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    assert proc.returncode == 0, proc.stdout
    data = json.loads(proc.stdout)
    assert data["status"] == "AGENT_EXCHANGE_LOOP_VALID"
    assert data["layer_version"] == "v0.1.3"

def test_cli_false_sufficiency_case_outputs_risk():
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(FALSE_SUFF)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    assert proc.returncode == 0, proc.stdout
    data = json.loads(proc.stdout)
    assert data["status"] == "FALSE_SUFFICIENCY_RISK"
    assert "Err_AGENT_NO_RETURN_SIGNAL" in data["errors"]
