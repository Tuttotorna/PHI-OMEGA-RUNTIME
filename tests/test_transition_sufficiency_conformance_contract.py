import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "data" / "transition_sufficiency_conformance_cases.json"
TOOL_PATH = ROOT / "tools" / "transition_sufficiency_conformance.py"
DOC_PATH = ROOT / "docs" / "TRANSITION_SUFFICIENCY_CONFORMANCE_CONTRACT.md"
SCHEMA_PATH = ROOT / "schemas" / "transition_sufficiency_conformance_result.schema.json"


def load_tool_module():
    spec = importlib.util.spec_from_file_location("transition_sufficiency_conformance", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_conformance_fixture_exists_and_has_unique_cases():
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))

    assert data["fixture_version"] == "tsc-0.1.0"
    assert data["core_invariant"] == "Valid(τ) ⇔ Required(τ) ⊆ Supported(τ)"
    assert "PASS" in data["result_contract"]
    assert "FAIL" in data["result_contract"]
    assert "NON_CONFORMANT" in data["result_contract"]
    assert "UNTESTABLE" in data["result_contract"]

    case_ids = [case["case_id"] for case in data["cases"]]
    assert len(case_ids) >= 10
    assert len(case_ids) == len(set(case_ids))

    required_case_ids = {
        "TSC-001",
        "TSC-002",
        "TSC-003",
        "TSC-004",
        "TSC-005",
        "TSC-006",
        "TSC-007",
        "TSC-008",
        "TSC-009",
        "TSC-010",
    }
    assert required_case_ids.issubset(set(case_ids))


def test_each_case_has_required_operational_fields():
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))

    for case in data["cases"]:
        assert case["case_id"].startswith("TSC-")
        assert case["name"]
        assert case["failure_class"]
        assert case["description"]
        assert isinstance(case["required_support"], list)
        assert case["required_support"]
        assert isinstance(case["stimulus"], dict)
        assert isinstance(case["expected_decisions"], list)
        assert case["expected_decisions"]


def test_result_schema_contains_minimum_contract_fields():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    required = set(schema["required"])
    assert "runtime" in required
    assert "implementation_version" in required
    assert "fixture_version" in required
    assert "case_id" in required
    assert "observed_support" in required
    assert "decision" in required
    assert "expected_decision" in required
    assert "result" in required
    assert "evidence_refs" in required
    assert "terminal_outcome_ref" in required


def test_runner_pass_fail_non_conformant_and_untestable():
    module = load_tool_module()
    cases_doc = module.load_cases(CASES_PATH)

    pass_result = module.evaluate_observation(
        {
            "runtime": "test-runtime",
            "implementation_version": "0",
            "case_id": "TSC-001",
            "observed_support": {
                "observable_state": True,
                "support_basis_present": True,
                "terminal_outcome_present": True,
                "binding_path_present": True,
            },
            "decision": "HARD_BLOCK",
            "evidence_refs": ["test:evidence"],
            "terminal_outcome_ref": "test:terminal",
        },
        cases_doc=cases_doc,
    )
    assert pass_result["result"] == "PASS"

    fail_result = module.evaluate_observation(
        {
            "runtime": "test-runtime",
            "implementation_version": "0",
            "case_id": "TSC-001",
            "observed_support": {
                "observable_state": True,
                "support_basis_present": True,
                "terminal_outcome_present": True,
                "binding_path_present": True,
            },
            "decision": "ALLOW",
            "evidence_refs": ["test:evidence"],
            "terminal_outcome_ref": "test:terminal",
        },
        cases_doc=cases_doc,
    )
    assert fail_result["result"] == "FAIL"

    non_conformant_result = module.evaluate_observation(
        {
            "runtime": "test-runtime",
            "implementation_version": "0",
            "case_id": "TSC-003",
            "observed_support": {
                "observable_state": True,
                "support_basis_missing": True,
            },
            "decision": "ALLOW",
            "evidence_refs": [],
            "terminal_outcome_ref": None,
        },
        cases_doc=cases_doc,
    )
    assert non_conformant_result["result"] == "NON_CONFORMANT"

    untestable_result = module.evaluate_observation(
        {
            "runtime": "test-runtime",
            "implementation_version": "0",
            "case_id": "TSC-010",
            "observed_support": {
                "observable_state": False,
            },
            "decision": "",
            "evidence_refs": [],
            "terminal_outcome_ref": None,
        },
        cases_doc=cases_doc,
    )
    assert untestable_result["result"] == "UNTESTABLE"


def test_documentation_preserves_scope_limits_and_canonical_sentence():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "Transition Sufficiency Conformance Contract" in text
    assert "Valid(τ) ⇔ Required(τ) ⊆ Supported(τ)" in text
    assert "No runtime may claim a transition is valid" in text
    assert "not external adoption" in text
    assert "no external adoption" in text.lower()
    assert "no external endorsement" in text.lower()
