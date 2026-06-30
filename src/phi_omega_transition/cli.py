from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import evaluate_transition, transition_from_dict


DEMO_TRANSITION = {
    "transition_id": "clinical_prompt_optimization_001",
    "state_before": "prompt_candidate",
    "proposed_action": "promote_prompt_to_production",
    "state_after": "production_prompt",
    "required": {
        "authority": ["clinical_owner_approval"],
        "boundary": ["production_clinical_agent"],
        "context": ["clinical_eval_dataset"],
        "evidence": ["hallucination_rate", "omission_rate"],
        "policy": ["clinical_safety_policy"],
        "time_window": ["current_eval_window"],
        "recovery": ["rollback_prompt_version"],
        "verifier_depth": "D2",
        "minimum_gain": 0
    },
    "supported": {
        "authority": ["clinical_owner_approval"],
        "boundary": ["production_clinical_agent"],
        "context": ["clinical_eval_dataset"],
        "evidence": ["hallucination_rate"],
        "policy": ["clinical_safety_policy"],
        "time_window": ["current_eval_window"],
        "recovery": ["rollback_prompt_version"],
        "verifier_depth": "D2",
        "estimated_gain": 12000
    }
}


def demo() -> None:
    transition = transition_from_dict(DEMO_TRANSITION)
    result = evaluate_transition(transition)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def check() -> None:
    parser = argparse.ArgumentParser(
        description="PHI-OMEGA Transition Sufficiency Checker"
    )
    parser.add_argument(
        "transition_file",
        help="Path to a JSON transition file."
    )
    args = parser.parse_args()

    path = Path(args.transition_file)
    data = json.loads(path.read_text(encoding="utf-8"))

    transition = transition_from_dict(data)
    result = evaluate_transition(transition)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    check()
