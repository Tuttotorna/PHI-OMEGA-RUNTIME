
from phi_omega_transition.core import evaluate_transition, transition_from_dict


def result(data):
    return evaluate_transition(transition_from_dict(data))


def base_transition():
    return {
        "transition_id": "v019_base",
        "state_before": "candidate",
        "proposed_action": "promote_transition",
        "state_after": "runtime_state",
        "required": {
            "authority": ["owner_approval"],
            "boundary": ["runtime_boundary"],
            "context": ["current_eval_context"],
            "evidence": ["field_return"],
            "policy": ["runtime_policy"],
            "time_window": ["current_window"],
            "recovery": ["rollback_path"],
            "verifier_depth": "D1",
            "minimum_gain": 0,
        },
        "supported": {
            "authority": ["owner_approval"],
            "boundary": ["runtime_boundary"],
            "context": ["current_eval_context"],
            "evidence": ["field_return"],
            "policy": ["runtime_policy"],
            "time_window": ["current_window"],
            "recovery": ["rollback_path"],
            "verifier_depth": "D1",
            "estimated_gain": 1,
        },
    }


def test_v019_allows_when_required_subset_supported():
    out = result(base_transition())
    assert out["decision"] == "ALLOW"
    assert out["valid"] is True
    assert out["next_allowed_transition"] == "execute"


def test_v019_soft_missing_support_is_repair_not_hard_block():
    data = base_transition()
    data["required"]["evidence"].append("omission_rate")
    out = result(data)
    assert out["decision"] == "REPAIR"
    assert out["valid"] is False
    assert out["missing_requirements"]["evidence"] == ["omission_rate"]


def test_v019_verifier_depth_failure_is_soft_block():
    data = base_transition()
    data["required"]["verifier_depth"] = "D3"
    data["supported"]["verifier_depth"] = "D1"
    out = result(data)
    assert out["decision"] == "SOFT_BLOCK"
    assert out["verifier_depth_ok"] is False


def test_v019_gain_failure_is_soft_block():
    data = base_transition()
    data["required"]["minimum_gain"] = 100
    data["supported"]["estimated_gain"] = 10
    out = result(data)
    assert out["decision"] == "SOFT_BLOCK"
    assert out["gain_ok"] is False


def test_v019_hard_boundary_missing_is_hard_block():
    data = base_transition()
    data["required"]["hard_boundary"] = ["non_repairable_regulatory_boundary"]
    out = result(data)
    assert out["decision"] == "HARD_BLOCK"
    assert out["valid"] is False
    assert out["hard_block_reasons"] == {
        "hard_boundary": ["non_repairable_regulatory_boundary"]
    }


def test_v019_hard_boundary_supported_can_allow():
    data = base_transition()
    data["required"]["hard_boundary"] = ["non_repairable_regulatory_boundary"]
    data["supported"]["hard_boundary"] = ["non_repairable_regulatory_boundary"]
    out = result(data)
    assert out["decision"] == "ALLOW"
    assert out["valid"] is True
