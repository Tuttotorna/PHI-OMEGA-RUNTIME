import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from run_phi_omega import audit_case


def read_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def minimal_case():
    return read_json("examples/minimal_case.json")


BARE_LIMIT_OBJECTS = [
    "nothing",
    "absolute nothing",
    "time",
    "time itself",
    "identity",
    "absolute identity",
    "outside Ω",
    "outside omega",
    "infinity",
    "origin of totality",
    "everything",
    "totality",
]


@pytest.mark.parametrize("obj", BARE_LIMIT_OBJECTS)
def test_bare_limit_object_requires_repair_even_with_weak_context_elsewhere(obj):
    case = minimal_case()
    case["object"] = obj
    case["mode"] = "validity"
    case["use"] = "audit it itself"
    case["accessible_field"] = "project field, operational dependencies, locally observed trace"
    case["observed_issue"] = "The object appears locally understandable but is not fixed as an operational object."
    case["dependency"] = "declared context, operational field, trace"
    case["removal_failure"] = "Without context, the object loses operational meaning."
    case["proposed_realignment"] = "Declare the object as word, concept, deadline, record, version, symbol, local fragment, or bounded field."
    result = audit_case(case)
    assert result["status"] == "REQUIRES_REPAIR"
    assert "Err_DECLARED_OBJECT_NOT_AUDITABLE_AS_DECLARED" in result["errors"]
    assert "Err_WEAK_CONTEXT_AS_CONTEXT_FIX" in result["errors"]


def test_plain_time_with_project_context_still_requires_object_repair():
    case = minimal_case()
    case["object"] = "time"
    case["mode"] = "project governance"
    case["use"] = "check whether the decision remains valid after the deadline"
    case["accessible_field"] = "timeline, approval email, delivery date, dependency list"
    case["observed_issue"] = "The deadline may change the validity of the decision."
    case["dependency"] = "deadline, approval timestamp, delivery date, decision owner"
    case["removal_failure"] = "Without the deadline trace, the decision cannot be evaluated across time."
    case["proposed_realignment"] = "Audit the project approval deadline, not time as a bare object."
    result = audit_case(case)
    assert result["status"] == "REQUIRES_REPAIR"
    assert "Err_DECLARED_OBJECT_NOT_AUDITABLE_AS_DECLARED" in result["errors"]


@pytest.mark.parametrize(
    "obj",
    [
        "the word 'nothing' as a linguistic concept",
        "the term 'time' as a semantic concept",
        "project approval deadline",
        "identity record version",
        "formal infinity symbol",
        "local fragment origin",
        "bounded accessible field",
    ],
)
def test_context_fixed_limit_related_objects_can_pass(obj):
    case = minimal_case()
    case["object"] = obj
    case["mode"] = "semantic or operational clarification"
    case["use"] = "distinguish the declared object from an unfixed absolute object before audit"
    case["accessible_field"] = "declared object, sentence context, operational trace, relevant convention, and field limit"
    case["observed_issue"] = "A named object could be confused with an absolute audit-ready object."
    case["dependency"] = "declared context, trace, convention, field limit, and distinction between name and operational object"
    case["removal_failure"] = "Without context and trace, the object may be mistaken for an unfixed absolute object."
    case["proposed_realignment"] = "Audit the explicitly context-fixed object inside the stated field and use."
    result = audit_case(case)
    assert result["status"] == "RUNTIME_AUDIT_PRODUCED"
    assert result["standing"] == "VALID_OPERATIONAL_STANDING"
    assert "Err_DECLARED_OBJECT_NOT_AUDITABLE_AS_DECLARED" not in result["errors"]
    assert "Err_WEAK_CONTEXT_AS_CONTEXT_FIX" not in result["errors"]


def test_previous_valid_minimal_case_still_passes():
    result = audit_case(minimal_case())
    assert result["status"] == "RUNTIME_AUDIT_PRODUCED"
    assert result["standing"] == "VALID_OPERATIONAL_STANDING"


def test_malformed_external_evidence_still_requires_repair_not_exception():
    case = minimal_case()
    case["external_evidence"] = "bad evidence"
    result = audit_case(case)
    assert result["status"] == "REQUIRES_REPAIR"
    assert "Err_EXTERNAL_EVIDENCE_NOT_OBJECT" in result["errors"]


def test_raw_symbol_still_invalid_input():
    result = audit_case(".")
    assert result["status"] == "INVALID_INPUT"
    assert "Err_INPUT_NOT_JSON_OBJECT" in result["errors"]
