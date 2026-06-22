import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT))
from run_phi_omega import audit_case, source_repo_status

def read_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def test_minimal_case_produces_valid_operational_standing():
    result = audit_case(read_json("examples/minimal_case.json"))
    assert result["status"] == "RUNTIME_AUDIT_PRODUCED"
    assert result["standing"] == "VALID_OPERATIONAL_STANDING"
    assert result["false_sufficiency_risk"] is True
    assert "distinction_D_m" in result
    assert "necessary_exchange_S" in result
    assert "added_diagnostic_value" in result

def test_external_trace_case_produces_valid_standing():
    result = audit_case(read_json("examples/external_trace_case.json"))
    assert result["status"] == "RUNTIME_AUDIT_PRODUCED"
    assert result["standing"] == "VALID_OPERATIONAL_STANDING"
    assert result["external_evidence"]["present"] is False

def test_external_evidence_case_supported_source():
    result = audit_case(read_json("examples/external_evidence_case.json"))
    assert result["status"] == "RUNTIME_AUDIT_PRODUCED"
    assert result["external_evidence"]["source_repo_status"] == "SUPPORTED_EVIDENCE_PRODUCER"
    assert result["external_evidence"]["false_sufficiency_risk"] is True

def test_source_repo_statuses_preserved_from_parent_v065():
    assert source_repo_status("OMNIABASE") == "SUPPORTED_EVIDENCE_PRODUCER"
    assert source_repo_status("OMNIA-INVARIANCE") == "SUPPORTED_EVIDENCE_PRODUCER"
    assert source_repo_status("OMNIA-FRAGILITY-CHECKER") == "SUPPORTED_EVIDENCE_PRODUCER"
    assert source_repo_status("OMNIA-VALIDATION") == "SUPPORTED_EVIDENCE_PRODUCER"
    assert source_repo_status("OMNIA") == "REFERENCE_ONLY"
    assert source_repo_status("OMNIA-FRAME-FIDELITY") == "PENDING_ADAPTER"
    assert source_repo_status("OMNIABASE-AI-OBSERVATION") == "PENDING_ADAPTER"

def test_cli_minimal_case_json_output():
    result = subprocess.run(
        [sys.executable, "run_phi_omega.py", "examples/minimal_case.json", "--json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["status"] == "RUNTIME_AUDIT_PRODUCED"
    assert data["standing"] == "VALID_OPERATIONAL_STANDING"
