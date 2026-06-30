import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "transition_gain_layer.py"

spec = importlib.util.spec_from_file_location("transition_gain_layer", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

TransitionGainInput = module.TransitionGainInput
evaluate_transition_gain = module.evaluate_transition_gain


def test_transition_gain_basic_avoided_loss():
    result = evaluate_transition_gain(
        TransitionGainInput(
            attempted_transitions=10_000,
            baseline_failure_rate=0.005,
            guarded_failure_rate=0.0025,
            average_failure_cost=200,
        )
    )

    assert result.prevented_invalid_transitions == 25
    assert result.expected_cost_avoided == 5000
    assert result.net_gain == 5000
    assert result.decision_path == "ALLOW"
    assert result.gain_classification == "POSITIVE_PREVENTABLE_LOSS_REMOVAL"


def test_failure_reduction_percent():
    result = evaluate_transition_gain(
        TransitionGainInput(
            attempted_transitions=1000,
            baseline_failure_rate=0.10,
            guarded_failure_rate=0.04,
            average_failure_cost=100,
        )
    )

    assert round(result.preventable_failure_reduction_percent, 2) == 60.00


def test_time_cost_saved_is_counted():
    result = evaluate_transition_gain(
        TransitionGainInput(
            attempted_transitions=100,
            baseline_failure_rate=0.20,
            guarded_failure_rate=0.10,
            average_failure_cost=50,
            debug_hours_saved_per_prevented_failure=2,
            hourly_operational_cost=100,
        )
    )

    assert result.prevented_invalid_transitions == 10
    assert result.expected_cost_avoided == 500
    assert result.expected_time_cost_saved == 2000
    assert result.gross_gain == 2500


def test_gate_cost_and_cost_of_delay_reduce_net_gain():
    result = evaluate_transition_gain(
        TransitionGainInput(
            attempted_transitions=100,
            baseline_failure_rate=0.20,
            guarded_failure_rate=0.10,
            average_failure_cost=50,
            gate_operational_cost=300,
            cost_of_delay=300,
        )
    )

    assert result.expected_cost_avoided == 500
    assert result.net_gain == -100
    assert result.decision_path == "REPAIR"
    assert result.gain_classification == "NEGATIVE_OR_UNPROVEN_GAIN"


def test_profit_never_overrides_invalid_transition():
    result = evaluate_transition_gain(
        TransitionGainInput(
            attempted_transitions=10_000,
            baseline_failure_rate=0.10,
            guarded_failure_rate=0.01,
            average_failure_cost=1000,
            transition_valid=False,
            missing_dependency_repairable=True,
        )
    )

    assert result.net_gain > 0
    assert result.decision_path == "REPAIR"
    assert result.validity_override_blocked is True


def test_hard_boundary_violation_never_allows():
    result = evaluate_transition_gain(
        TransitionGainInput(
            attempted_transitions=10_000,
            baseline_failure_rate=0.10,
            guarded_failure_rate=0.01,
            average_failure_cost=1000,
            transition_valid=True,
            hard_boundary_violation=True,
        )
    )

    assert result.net_gain > 0
    assert result.decision_path == "HARD_BLOCK"


def test_rates_are_clamped():
    result = evaluate_transition_gain(
        TransitionGainInput(
            attempted_transitions=100,
            baseline_failure_rate=2.0,
            guarded_failure_rate=-1.0,
            average_failure_cost=10,
        )
    )

    assert result.prevented_invalid_transitions == 100
    assert result.expected_cost_avoided == 1000
