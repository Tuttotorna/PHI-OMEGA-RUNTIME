#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List

VERSION = "v0.1.0"

PARENT_REPO = "https://github.com/Tuttotorna/PHI-OMEGA-OPERATIONAL-FORMULA"
PARENT_RELEASE = "https://github.com/Tuttotorna/PHI-OMEGA-OPERATIONAL-FORMULA/releases/tag/v0.1.65"
PARENT_TAG = "v0.1.65"
PARENT_COMMIT = "910ce08ceffe4686e2e45123986c1fac6d1434a4"

SUPPORTED_EVIDENCE_PRODUCERS = {
    "OMNIABASE",
    "OMNIA-INVARIANCE",
    "OMNIA-FRAGILITY-CHECKER",
    "OMNIA-VALIDATION",
}

REFERENCE_ONLY_REPOS = {
    "OMNIA",
}

PENDING_ADAPTER_REPOS = {
    "OMNIA-FRAME-FIDELITY",
    "OMNIABASE-AI-OBSERVATION",
}

REQUIRED_FIELDS = [
    "object",
    "mode",
    "use",
    "accessible_field",
    "observed_issue",
    "dependency",
    "removal_failure",
    "proposed_realignment",
]

FAKE_USE_PATTERNS = [
    r"\bunderstand\b",
    r"\bsummarize\b",
    r"\bsummary\b",
    r"\bexplain\b",
    r"\bclassify\b",
    r"\bcompare\b",
    r"\bjudge\b",
    r"\bwhat is\b",
    r"\bread\b",
    r"\btheory\b",
    r"\bframework\b",
]

def normalize_source_repo(value: Any) -> str:
    text = str(value or "").strip()
    text = re.sub(r"^https?://github\.com/", "", text, flags=re.IGNORECASE)
    text = text.rstrip("/")
    if "/" in text:
        text = text.split("/")[-1]
    return text.replace("_", "-").replace(" ", "-").upper()

def source_repo_status(source_repo: Any) -> str:
    key = normalize_source_repo(source_repo)
    if key in SUPPORTED_EVIDENCE_PRODUCERS:
        return "SUPPORTED_EVIDENCE_PRODUCER"
    if key in REFERENCE_ONLY_REPOS:
        return "REFERENCE_ONLY"
    if key in PENDING_ADAPTER_REPOS:
        return "PENDING_ADAPTER"
    if not key:
        return "NO_EXTERNAL_SOURCE"
    return "UNAUDITED_SOURCE_REQUIRES_REVIEW"

def as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]

def compact_text(*values: Any) -> str:
    return " ".join(str(v or "") for v in values).strip().lower()

def is_fake_preuse(case: Dict[str, Any]) -> bool:
    text = compact_text(case.get("object"), case.get("use"), case.get("observed_issue"))
    mentions_phi = "phi-omega" in text or "phi omega" in text or "this repo" in text or "repository" in text
    fake_action = any(re.search(pattern, text) for pattern in FAKE_USE_PATTERNS)
    concrete_dependency = bool(str(case.get("dependency") or "").strip())
    concrete_failure = bool(str(case.get("removal_failure") or "").strip())

    if mentions_phi and fake_action:
        return True

    if fake_action and not (concrete_dependency and concrete_failure):
        return True

    return False

def missing_required(case: Dict[str, Any]) -> List[str]:
    missing = []
    for field in REQUIRED_FIELDS:
        value = case.get(field)
        if value is None:
            missing.append(field)
        elif isinstance(value, str) and not value.strip():
            missing.append(field)
    return missing

def external_evidence_audit(case: Dict[str, Any]) -> Dict[str, Any]:
    evidence = case.get("external_evidence")
    if not evidence:
        return {
            "present": False,
            "source_repo_status": "NO_EXTERNAL_SOURCE",
            "errors": [],
            "warnings": [],
            "false_sufficiency_risk": False,
            "summary": "No external evidence packet supplied.",
        }

    source = evidence.get("source_repo")
    status = source_repo_status(source)

    errors = []
    warnings = []

    required = ["source_repo", "field_limit"]
    for field in required:
        value = evidence.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            errors.append("Err_EXTERNAL_EVIDENCE_SCHEMA_INCOMPLETE")

    if status == "PENDING_ADAPTER":
        errors.append("Err_EXTERNAL_REPO_PENDING_ADAPTER")
    elif status == "REFERENCE_ONLY":
        warnings.append("REFERENCE_ONLY_SOURCE_NOT_SIMPLE_SENSOR")
    elif status == "UNAUDITED_SOURCE_REQUIRES_REVIEW":
        warnings.append("Err_UNAUDITED_SOURCE_REQUIRES_REVIEW")

    field_limit = str(evidence.get("field_limit") or "").lower()
    if "all" in field_limit and ("proof" in field_limit or "total" in field_limit):
        errors.append("Err_EXTERNAL_EVIDENCE_TOTALIZATION")

    fragile = as_list(evidence.get("fragile_features"))
    ruptures = as_list(evidence.get("ruptures"))
    false_sufficiency_risk = bool(fragile or ruptures)

    return {
        "present": True,
        "source_repo": source,
        "source_repo_normalized": normalize_source_repo(source),
        "source_repo_status": status,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "false_sufficiency_risk": false_sufficiency_risk,
        "stable_features_count": len(as_list(evidence.get("stable_features"))),
        "fragile_features_count": len(fragile),
        "ruptures_count": len(ruptures),
        "field_limit": evidence.get("field_limit"),
    }

