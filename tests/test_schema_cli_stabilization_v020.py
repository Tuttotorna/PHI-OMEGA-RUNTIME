
import json
from pathlib import Path

from phi_omega_transition import __version__
from phi_omega_transition.core import evaluate_transition, transition_from_dict


ROOT = Path(__file__).resolve().parents[1]


def test_v020_package_version_is_aligned():
    assert __version__ == "0.2.0"


def test_v020_transition_case_schema_exists_and_has_required_surface():
    schema_path = ROOT / "schemas" / "transition_case.schema.json"
    assert schema_path.exists()
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    assert schema["title"] == "PHI-OMEGA Transition Sufficiency Case"
    assert "transition_id" in schema["required"]
    assert "proposed_action" in schema["required"]
    assert "required" in schema["required"]
    assert "supported" in schema["required"]


def test_v020_transition_result_schema_exists_and_has_stable_decisions():
    schema_path = ROOT / "schemas" / "transition_result.schema.json"
    assert schema_path.exists()
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    assert schema["title"] == "PHI-OMEGA Transition Sufficiency Result"
    assert "decision" in schema["required"]
    assert schema["properties"]["decision"]["enum"] == [
        "ALLOW",
        "REPAIR",
        "SOFT_BLOCK",
        "HARD_BLOCK",
    ]


def test_v020_transition_result_contains_stable_output_keys():
    case = {
        "transition_id": "v020_stable_surface",
        "state_before": "candidate",
        "proposed_action": "execute_transition",
        "state_after": "executed",
        "required": {
            "authority": ["owner_approval"],
            "boundary": ["runtime_boundary"],
            "verifier_depth": "D1",
            "minimum_gain": 0,
        },
        "supported": {
            "authority": ["owner_approval"],
            "boundary": ["runtime_boundary"],
            "verifier_depth": "D1",
            "estimated_gain": 1,
        },
    }

    out = evaluate_transition(transition_from_dict(case))

    expected_keys = {
        "transition_id",
        "decision",
        "valid",
        "formula",
        "state_before",
        "proposed_action",
        "state_after",
        "missing_requirements",
        "hard_block_reasons",
        "required_subset_supported",
        "verifier_depth_required",
        "verifier_depth_supported",
        "verifier_depth_ok",
        "minimum_gain_required",
        "estimated_gain_supported",
        "gain_ok",
        "reason",
        "next_allowed_transition",
    }

    assert expected_keys.issubset(out.keys())


def test_v020_cli_reference_docs_exist():
    assert (ROOT / "docs" / "CLI_REFERENCE.md").exists()
    assert (ROOT / "docs" / "TRANSITION_SCHEMA.md").exists()
    assert (ROOT / "docs" / "STABLE_INTERFACE_V020.md").exists()
