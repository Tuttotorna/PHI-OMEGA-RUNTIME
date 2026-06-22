import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from run_phi_omega import audit_case


def read_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def minimal_case():
    return read_json("examples/minimal_case.json")


def test_raw_symbol_is_invalid_input_not_case():
    result = audit_case(".")
    assert result["status"] == "INVALID_INPUT"
    assert result["standing"] == "NO_OPERATIONAL_STANDING"
    assert "Err_INPUT_NOT_JSON_OBJECT" in result["errors"]


def test_missing_fields_preserves_invalid_input_contract():
    result = audit_case({"object": "x"})
    assert result["status"] == "INVALID_INPUT"
    assert result["standing"] == "NO_OPERATIONAL_STANDING"
    assert result["input_contract"] == "INSUFFICIENT_INPUT"
    assert "Err_RUNTIME_SCHEMA_INCOMPLETE" in result["errors"]


def test_required_field_non_string_rejected():
    case = minimal_case()
    case["object"] = []
    result = audit_case(case)
    assert result["status"] == "INVALID_INPUT"
    assert result["standing"] == "NO_OPERATIONAL_STANDING"
    assert "Err_REQUIRED_FIELD_NOT_STRING" in result["errors"]
    assert "object" in result["invalid_field_types"]


def test_external_evidence_malformed_requires_repair_not_exception():
    case = minimal_case()
    case["external_evidence"] = ["not", "an", "object"]
    result = audit_case(case)
    assert result["status"] == "REQUIRES_REPAIR"
    assert result["standing"] == "LIMITED_OPERATIONAL_STANDING"
    assert "Err_EXTERNAL_EVIDENCE_NOT_OBJECT" in result["errors"]


def test_accessible_field_everything_requires_repair():
    case = minimal_case()
    case["accessible_field"] = "everything"
    result = audit_case(case)
    assert result["status"] == "REQUIRES_REPAIR"
    assert "Err_ACCESSIBLE_FIELD_TOTALIZED" in result["errors"]


def test_bare_limit_object_requires_context_indexing():
    case = minimal_case()
    case["object"] = "nothing"
    case["mode"] = "validity"
    case["use"] = "prove absolute nothing"
    case["accessible_field"] = "all reality"
    result = audit_case(case)
    assert result["status"] == "REQUIRES_REPAIR"
    assert "Err_DECLARED_OBJECT_NOT_AUDITABLE_AS_DECLARED" in result["errors"]
    assert result["context_indexed_object_guard"]["route"]["guard"] == "NULL_ABSENCE_GUARD"


def test_context_fixed_word_object_can_enter_runtime():
    case = minimal_case()
    case["object"] = "the word 'nothing' as a linguistic concept"
    case["mode"] = "semantic clarification"
    case["use"] = "distinguish the word from an absolute nothing object"
    case["accessible_field"] = "the declared word, sentence context, linguistic convention, and PHI-OMEGA null guard"
    case["observed_issue"] = "The named word could be confused with an absolute object."
    case["dependency"] = "sentence context, semantic convention, explicit distinction between word and referent"
    case["removal_failure"] = "Without context, the word may be mistaken for an audit-ready absolute object."
    case["proposed_realignment"] = "Audit the declared word and concept form, not an absolute nothing object."
    result = audit_case(case)
    assert result["status"] == "RUNTIME_AUDIT_PRODUCED"
    assert result["standing"] == "VALID_OPERATIONAL_STANDING"
    assert "Err_DECLARED_OBJECT_NOT_AUDITABLE_AS_DECLARED" not in result["errors"]


def test_generic_cosmetic_case_requires_repair():
    case = {
        "object": "AI",
        "mode": "better",
        "use": "improve things",
        "accessible_field": "business",
        "observed_issue": "it may fail",
        "dependency": "context",
        "removal_failure": "bad results",
        "proposed_realignment": "use PHI-OMEGA",
    }
    result = audit_case(case)
    assert result["status"] == "REQUIRES_REPAIR"
    assert "Err_OPERATIONAL_SUBSTANCE_INSUFFICIENT" in result["errors"]
    assert "Err_REALIGNMENT_AUTOREFERENTIAL" in result["errors"]


def test_valid_minimal_case_still_passes():
    result = audit_case(minimal_case())
    assert result["status"] == "RUNTIME_AUDIT_PRODUCED"
    assert result["standing"] == "VALID_OPERATIONAL_STANDING"
