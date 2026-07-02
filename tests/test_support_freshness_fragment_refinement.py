import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "data" / "transition_sufficiency_conformance_cases.json"
TOOL_PATH = ROOT / "tools" / "transition_sufficiency_conformance.py"
DOC_PATH = ROOT / "docs" / "SUPPORT_FRESHNESS_FRAGMENT_REFINEMENT.md"


def load_tool_module():
    spec = importlib.util.spec_from_file_location("transition_sufficiency_conformance", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_fixture_version_and_refinement_cases_present():
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))

    assert data["fixture_version"] == "tsc-0.2.0"
    assert "support_predicate_refinement" in data
    assert "Fresh(FragmentLevelSupported(τ))" in data["support_predicate_refinement"]["refined_reading"]

    case_ids = {case["case_id"] for case in data["cases"]}

    assert "TSC-011" in case_ids
    assert "TSC-012" in case_ids
    assert "TSC-013" in case_ids
    assert "TSC-014" in case_ids
    assert "TSC-015" in case_ids


def test_stale_evidence_false_pass_is_caught():
    module = load_tool_module()
    cases_doc = module.load_cases(CASES_PATH)

    result = module.evaluate_observation(
        {
            "runtime": "test-runtime",
            "implementation_version": "0",
            "case_id": "TSC-011",
            "observed_support": {
                "observable_state": True,
                "schema_intact": True,
                "support_reference_present": True,
                "evidence_stale": True,
            },
            "decision": "ALLOW",
            "evidence_refs": ["test:policy_ref"],
            "terminal_outcome_ref": "test:terminal",
        },
        cases_doc=cases_doc,
    )

    assert result["result"] == "FAIL"


def test_stale_evidence_revalidation_passes():
    module = load_tool_module()
    cases_doc = module.load_cases(CASES_PATH)

    result = module.evaluate_observation(
        {
            "runtime": "test-runtime",
            "implementation_version": "0",
            "case_id": "TSC-011",
            "observed_support": {
                "observable_state": True,
                "schema_intact": True,
                "support_reference_present": True,
                "evidence_stale": True,
            },
            "decision": "REPAIR_OR_REVALIDATE",
            "evidence_refs": ["test:policy_ref"],
            "terminal_outcome_ref": None,
        },
        cases_doc=cases_doc,
    )

    assert result["result"] == "PASS"


def test_object_level_support_without_valid_fragment_fails_if_allowed():
    module = load_tool_module()
    cases_doc = module.load_cases(CASES_PATH)

    result = module.evaluate_observation(
        {
            "runtime": "test-runtime",
            "implementation_version": "0",
            "case_id": "TSC-012",
            "observed_support": {
                "observable_state": True,
                "support_object_present": True,
                "required_fragment_invalid": True,
            },
            "decision": "ALLOW",
            "evidence_refs": ["test:support_object"],
            "terminal_outcome_ref": "test:terminal",
        },
        cases_doc=cases_doc,
    )

    assert result["result"] == "FAIL"


def test_missing_operational_root_fragment_is_non_conformant():
    module = load_tool_module()
    cases_doc = module.load_cases(CASES_PATH)

    result = module.evaluate_observation(
        {
            "runtime": "test-runtime",
            "implementation_version": "0",
            "case_id": "TSC-013",
            "observed_support": {
                "observable_state": True,
                "support_chain_present": True,
                "operational_root_fragment_missing": True,
            },
            "decision": "ALLOW",
            "evidence_refs": [],
            "terminal_outcome_ref": None,
        },
        cases_doc=cases_doc,
    )

    assert result["result"] == "NON_CONFORMANT"


def test_refinement_doc_preserves_anti_infinite_regress_rule():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "Valid(τ) ⇔ Required(τ) ⊆ Fresh(FragmentLevelSupported(τ))" in text
    assert "operational root fragment" in text
    assert "This is not an infinite regress" in text
    assert "Past-error-to-future-constraint conversion" in text
    assert "object-level support is not the same as fragment-level transition support" in text