def audit_case(case: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []
    opportunities: List[str] = []

    if not isinstance(case, dict):
        return {
            "runtime_version": VERSION,
            "status": "INVALID_INPUT",
            "standing": "NO_OPERATIONAL_STANDING",
            "errors": ["Err_INPUT_NOT_JSON_OBJECT"],
        }

    missing = missing_required(case)
    if missing:
        errors.append("Err_RUNTIME_SCHEMA_INCOMPLETE")

    if is_fake_preuse(case):
        return {
            "runtime_version": VERSION,
            "status": "NO_OPERATIONAL_STANDING",
            "standing": "NO_OPERATIONAL_STANDING",
            "object": case.get("object"),
            "mode": case.get("mode"),
            "use": case.get("use"),
            "errors": ["Err_PRE_USE_READING_AS_USE", "Err_USE_FIRST_AS_TEXT"],
            "required_next_action": (
                "Provide a concrete object, concrete use, dependency, removal failure, "
                "and realignment that changes the next operational action."
            ),
            "limit": "Reading, summary, comparison, or theory judgment before runtime audit is ordinary discourse, not PHI-OMEGA use.",
            "parent_repo": PARENT_REPO,
        }

    if missing:
        return {
            "runtime_version": VERSION,
            "status": "INVALID_INPUT",
            "standing": "NO_OPERATIONAL_STANDING",
            "missing_fields": missing,
            "errors": sorted(set(errors)),
            "required_fields": REQUIRED_FIELDS,
            "parent_repo": PARENT_REPO,
        }

    external = external_evidence_audit(case)
    errors.extend(external.get("errors", []))
    warnings.extend(external.get("warnings", []))

    obj = str(case.get("object")).strip()
    mode = str(case.get("mode")).strip()
    use = str(case.get("use")).strip()
    field = str(case.get("accessible_field")).strip()
    issue = str(case.get("observed_issue")).strip()
    dependency = str(case.get("dependency")).strip()
    removal_failure = str(case.get("removal_failure")).strip()
    realignment = str(case.get("proposed_realignment")).strip()

    false_sufficiency_risk = True
    if external.get("false_sufficiency_risk"):
        false_sufficiency_risk = True

    if errors:
        status = "REQUIRES_REPAIR"
        standing = "LIMITED_OPERATIONAL_STANDING"
    else:
        status = "RUNTIME_AUDIT_PRODUCED"
        standing = "VALID_OPERATIONAL_STANDING"

    distinction = (
        f"{obj} is treated only in mode '{mode}' for use '{use}', "
        f"not as a total or self-sufficient object."
    )

    necessary_exchange = (
        f"The declared dependency is '{dependency}'. "
        f"If removed, the declared failure is '{removal_failure}'."
    )

    operational_error = (
        "Err_FALSE_SUFFICIENCY_RISK: the object/use may be treated as sufficient "
        "while depending on a field relation that must remain active."
    )

    added_value = (
        "The runtime converted a readable claim into an indexed audit object with "
        "object, mode, use, accessible field, dependency, failure condition, realignment, and limit."
    )

    opportunities.append(
        "Use this output before reading parent theory; only then inspect parent guards if needed."
    )

    return {
        "runtime_version": VERSION,
        "status": status,
        "standing": standing,
        "object": obj,
        "mode": mode,
        "use": use,
        "accessible_field": field,
        "distinction_D_m": distinction,
        "necessary_exchange_S": necessary_exchange,
        "observed_issue": issue,
        "false_sufficiency_risk": false_sufficiency_risk,
        "operational_error": operational_error,
        "realignment": realignment,
        "external_evidence": external,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "opportunities": opportunities,
        "limit": "This runtime output is an operational audit result, not proof of the parent theory and not totality.",
        "added_diagnostic_value": added_value,
        "parent_repo": PARENT_REPO,
        "parent_release": PARENT_RELEASE,
        "parent_tag": PARENT_TAG,
        "parent_commit": PARENT_COMMIT,
    }

def load_json_arg(value: str) -> Dict[str, Any]:
    raw = str(value).strip()
    if raw.startswith("{"):
        return json.loads(raw)

    path = Path(raw)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))

    return json.loads(raw)

def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run PHI-OMEGA runtime audit on one JSON case.")
    parser.add_argument("case", help="Path to JSON case file or raw JSON object string.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    args = parser.parse_args(argv)

    try:
        case = load_json_arg(args.case)
        result = audit_case(case)
    except Exception as exc:
        result = {
            "runtime_version": VERSION,
            "status": "INVALID_INPUT",
            "standing": "NO_OPERATIONAL_STANDING",
            "errors": ["Err_INVALID_JSON_OR_PATH"],
            "detail": str(exc),
        }

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("status") not in {"INVALID_INPUT"} else 2

if __name__ == "__main__":
    raise SystemExit(main())
