from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "SCENARIO_CUSTOM_EVAL_NOTE.md"
AGENT_DOC = ROOT / "AGENT_EXCHANGE_LOOP_EVAL.md"
TOOL = ROOT / "tools" / "agent_exchange_loop_eval.py"

def read(path):
    return path.read_text(encoding="utf-8")

def test_scenario_adapter_note_exists_and_is_subordinate():
    assert NOTE.exists()
    text = read(NOTE)
    assert "PHI-OMEGA-RUNTIME:SCENARIO_CUSTOM_EVAL_ADAPTER_NOTE:v0.1.4" in text
    assert "This is an adapter note only." in text
    assert "It does not redefine PHI-OMEGA." in text
    assert "It does not supersede Agent Exchange-Loop Eval." in text
    assert "It does not make Scenario, LangWatch, or any external framework the center." in text
    assert "The adapter is subordinate, local, reversible, and non-foundational." in text

def test_scenario_adapter_preserves_old_key_path():
    text = read(NOTE)
    assert "PHI-OMEGA mother formula" in text
    assert "PHI-OMEGA-RUNTIME" in text
    assert "Agent Exchange-Loop Eval" in text
    assert "Scenario-compatible adapter note" in text
    assert "mother formula → runtime → Agent Exchange-Loop Eval" in text

def test_scenario_adapter_targets_exact_failure_class():
    text = read(NOTE)
    assert "local pass / real-use fail" in text
    assert "field return" in text
    assert "false sufficiency risk" in text
    assert "next-state repair" in text
    assert "FALSE_SUFFICIENCY_RISK" in text

def test_scenario_adapter_declares_non_dependency_without_capture_phrase():
    text = read(NOTE)
    assert "Scenario is one possible use environment." in text
    assert "It does not require Scenario for PHI-OMEGA Runtime." in text
    assert "It does not make any external framework required by PHI-OMEGA." in text
    assert "Err_SCENARIO_DEPENDENCY_FALSE" in text

def test_scenario_adapter_links_existing_agent_layer_without_superseding_it():
    text = read(NOTE)
    agent_text = read(AGENT_DOC)
    assert "`AGENT_EXCHANGE_LOOP_EVAL.md`" in text
    assert "`tools/agent_exchange_loop_eval.py`" in text
    assert "PHI-OMEGA Agent Exchange-Loop Eval checks whether an AI agent has a real give/receive loop" in agent_text
    assert "PHI-OMEGA Agent Exchange-Loop Eval checks whether an AI agent has a real give/receive loop" in text
    assert "It does not supersede Agent Exchange-Loop Eval." in text

def test_adapter_does_not_contain_center_capture_language():
    text = read(NOTE).lower()
    forbidden = [
        "scenario is the center",
        "scenario becomes the center",
        "phi-omega depends on scenario",
        "replace agent exchange-loop eval",
        "redefine phi-omega through scenario",
    ]
    for phrase in forbidden:
        assert phrase not in text
