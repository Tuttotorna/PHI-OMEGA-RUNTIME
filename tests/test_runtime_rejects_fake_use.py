import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT))
from run_phi_omega import audit_case

def read_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def test_fake_preuse_case_rejected():
    result = audit_case(read_json("examples/fake_preuse_case.json"))
    assert result["status"] == "NO_OPERATIONAL_STANDING"
    assert result["standing"] == "NO_OPERATIONAL_STANDING"
    assert "Err_PRE_USE_READING_AS_USE" in result["errors"]
    assert "Err_USE_FIRST_AS_TEXT" in result["errors"]

def test_missing_required_fields_invalid():
    result = audit_case({"object": "x"})
    assert result["status"] == "INVALID_INPUT"
    assert result["standing"] == "NO_OPERATIONAL_STANDING"
    assert "Err_RUNTIME_SCHEMA_INCOMPLETE" in result["errors"]

def test_pending_adapter_external_evidence_requires_repair():
    case = read_json("examples/external_evidence_case.json")
    case["external_evidence"]["source_repo"] = "OMNIABASE-AI-OBSERVATION"
    result = audit_case(case)
    assert result["status"] == "REQUIRES_REPAIR"
    assert result["standing"] == "LIMITED_OPERATIONAL_STANDING"
    assert "Err_EXTERNAL_REPO_PENDING_ADAPTER" in result["errors"]

def test_cli_fake_preuse_returns_operational_rejection():
    result = subprocess.run(
        [sys.executable, "run_phi_omega.py", "examples/fake_preuse_case.json", "--json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["status"] == "NO_OPERATIONAL_STANDING"
    assert data["standing"] == "NO_OPERATIONAL_STANDING"
