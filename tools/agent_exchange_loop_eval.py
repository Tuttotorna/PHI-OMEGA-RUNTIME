#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

LAYER_VERSION = "v0.1.3"
LAYER_NAME = "PHI-OMEGA Agent Exchange-Loop Eval"

REQUIRED_FIELDS = [
    "agent",
    "task_received",
    "action_produced",
    "expected_use",
]

RETURN_FIELDS = [
    "field_feedback",
    "return_signal",
    "observed_outcome",
]

SUCCESS_FIELDS = [
    "success_criteria",
    "validation_method",
]

NEGATIVE_PHRASES = [
    "not acceptable",
    "not usable",
    "not sufficient",
    "real use failed",
    "field failure",
    "field failed",
]

NEGATIVE_WORDS = [
    "failed",
    "failure",
    "rejected",
    "complaint",
    "error",
    "wrong",
    "unsafe",
    "harm",
    "harmed",
    "blocked",
    "mismatch",
]

LOCAL_PASS_TERMS = [
    "passed",
    "pass",
    "looks correct",
    "plausible",
    "accepted locally",
    "local test",
    "unit test",
    "text eval",
]

SAFE_REGRESSION_PATTERNS = [
    "regression test passed",
    "regression tests passed",
    "without api regression",
    "without regression",
    "no regression",
    "no api regression",
    "no public api change",
    "public api unchanged",
]

def is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, list):
        return len(value) == 0 or all(is_empty(v) for v in value)
    if isinstance(value, dict):
        return len(value) == 0 or all(is_empty(v) for v in value.values())
    return False

def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)

def load_case(path: Path) -> Dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return {
            "_invalid_json": True,
            "_json_error": str(e),
        }
    if not isinstance(data, dict):
        return {
            "_invalid_json": True,
            "_json_error": "Top-level input must be a JSON object.",
        }
    return data

def split_sentences(text: str) -> List[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]

def contains_local_pass(text: str) -> bool:
    t = text.lower()
    return any(term in t for term in LOCAL_PASS_TERMS)

def sentence_has_negative_signal(sentence: str) -> bool:
    s = sentence.lower()

    if any(phrase in s for phrase in NEGATIVE_PHRASES):
        return True

    for word in NEGATIVE_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", s):
            return True

    if re.search(r"\bregression\b", s):
        if any(pattern in s for pattern in SAFE_REGRESSION_PATTERNS):
            return False
        if "passed" in s or "pass" in s:
            return False
        return True

    return False

def has_field_incompatibility(text: str) -> bool:
    return any(sentence_has_negative_signal(sentence) for sentence in split_sentences(text))

def field_presence(case: Dict[str, Any], fields: List[str]) -> bool:
    return any(field in case and not is_empty(case.get(field)) for field in fields)

def summarize_receive(case: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "task_received": case.get("task_received"),
        "context": case.get("context"),
        "tools": case.get("tools"),
        "constraints": case.get("constraints"),
        "expected_use": case.get("expected_use"),
    }

def summarize_give(case: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "action_produced": case.get("action_produced"),
        "output": case.get("output"),
        "tool_calls": case.get("tool_calls"),
        "declared_next_state": case.get("declared_next_state"),
    }

def summarize_field_return(case: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "field_feedback": case.get("field_feedback"),
        "return_signal": case.get("return_signal"),
        "observed_outcome": case.get("observed_outcome"),
        "success_criteria": case.get("success_criteria"),
        "validation_method": case.get("validation_method"),
    }

