#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

VERSION = "v0.1.1"

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

GENERIC_VALUES = {
    "thing",
    "something",
    "stuff",
    "object",
    "system",
    "ai",
    "decision",
    "better",
    "validity",
    "governance",
    "context",
    "business",
    "everything",
    "all",
    "none",
}

GENERIC_PHRASES = {
    "improve things",
    "make better",
    "better result",
    "better results",
    "good decision",
    "check context",
    "use context",
    "use phi-omega",
    "apply phi-omega",
    "apply the formula",
    "use the formula",
    "check dependencies",
    "do better analysis",
    "analyze better",
}

TOTALIZING_PATTERNS = [
    r"\beverything\b",
    r"\ball reality\b",
    r"\bcomplete reality\b",
    r"\btotal reality\b",
    r"\bwhole reality\b",
    r"\bprove all\b",
    r"\btotal proof\b",
    r"\buniversal proof\b",
    r"\bfinal proof\b",
    r"\babsolute proof\b",
    r"\bwithout limit\b",
]

CONTEXT_FIXING_TERMS = [
    "word",
    "term",
    "concept",
    "linguistic",
    "semantic",
    "punctuation",
    "symbol",
    "local",
    "bounded",
    "accessible",
    "field",
    "project",
    "deadline",
    "timeline",
    "clock",
    "trace",
    "record",
    "version",
    "re-identification",
    "identity_",
    "fragment",
    "operational",
    "case",
]

