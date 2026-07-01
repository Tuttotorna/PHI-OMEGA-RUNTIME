from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Iterable, Union


class Decision(str, Enum):
    ALLOW = "ALLOW"
    REPAIR = "REPAIR"
    SOFT_BLOCK = "SOFT_BLOCK"
    HARD_BLOCK = "HARD_BLOCK"


class VerifierDepth(IntEnum):
    D0 = 0
    D1 = 1
    D2 = 2
    D3 = 3


SOFT_SUPPORT_FIELDS = (
    "authority",
    "boundary",
    "context",
    "evidence",
    "policy",
    "time_window",
    "recovery",
)

HARD_SUPPORT_FIELDS = (
    "hard_authority",
    "hard_boundary",
    "hard_policy",
)


@dataclass(frozen=True)
class TransitionRequirements:
    authority: list[str] = field(default_factory=list)
    boundary: list[str] = field(default_factory=list)
    context: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    policy: list[str] = field(default_factory=list)
    time_window: list[str] = field(default_factory=list)
    recovery: list[str] = field(default_factory=list)

    hard_authority: list[str] = field(default_factory=list)
    hard_boundary: list[str] = field(default_factory=list)
    hard_policy: list[str] = field(default_factory=list)

    verifier_depth: VerifierDepth = VerifierDepth.D0
    minimum_gain: float = 0.0


@dataclass(frozen=True)
class TransitionSupport:
    authority: list[str] = field(default_factory=list)
    boundary: list[str] = field(default_factory=list)
    context: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    policy: list[str] = field(default_factory=list)
    time_window: list[str] = field(default_factory=list)
    recovery: list[str] = field(default_factory=list)

    hard_authority: list[str] = field(default_factory=list)
    hard_boundary: list[str] = field(default_factory=list)
    hard_policy: list[str] = field(default_factory=list)

    verifier_depth: VerifierDepth = VerifierDepth.D0
    estimated_gain: float = 0.0


@dataclass(frozen=True)
class Transition:
    transition_id: str
    state_before: str
    proposed_action: str
    state_after: str
    required: TransitionRequirements
    supported: TransitionSupport


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, tuple):
        return [str(item) for item in value]
    if isinstance(value, set):
        return [str(item) for item in value]
    return [str(value)]


def _missing(required_items: Iterable[str], supported_items: Iterable[str]) -> list[str]:
    return sorted(set(required_items) - set(supported_items))


def _depth_from_value(value: Union[str, int, VerifierDepth]) -> VerifierDepth:
    if isinstance(value, VerifierDepth):
        return value
    if isinstance(value, int):
        return VerifierDepth(value)
    if isinstance(value, str):
        normalized = value.strip().upper()
        if normalized.isdigit():
            return VerifierDepth(int(normalized))
        return VerifierDepth[normalized]
    raise ValueError(f"Unsupported verifier depth: {value!r}")


def transition_from_dict(data: dict[str, Any]) -> Transition:
    required = data.get("required", {})
    supported = data.get("supported", {})

    return Transition(
        transition_id=str(data["transition_id"]),
        state_before=str(data.get("state_before", "")),
        proposed_action=str(data["proposed_action"]),
        state_after=str(data.get("state_after", "")),
        required=TransitionRequirements(
            authority=_as_list(required.get("authority", [])),
            boundary=_as_list(required.get("boundary", [])),
            context=_as_list(required.get("context", [])),
            evidence=_as_list(required.get("evidence", [])),
            policy=_as_list(required.get("policy", [])),
            time_window=_as_list(required.get("time_window", [])),
            recovery=_as_list(required.get("recovery", [])),
            hard_authority=_as_list(required.get("hard_authority", [])),
            hard_boundary=_as_list(required.get("hard_boundary", [])),
            hard_policy=_as_list(required.get("hard_policy", [])),
            verifier_depth=_depth_from_value(required.get("verifier_depth", "D0")),
            minimum_gain=float(required.get("minimum_gain", 0.0)),
        ),
        supported=TransitionSupport(
            authority=_as_list(supported.get("authority", [])),
            boundary=_as_list(supported.get("boundary", [])),
            context=_as_list(supported.get("context", [])),
            evidence=_as_list(supported.get("evidence", [])),
            policy=_as_list(supported.get("policy", [])),
            time_window=_as_list(supported.get("time_window", [])),
            recovery=_as_list(supported.get("recovery", [])),
            hard_authority=_as_list(supported.get("hard_authority", [])),
            hard_boundary=_as_list(supported.get("hard_boundary", [])),
            hard_policy=_as_list(supported.get("hard_policy", [])),
            verifier_depth=_depth_from_value(supported.get("verifier_depth", "D0")),
            estimated_gain=float(supported.get("estimated_gain", 0.0)),
        ),
    )


def _missing_by_field(t: Transition, fields: tuple[str, ...]) -> dict[str, list[str]]:
    missing: dict[str, list[str]] = {}
    for field_name in fields:
        required_items = getattr(t.required, field_name)
        supported_items = getattr(t.supported, field_name)
        gap = _missing(required_items, supported_items)
        if gap:
            missing[field_name] = gap
    return missing


def evaluate_transition(t: Transition) -> dict[str, Any]:
    soft_missing = _missing_by_field(t, SOFT_SUPPORT_FIELDS)
    hard_missing = _missing_by_field(t, HARD_SUPPORT_FIELDS)

    missing_requirements = {**soft_missing, **hard_missing}

    required_subset_supported = not missing_requirements
    verifier_ok = t.supported.verifier_depth >= t.required.verifier_depth
    gain_ok = t.supported.estimated_gain >= t.required.minimum_gain
    hard_block_required = bool(hard_missing)

    valid = (
        required_subset_supported
        and verifier_ok
        and gain_ok
        and not hard_block_required
    )

    if hard_block_required:
        decision = Decision.HARD_BLOCK
        reason = (
            "Required(τ) contains non-repairable hard support that is not present "
            "in Supported(τ). Execution must be blocked."
        )
    elif valid:
        decision = Decision.ALLOW
        reason = (
            "Required(τ) is contained in Supported(τ). "
            "Transition sufficiency satisfied."
        )
    elif not required_subset_supported:
        decision = Decision.REPAIR
        reason = (
            "Required(τ) is not contained in Supported(τ). "
            "Missing support must be repaired before execution."
        )
    elif not verifier_ok:
        decision = Decision.SOFT_BLOCK
        reason = "Verifier depth is insufficient for the proposed next transition."
    elif not gain_ok:
        decision = Decision.SOFT_BLOCK
        reason = "Estimated gain does not justify the transition cost."
    else:
        decision = Decision.HARD_BLOCK
        reason = "Transition failed sufficiency conditions."

    return {
        "transition_id": t.transition_id,
        "decision": decision.value,
        "valid": valid,
        "formula": "Valid(τ) ⇔ Required(τ) ⊆ Supported(τ)",
        "state_before": t.state_before,
        "proposed_action": t.proposed_action,
        "state_after": t.state_after,
        "missing_requirements": missing_requirements,
        "hard_block_reasons": hard_missing,
        "required_subset_supported": required_subset_supported,
        "verifier_depth_required": t.required.verifier_depth.name,
        "verifier_depth_supported": t.supported.verifier_depth.name,
        "verifier_depth_ok": verifier_ok,
        "minimum_gain_required": t.required.minimum_gain,
        "estimated_gain_supported": t.supported.estimated_gain,
        "gain_ok": gain_ok,
        "reason": reason,
        "next_allowed_transition": (
            "execute" if valid else "repair_or_recompute_before_execution"
        ),
    }
