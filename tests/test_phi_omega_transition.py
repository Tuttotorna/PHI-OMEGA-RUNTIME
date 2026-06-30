from phi_omega_transition import (
    VerifierDepth,
    Transition,
    TransitionRequirements,
    TransitionSupport,
    evaluate_transition,
    transition_from_dict,
)


def test_allow_when_required_is_subset_of_supported():
    transition = Transition(
        transition_id="allow_001",
        state_before="draft",
        proposed_action="publish",
        state_after="published",
        required=TransitionRequirements(
            authority=["owner"],
            evidence=["review"],
            verifier_depth=VerifierDepth.D1,
            minimum_gain=0,
        ),
        supported=TransitionSupport(
            authority=["owner"],
            evidence=["review"],
            verifier_depth=VerifierDepth.D1,
            estimated_gain=10,
        ),
    )

    result = evaluate_transition(transition)

    assert result["decision"] == "ALLOW"
    assert result["valid"] is True
    assert result["missing_requirements"] == {}


def test_repair_when_required_evidence_is_missing():
    transition = Transition(
        transition_id="repair_001",
        state_before="prompt_candidate",
        proposed_action="promote_prompt_to_production",
        state_after="production_prompt",
        required=TransitionRequirements(
            evidence=["hallucination_rate", "omission_rate"],
            verifier_depth=VerifierDepth.D2,
        ),
        supported=TransitionSupport(
            evidence=["hallucination_rate"],
            verifier_depth=VerifierDepth.D2,
            estimated_gain=100,
        ),
    )

    result = evaluate_transition(transition)

    assert result["decision"] == "REPAIR"
    assert result["valid"] is False
    assert result["missing_requirements"]["evidence"] == ["omission_rate"]


def test_soft_block_when_verifier_depth_is_insufficient():
    transition = Transition(
        transition_id="depth_001",
        state_before="agent_plan",
        proposed_action="execute_payment",
        state_after="payment_executed",
        required=TransitionRequirements(
            authority=["finance_owner"],
            verifier_depth=VerifierDepth.D3,
        ),
        supported=TransitionSupport(
            authority=["finance_owner"],
            verifier_depth=VerifierDepth.D1,
            estimated_gain=1000,
        ),
    )

    result = evaluate_transition(transition)

    assert result["decision"] == "SOFT_BLOCK"
    assert result["valid"] is False
    assert result["verifier_depth_ok"] is False


def test_soft_block_when_gain_is_insufficient():
    transition = Transition(
        transition_id="gain_001",
        state_before="candidate_action",
        proposed_action="run_expensive_job",
        state_after="job_completed",
        required=TransitionRequirements(
            authority=["system_owner"],
            verifier_depth=VerifierDepth.D1,
            minimum_gain=500,
        ),
        supported=TransitionSupport(
            authority=["system_owner"],
            verifier_depth=VerifierDepth.D1,
            estimated_gain=100,
        ),
    )

    result = evaluate_transition(transition)

    assert result["decision"] == "SOFT_BLOCK"
    assert result["valid"] is False
    assert result["gain_ok"] is False


def test_transition_from_dict_parses_verifier_depth():
    data = {
        "transition_id": "parse_001",
        "state_before": "s0",
        "proposed_action": "advance",
        "state_after": "s1",
        "required": {
            "authority": ["owner"],
            "verifier_depth": "D2",
        },
        "supported": {
            "authority": ["owner"],
            "verifier_depth": "D3",
            "estimated_gain": 1,
        },
    }

    transition = transition_from_dict(data)
    result = evaluate_transition(transition)

    assert result["decision"] == "ALLOW"
    assert result["verifier_depth_required"] == "D2"
    assert result["verifier_depth_supported"] == "D3"


def test_numeric_string_verifier_depth_is_supported():
    data = {
        "transition_id": "parse_numeric_depth_001",
        "proposed_action": "advance",
        "required": {"verifier_depth": "1"},
        "supported": {"verifier_depth": "2", "estimated_gain": 1},
    }

    transition = transition_from_dict(data)
    result = evaluate_transition(transition)

    assert result["decision"] == "ALLOW"
    assert result["verifier_depth_required"] == "D1"
    assert result["verifier_depth_supported"] == "D2"