LIMIT_OBJECT_ROUTES: List[Tuple[str, str, str]] = [
    ("nothing", "NULL_ABSENCE_GUARD", "Concept(nulla) / declared absence form"),
    ("nulla", "NULL_ABSENCE_GUARD", "Concept(nulla) / declared absence form"),
    ("absolute nothing", "NULL_ABSENCE_GUARD", "Concept(nulla), not Nulla_abs"),
    ("outside omega", "OMEGA_OUTSIDE_DISTINCTION_GUARD", "Concept(Outside(Ω)) / boundary-need form"),
    ("outside Ω", "OMEGA_OUTSIDE_DISTINCTION_GUARD", "Concept(Outside(Ω)) / boundary-need form"),
    ("outside totality", "OMEGA_OUTSIDE_DISTINCTION_GUARD", "Concept(Outside(Ω)) / boundary-need form"),
    ("omega", "OMEGA_DOMAIN_GUARD", "NOT_APPLICABLE for Ω as ordinary x"),
    ("Ω", "OMEGA_DOMAIN_GUARD", "NOT_APPLICABLE for Ω as ordinary x"),
    ("totality", "OMEGA_DOMAIN_GUARD", "audit a bounded fragment inside Ω_A"),
    ("everything", "ACCESSIBLE_OMEGA_BOUNDARY", "bounded Ω_A field declaration"),
    ("infinity", "OMEGA_INFINITE_PARAMETER_GUARD", "Concept(∞) / local-formal infinity / Ω parameter"),
    ("infinite", "OMEGA_INFINITE_PARAMETER_GUARD", "Concept(∞) / local-formal infinity / Ω parameter"),
    ("time", "TIME_FIELD_GUARD", "T_Φ^A / local temporal field"),
    ("time itself", "TIME_FIELD_GUARD", "T_Φ^A / local temporal field"),
    ("identity", "IDENTITY_REIFICATION_GUARD", "Identity_{A,m,U} / operational re-identification"),
    ("absolute identity", "IDENTITY_REIFICATION_GUARD", "Identity_{A,m,U} / operational re-identification"),
    ("origin of omega", "OMEGA_NO_ORIGIN_GUARD", "local fragment-origin, not origin of Ω"),
    ("origin of Ω", "OMEGA_NO_ORIGIN_GUARD", "local fragment-origin, not origin of Ω"),
    ("origin of totality", "OMEGA_NO_ORIGIN_GUARD", "local fragment-origin, not origin of Ω"),
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


def normalize_text(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = text.replace("ω", "omega")
    text = re.sub(r"[^a-z0-9_\-\s]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def contains_any_pattern(text: str, patterns: List[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def has_context_fix(text: str) -> bool:
    normalized = normalize_text(text)
    return any(term.lower() in normalized for term in CONTEXT_FIXING_TERMS)


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


def invalid_required_types(case: Dict[str, Any]) -> List[str]:
    invalid = []
    for field in REQUIRED_FIELDS:
        if field in case and case.get(field) is not None and not isinstance(case.get(field), str):
            invalid.append(field)
    return invalid


def field_is_operationally_empty(value: Any) -> bool:
    if not isinstance(value, str):
        return True
    text = normalize_text(value)
    if not text:
        return True
    if text in GENERIC_VALUES or text in GENERIC_PHRASES:
        return True
    tokens = [t for t in text.split() if t]
    if len(tokens) == 1 and tokens[0] in GENERIC_VALUES:
        return True
    return False


def operational_substance_audit(case: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []
    weak_fields: List[str] = []

    for field in ["object", "mode", "use", "accessible_field", "dependency", "removal_failure", "proposed_realignment"]:
        if field_is_operationally_empty(case.get(field)):
            weak_fields.append(field)

    realignment = normalize_text(case.get("proposed_realignment"))
    if realignment in GENERIC_PHRASES or realignment.startswith("use phi omega") or realignment.startswith("apply phi omega"):
        errors.append("Err_REALIGNMENT_AUTOREFERENTIAL")

    dependency = case.get("dependency")
    if isinstance(dependency, str) and normalize_text(dependency) in {"context", "dependencies", "field", "everything"}:
        errors.append("Err_DEPENDENCY_OPERATIONALLY_EMPTY")

    field = normalize_text(case.get("accessible_field"))
    if contains_any_pattern(field, TOTALIZING_PATTERNS):
        errors.append("Err_ACCESSIBLE_FIELD_TOTALIZED")

    if weak_fields:
        errors.append("Err_OPERATIONAL_SUBSTANCE_INSUFFICIENT")

    return {
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "weak_fields": weak_fields,
    }


def context_indexed_object_audit(case: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []
    route = None

    obj_raw = str(case.get("object") or "").strip()
    obj = normalize_text(obj_raw)
    mode_use_field = compact_text(case.get("mode"), case.get("use"), case.get("accessible_field"), case.get("observed_issue"))
    full_context = compact_text(case.get("object"), case.get("mode"), case.get("use"), case.get("accessible_field"), case.get("observed_issue"))

    if not obj:
        return {"errors": ["Err_DECLARED_OBJECT_EMPTY"], "warnings": [], "route": None}

    if len(obj) <= 2 and not has_context_fix(mode_use_field):
        errors.append("Err_DECLARED_OBJECT_REQUIRES_CONTEXT")
        route = {
            "declared_object": obj_raw,
            "guard": "CONTEXT_INDEXED_OBJECT_GUARD",
            "route_to": "declared symbol/trace inside a specified mode, use, and accessible field",
            "reason": "A bare sign or very short token is not audit-ready outside context.",
        }

    for term, guard, route_to in LIMIT_OBJECT_ROUTES:
        term_norm = normalize_text(term)
        if obj == term_norm or obj.startswith(term_norm + " ") or (" " + term_norm + " ") in (" " + obj + " "):
            if not has_context_fix(full_context):
                errors.append("Err_DECLARED_OBJECT_NOT_AUDITABLE_AS_DECLARED")
                route = {
                    "declared_object": obj_raw,
                    "guard": guard,
                    "route_to": route_to,
                    "reason": "The declared name is a limit-form or context-dependent object; it must be fixed by mode, use, accessible field, traces, and limits before audit.",
                }
            break

    if contains_any_pattern(full_context, TOTALIZING_PATTERNS):
        warnings.append("TOTALIZING_LANGUAGE_REQUIRES_BOUNDARY_CHECK")

    return {
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "route": route,
    }


def external_evidence_audit(case: Dict[str, Any]) -> Dict[str, Any]:
    evidence = case.get("external_evidence")
    if evidence in (None, "", [], {}):
        return {
            "present": False,
            "source_repo_status": "NO_EXTERNAL_SOURCE",
            "errors": [],
            "warnings": [],
            "false_sufficiency_risk": False,
            "summary": "No external evidence packet supplied.",
        }

    if not isinstance(evidence, dict):
        return {
            "present": True,
            "source_repo_status": "INVALID_EXTERNAL_EVIDENCE",
            "errors": ["Err_EXTERNAL_EVIDENCE_NOT_OBJECT"],
            "warnings": [],
            "false_sufficiency_risk": True,
            "summary": "external_evidence must be a JSON object if supplied.",
        }

    source = evidence.get("source_repo")
    status = source_repo_status(source)
    errors: List[str] = []
    warnings: List[str] = []

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
            "input_contract": "FAILED",
            "errors": ["Err_INPUT_NOT_JSON_OBJECT"],
        }

    invalid_types = invalid_required_types(case)
    if invalid_types:
        return {
            "runtime_version": VERSION,
            "status": "INVALID_INPUT",
            "standing": "NO_OPERATIONAL_STANDING",
            "input_contract": "FAILED",
            "invalid_field_types": invalid_types,
            "errors": ["Err_REQUIRED_FIELD_NOT_STRING"],
            "required_fields": REQUIRED_FIELDS,
            "parent_repo": PARENT_REPO,
        }

    missing = missing_required(case)
    if missing:
        errors.append("Err_RUNTIME_SCHEMA_INCOMPLETE")

    if is_fake_preuse(case):
        return {
            "runtime_version": VERSION,
            "status": "NO_OPERATIONAL_STANDING",
            "standing": "NO_OPERATIONAL_STANDING",
            "input_contract": "FAILED_FAKE_USE",
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
            "input_contract": "INSUFFICIENT_INPUT",
            "missing_fields": missing,
            "errors": sorted(set(errors)),
            "required_fields": REQUIRED_FIELDS,
            "parent_repo": PARENT_REPO,
        }

    context_guard = context_indexed_object_audit(case)
    substance = operational_substance_audit(case)
    external = external_evidence_audit(case)

    errors.extend(context_guard.get("errors", []))
    errors.extend(substance.get("errors", []))
    errors.extend(external.get("errors", []))
    warnings.extend(context_guard.get("warnings", []))
    warnings.extend(substance.get("warnings", []))
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
    if context_guard.get("route"):
        opportunities.append(
            "Repair declared object by routing it to its context-indexed operational form before treating it as audit-ready."
        )
    if substance.get("weak_fields"):
        opportunities.append(
            "Replace generic field labels with concrete object, use, dependency, failure condition, and operational realignment."
        )

    return {
        "runtime_version": VERSION,
        "status": status,
        "standing": standing,
        "input_contract": "PASSED_WITH_REPAIR_REQUIRED" if errors else "PASSED",
        "object": obj,
        "mode": mode,
        "use": use,
        "accessible_field": field,
        "context_indexed_object_guard": context_guard,
        "operational_substance_guard": substance,
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
            "input_contract": "FAILED",
            "errors": ["Err_INVALID_JSON_OR_PATH"],
            "detail": str(exc),
        }

    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("status") not in {"INVALID_INPUT"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