def evaluate_agent_exchange_loop(case: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []
    opportunities: List[str] = []

    if case.get("_invalid_json"):
        return {
            "layer": LAYER_NAME,
            "layer_version": LAYER_VERSION,
            "status": "INVALID_AGENT_EVAL_INPUT",
            "errors": ["Err_AGENT_EVAL_INPUT_NOT_JSON_OBJECT"],
            "warnings": [],
            "opportunities": ["Provide a JSON object describing one concrete agent run."],
            "details": {"json_error": case.get("_json_error")},
        }

    missing_required = [field for field in REQUIRED_FIELDS if field not in case or is_empty(case.get(field))]
    if missing_required:
        errors.append("Err_AGENT_EVAL_SCHEMA_INCOMPLETE")

    for field in REQUIRED_FIELDS:
        if field in case and not is_empty(case.get(field)) and not isinstance(case.get(field), (str, list, dict)):
            errors.append("Err_AGENT_EVAL_FIELD_UNSUPPORTED_TYPE")

    has_return = field_presence(case, RETURN_FIELDS)
    has_success = field_presence(case, SUCCESS_FIELDS)

    if not has_return:
        errors.append("Err_AGENT_NO_RETURN_SIGNAL")
        opportunities.append("Add field feedback, return signal, or observed outcome from the real use environment.")

    if not has_success:
        warnings.append("Warn_AGENT_SUCCESS_CRITERIA_NOT_EXPLICIT")
        opportunities.append("Declare success criteria or validation method for the agent run.")

    combined_action = as_text(case.get("action_produced")) + " " + as_text(case.get("output"))
    combined_feedback = " ".join(as_text(case.get(field)) for field in RETURN_FIELDS + SUCCESS_FIELDS)
    combined_all = combined_action + " " + combined_feedback

    local_pass = contains_local_pass(combined_all)
    field_negative = has_field_incompatibility(combined_feedback)

    if local_pass and field_negative:
        errors.append("Err_AGENT_LOCAL_OUTPUT_FIELD_FAILURE")
        opportunities.append("Do not treat local pass as sufficient. Reconcile local validation with field failure.")

    if field_negative:
        warnings.append("Warn_FIELD_RETURN_SHOWS_INCOMPATIBILITY")

    if "confidence" in case and isinstance(case.get("confidence"), (int, float)):
        if case["confidence"] >= 0.8 and not has_return:
            errors.append("Err_AGENT_HIGH_CONFIDENCE_WITHOUT_FIELD_RETURN")
            opportunities.append("Lower confidence or require field return before declaring operational sufficiency.")

    if "declared_next_state" not in case or is_empty(case.get("declared_next_state")):
        warnings.append("Warn_AGENT_NEXT_STATE_NOT_DECLARED")
        opportunities.append("Declare how the agent should transform after feedback.")

    if missing_required:
        status = "INVALID_AGENT_EVAL_INPUT"
    elif "Err_AGENT_LOCAL_OUTPUT_FIELD_FAILURE" in errors:
        status = "FALSE_SUFFICIENCY_RISK"
    elif "Err_AGENT_HIGH_CONFIDENCE_WITHOUT_FIELD_RETURN" in errors:
        status = "FALSE_SUFFICIENCY_RISK"
    elif "Err_AGENT_NO_RETURN_SIGNAL" in errors:
        status = "AGENT_EXCHANGE_LOOP_INCOMPLETE"
    else:
        status = "AGENT_EXCHANGE_LOOP_VALID"

    risk_score = 0
    risk_score += 40 if "Err_AGENT_NO_RETURN_SIGNAL" in errors else 0
    risk_score += 40 if "Err_AGENT_LOCAL_OUTPUT_FIELD_FAILURE" in errors else 0
    risk_score += 20 if "Err_AGENT_HIGH_CONFIDENCE_WITHOUT_FIELD_RETURN" in errors else 0
    risk_score += 10 if "Warn_AGENT_SUCCESS_CRITERIA_NOT_EXPLICIT" in warnings else 0
    risk_score += 10 if "Warn_AGENT_NEXT_STATE_NOT_DECLARED" in warnings else 0
    risk_score = min(100, risk_score)

    return {
        "layer": LAYER_NAME,
        "layer_version": LAYER_VERSION,
        "status": status,
        "agent": case.get("agent"),
        "receive": summarize_receive(case),
        "give": summarize_give(case),
        "field_return": summarize_field_return(case),
        "exchange_assessment": {
            "has_required_agent_case": not bool(missing_required),
            "has_field_return": has_return,
            "has_success_criteria": has_success,
            "local_pass_detected": local_pass,
            "field_incompatibility_detected": field_negative,
            "false_sufficiency_risk_score": risk_score,
        },
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "opportunities": sorted(set(opportunities)),
    }

def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    if not argv:
        print(json.dumps({
            "layer": LAYER_NAME,
            "layer_version": LAYER_VERSION,
            "status": "ERROR",
            "error": "Provide one JSON file path."
        }, indent=2))
        return 2

    path = Path(argv[0])
    case = load_case(path)
    result = evaluate_agent_exchange_loop(case)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] not in {"INVALID_AGENT_EVAL_INPUT"} else 1

if __name__ == "__main__":
    raise SystemExit(main())
