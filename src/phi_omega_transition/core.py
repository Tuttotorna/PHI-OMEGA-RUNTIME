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
    D0 = 0  # attested only
    D1 = 1  # local / proprietary verifier
    D2 = 2  # controlled reproducibility
    D3 = 3  # public reproducibility


@dataclass(frozen=True)
class TransitionRequirements:
    authority: list[str] = field(default_factory=list)
    boundary: list[str] = field(default_factory=list)
    context: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    policy: list[str] = field(default_factory=list)
    time_window: list[str] = field(default_factory=list)
    recovery: list[str] = field(default_factory=list)
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
            verifier_depth=_depth_from_value(supported.get("verifier_depth", "D0")),
            estimated_gain=float(supported.get("estimated_gain", 0.0)),
        ),
    )


def evaluate_transition(t: Transition) -> dict[str, Any]:
    """
    PHI-OMEGA Transition Sufficiency Framework.

    Core formula:

        Valid(τ) ⇔ Required(τ) ⊆ Supported(τ)

    A transition may proceed only when the authority, boundary, context,
    evidence, policy, time window, verifier depth, recovery path and gain
    required by the transition are supported at execution time.

    Gain can justify checking a transition.
    Gain cannot authorize an invalid transition.
    """

    missing = {
        "authority": _missing(t.required.authority, t.supported.authority),
        "boundary": _missing(t.required.boundary, t.supported.boundary),
        "context": _missing(t.required.context, t.supported.context),
        "evidence": _missing(t.required.evidence, t.supported.evidence),
        "policy": _missing(t.required.policy, t.supported.policy),
        "time_window": _missing(t.required.time_window, t.supported.time_window),
        "recovery": _missing(t.required.recovery, t.supported.recovery),
    }

    missing_requirements = {
        key: value for key, value in missing.items() if value
    }

    required_subset_supported = not missing_requirements
    verifier_ok = t.supported.verifier_depth >= t.required.verifier_depth
    gain_ok = t.supported.estimated_gain >= t.required.minimum_gain

    valid = required_subset_supported and verifier_ok and gain_ok

    if valid:
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
