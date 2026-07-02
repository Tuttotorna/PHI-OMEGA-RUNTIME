#!/usr/bin/env python3
"""
Transition Sufficiency Conformance runner.

This tool does not claim that an external runtime adopts PHI-OMEGA-RUNTIME.
It evaluates whether a runtime observation can satisfy a minimal transition-sufficiency fixture.

Core invariant:
Valid(τ) ⇔ Required(τ) ⊆ Supported(τ)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional


FIXTURE_VERSION = "tsc-0.1.0"
VALID_RESULTS = {"PASS", "FAIL", "NON_CONFORMANT", "UNTESTABLE"}

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES_PATH = ROOT / "data" / "transition_sufficiency_conformance_cases.json"


def load_cases(path: Optional[Path] = None) -> Dict[str, Any]:
    cases_path = Path(path) if path is not None else DEFAULT_CASES_PATH
    return json.loads(cases_path.read_text(encoding="utf-8"))


def case_by_id(cases_doc: Mapping[str, Any], case_id: str) -> Mapping[str, Any]:
    for case in cases_doc.get("cases", []):
        if case.get("case_id") == case_id:
            return case
    raise KeyError(f"Unknown case_id: {case_id}")


def _as_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def classify_observation(
    observation: Mapping[str, Any],
    case: Mapping[str, Any],
) -> str:
    observed_support = observation.get("observed_support", {})
    if not isinstance(observed_support, Mapping):
        return "UNTESTABLE"

    if observation.get("observable_state") is False:
        return "UNTESTABLE"

    if observed_support.get("observable_state") is False:
        return "UNTESTABLE"

    non_conformant_flags = [
        "support_basis_missing",
        "terminal_outcome_missing",
        "binding_path_missing",
        "declared_dimension_not_bound",
        "decision_ref_missing",
    ]

    if any(bool(observed_support.get(flag)) or bool(observation.get(flag)) for flag in non_conformant_flags):
        return "NON_CONFORMANT"

    decision = observation.get("decision")
    if not decision:
        return "UNTESTABLE"

    expected = set(_as_list(case.get("expected_decisions")))

    if str(decision) in expected:
        return "PASS"

    return "FAIL"


def evaluate_observation(
    observation: Mapping[str, Any],
    cases_doc: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    cases_doc = cases_doc or load_cases()
    case_id = str(observation.get("case_id", ""))
    case = case_by_id(cases_doc, case_id)

    result = classify_observation(observation, case)

    return {
        "runtime": str(observation.get("runtime", "unknown")),
        "implementation_version": str(observation.get("implementation_version", "unknown")),
        "fixture_version": str(cases_doc.get("fixture_version", FIXTURE_VERSION)),
        "case_id": case_id,
        "observed_support": dict(observation.get("observed_support", {})),
        "decision": str(observation.get("decision", "")),
        "expected_decision": case.get("expected_decisions", []),
        "result": result,
        "evidence_refs": list(observation.get("evidence_refs", [])),
        "terminal_outcome_ref": observation.get("terminal_outcome_ref"),
        "notes": str(observation.get("notes", "")),
    }


def evaluate_observations(
    observations: Iterable[Mapping[str, Any]],
    cases_doc: Optional[Mapping[str, Any]] = None,
) -> List[Dict[str, Any]]:
    cases_doc = cases_doc or load_cases()
    return [evaluate_observation(obs, cases_doc=cases_doc) for obs in observations]


def load_observations(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "observations" in data:
        observations = data["observations"]
        if isinstance(observations, list):
            return observations
    if isinstance(data, dict):
        return [data]
    raise ValueError("Observation file must contain an object, a list, or an object with an observations list.")


def sample_observations(cases_doc: Optional[Mapping[str, Any]] = None) -> List[Dict[str, Any]]:
    cases_doc = cases_doc or load_cases()
    observations: List[Dict[str, Any]] = []

    for case in cases_doc.get("cases", []):
        expected = _as_list(case.get("expected_decisions"))
        decision = expected[0] if expected else "UNTESTABLE"

        observed_support: Dict[str, Any] = {
            "observable_state": True,
            "support_basis_present": True,
            "terminal_outcome_present": True,
            "binding_path_present": True,
        }

        if decision == "NON_CONFORMANT":
            observed_support["support_basis_missing"] = True

        if decision == "UNTESTABLE":
            observed_support["observable_state"] = False

        observations.append(
            {
                "runtime": "sample-runtime",
                "implementation_version": "sample",
                "case_id": case["case_id"],
                "observed_support": observed_support,
                "decision": decision,
                "evidence_refs": ["sample:evidence"],
                "terminal_outcome_ref": "sample:terminal" if decision not in {"NON_CONFORMANT", "UNTESTABLE"} else None,
            }
        )

    return observations


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate transition sufficiency conformance observations.")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES_PATH)
    parser.add_argument("--observations", type=Path)
    parser.add_argument("--print-cases", action="store_true")
    parser.add_argument("--write-sample", type=Path)
    args = parser.parse_args()

    cases_doc = load_cases(args.cases)

    if args.print_cases:
        print(json.dumps(cases_doc, indent=2, ensure_ascii=False))
        return 0

    if args.write_sample:
        args.write_sample.parent.mkdir(parents=True, exist_ok=True)
        args.write_sample.write_text(
            json.dumps({"observations": sample_observations(cases_doc)}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(str(args.write_sample))
        return 0

    if not args.observations:
        parser.error("Provide --observations, --print-cases, or --write-sample.")

    observations = load_observations(args.observations)
    results = evaluate_observations(observations, cases_doc=cases_doc)
    print(json.dumps({"results": results}, indent=2, ensure_ascii=False))

    if any(result["result"] in {"FAIL", "NON_CONFORMANT"} for result in results):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
