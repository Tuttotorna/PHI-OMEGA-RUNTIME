"""
PHI-OMEGA-RUNTIME — Transition Gain Layer

This module estimates preventable loss removed before execution.

Validity first.
Convenience second.

A positive net gain must never authorize an invalid transition.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Literal, Dict, Any


DecisionPath = Literal["ALLOW", "REPAIR", "SOFT_BLOCK", "HARD_BLOCK"]


@dataclass(frozen=True)
class TransitionGainInput:
    attempted_transitions: int
    baseline_failure_rate: float
    guarded_failure_rate: float
    average_failure_cost: float
    debug_hours_saved_per_prevented_failure: float = 0.0
    hourly_operational_cost: float = 0.0
    compliance_or_reputation_cost_avoided: float = 0.0
    gate_operational_cost: float = 0.0
    cost_of_delay: float = 0.0
    transition_valid: bool = True
    missing_dependency_repairable: bool = False
    hard_boundary_violation: bool = False


@dataclass(frozen=True)
class TransitionGainResult:
    decision_path: DecisionPath
    prevented_invalid_transitions: float
    preventable_failure_reduction_percent: float
    expected_cost_avoided: float
    expected_time_cost_saved: float
    gross_gain: float
    net_gain: float
    gain_multiple: float | None
    gain_classification: str
    validity_override_blocked: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _clamp_rate(value: float) -> float:
    if value < 0:
        return 0.0
    if value > 1:
        return 1.0
    return float(value)


def classify_gain(net_gain: float) -> str:
    if net_gain > 0:
        return "POSITIVE_PREVENTABLE_LOSS_REMOVAL"
    if net_gain == 0:
        return "NEUTRAL_GAIN"
    return "NEGATIVE_OR_UNPROVEN_GAIN"


def evaluate_transition_gain(data: TransitionGainInput) -> TransitionGainResult:
    attempted = max(0, int(data.attempted_transitions))
    baseline = _clamp_rate(data.baseline_failure_rate)
    guarded = _clamp_rate(data.guarded_failure_rate)

    reduction_rate = max(0.0, baseline - guarded)
    prevented = attempted * reduction_rate

    expected_cost_avoided = prevented * max(0.0, data.average_failure_cost)

    expected_time_cost_saved = (
        prevented
        * max(0.0, data.debug_hours_saved_per_prevented_failure)
        * max(0.0, data.hourly_operational_cost)
    )

    gross_gain = (
        expected_cost_avoided
        + expected_time_cost_saved
        + max(0.0, data.compliance_or_reputation_cost_avoided)
    )

    net_gain = (
        gross_gain
        - max(0.0, data.gate_operational_cost)
        - max(0.0, data.cost_of_delay)
    )

    preventable_failure_reduction_percent = 0.0
    if baseline > 0:
        preventable_failure_reduction_percent = (reduction_rate / baseline) * 100.0

    gain_multiple = None
    total_cost = max(0.0, data.gate_operational_cost) + max(0.0, data.cost_of_delay)
    if total_cost > 0:
        gain_multiple = gross_gain / total_cost

    validity_override_blocked = False

    if data.hard_boundary_violation:
        decision: DecisionPath = "HARD_BLOCK"
    elif not data.transition_valid:
        validity_override_blocked = net_gain > 0
        decision = "REPAIR" if data.missing_dependency_repairable else "SOFT_BLOCK"
    else:
        decision = "ALLOW" if net_gain >= 0 else "REPAIR"

    return TransitionGainResult(
        decision_path=decision,
        prevented_invalid_transitions=prevented,
        preventable_failure_reduction_percent=preventable_failure_reduction_percent,
        expected_cost_avoided=expected_cost_avoided,
        expected_time_cost_saved=expected_time_cost_saved,
        gross_gain=gross_gain,
        net_gain=net_gain,
        gain_multiple=gain_multiple,
        gain_classification=classify_gain(net_gain),
        validity_override_blocked=validity_override_blocked,
    )


def example() -> Dict[str, Any]:
    result = evaluate_transition_gain(
        TransitionGainInput(
            attempted_transitions=10_000,
            baseline_failure_rate=0.005,
            guarded_failure_rate=0.0025,
            average_failure_cost=200,
            transition_valid=True,
        )
    )
    return result.to_dict()


if __name__ == "__main__":
    print(example())
