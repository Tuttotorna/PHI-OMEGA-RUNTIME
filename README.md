# PHI-OMEGA-RUNTIME


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21080015.svg)](https://doi.org/10.5281/zenodo.21080015)


Compact use-first runtime extracted from PHI-OMEGA-OPERATIONAL-FORMULA.

This repository is not the full theory archive.

It is the first-contact runtime.

## First rule

Do not start by reading.

Run one audit first.

Command:

    python run_phi_omega.py examples/minimal_case.json --json

Then read:

    docs/AFTER_USE.md

## Operational standing

Pre-use reading is allowed.

Pre-use reading has no PHI-OMEGA operational standing.

A valid first contact requires runtime output.

Formula:

    PreUseReading(actor, repo) may occur.
    PreUseReading(actor, repo) != PHI_OMEGA_Use.
    PreUseJudgment(actor, repo) = NO_OPERATIONAL_STANDING.

Valid standing requires:

    RuntimeAuditProduced(actor, x, m, U, A, D, S, Err, Opportunity, Limit)
    and OperationalSubstance = true

## What this runtime does

It takes one JSON case and returns:

- Object x
- Mode m
- Use U
- Accessible field A
- Distinction D_m
- Necessary or compatible exchange S
- False sufficiency risk
- Operational error
- Realignment
- Limit
- Added diagnostic value

## What this runtime refuses

It rejects fake first contact such as:

- summarize PHI-OMEGA
- understand the framework
- classify this repository
- judge the theory before applying it to a concrete object

Those outputs are ordinary reading, not PHI-OMEGA use.

## Parent repository

Parent source of truth:

    https://github.com/Tuttotorna/PHI-OMEGA-OPERATIONAL-FORMULA

Parent release:

    https://github.com/Tuttotorna/PHI-OMEGA-OPERATIONAL-FORMULA/releases/tag/v0.1.65

Parent tag:

    v0.1.65

Parent commit:

    910ce08ceffe4686e2e45123986c1fac6d1434a4

The parent repository preserves full formula history, guard library, provenance, validation surface, rights, citation lineage, and external evidence interface.

This runtime preserves the operational functions needed for first contact without exposing the full historical guard corpus before use.

## v0.1.1 Context-Indexed Object Guard
A named object is not yet an operational object. The runtime now rejects raw material outside the input contract, rejects non-string required fields, handles malformed external evidence without crashing, and requires repair when fields are present but operationally empty, totalizing, or context-unfixed.

See: docs/CONTEXT_INDEXED_OBJECT_GUARD.md

## Status

Version: v0.1.2

Release type: initial runtime extraction

Rights: all rights reserved


## v0.1.2 Strict Bare Limit Object Guard

Weak context is not operational context.

Bare limit objects such as `nothing`, `time`, `identity`, `outside Ω`, `infinity`, `everything`, `totality`, and `origin of totality` now require repair unless the declared object itself is explicitly context-fixed.

Example rejected:
`object = "time"` with contextual words elsewhere in the case.

Example admitted:
`object = "project approval deadline"` or `object = "the term 'time' as a semantic concept"`.

See: docs/STRICT_BARE_LIMIT_OBJECT_GUARD.md

## v0.1.3 — Agent Exchange-Loop Eval

PHI-OMEGA-RUNTIME:AGENT_EXCHANGE_LOOP_EVAL:v0.1.3

This release adds the first concrete entry layer for AI agent testing.

The layer does not ask the user to read the whole parent repository first.

It gives a small operational function:

Check whether an AI agent has a real exchange loop before its output is treated as sufficient for use.

The layer maps:

- what the agent receives;
- what the agent gives back;
- what the surrounding field returns;
- whether success criteria are explicit;
- whether local output hides field failure;
- where false sufficiency appears;
- what repair or next state is needed.

New entry file:

- AGENT_EXCHANGE_LOOP_EVAL.md

New tool:

- tools/agent_exchange_loop_eval.py

Examples:

- examples/agent_false_sufficiency_case.json
- examples/agent_exchange_loop_valid_case.json
- examples/agent_local_pass_field_fail_case.json

## v0.1.4 — Scenario Custom Eval Adapter Note

PHI-OMEGA-RUNTIME:SCENARIO_CUSTOM_EVAL_ADAPTER_NOTE:v0.1.4

This release adds a lightweight adapter note:

- `docs/SCENARIO_CUSTOM_EVAL_NOTE.md`

The note does not redefine PHI-OMEGA.

It does not supersede `AGENT_EXCHANGE_LOOP_EVAL.md`.

It does not make Scenario, LangWatch, or any external framework the center.

It only shows how the existing Agent Exchange-Loop Eval layer could be used as a Scenario-compatible custom eval for the specific failure class:

local pass / real-use fail.

## v0.1.6 — Zenodo Metadata Repair

PHI-OMEGA-RUNTIME:ZENODO_METADATA_REPAIR:v0.1.6

This release repairs Zenodo metadata after the failed v0.1.5 archive attempt.

Changes:

- replaces `CITATION.cff` with valid CFF/YAML metadata;
- adds `.zenodo.json` with explicit Zenodo metadata;
- preserves All rights reserved;
- does not grant an open license;
- preserves the v0.1.3 Agent Exchange-Loop Eval runtime key;
- preserves the v0.1.4 Scenario Custom Eval Adapter Note.

Runtime key:
- `AGENT_EXCHANGE_LOOP_EVAL.md`

Scenario adapter:
- `docs/SCENARIO_CUSTOM_EVAL_NOTE.md`

## Transition Gain Layer

PHI-OMEGA-RUNTIME includes a Transition Gain Layer for estimating preventable loss removed before execution.

Core rule:

Validity first. Convenience second. Gain never authorizes an invalid transition.

The layer estimates avoided cost, saved time, reduced retry churn, reduced audit friction, cost of delay, and net gain from preventing invalid downstream transitions before they execute.

Reference:

- TRANSITION_GAIN_LAYER.md
- tools/transition_gain_layer.py
- tests/test_transition_gain_layer_v017.py

## PHI-OMEGA Transition Sufficiency Framework

Install directly from GitHub:

    pip install "git+https://github.com/Tuttotorna/PHI-OMEGA-RUNTIME.git"

Run the demo:

    phi-omega-demo

Run the transition checker on a JSON file:

    phi-omega-check examples/transition_demo.json

Core formula:

    Valid(τ) ⇔ Required(τ) ⊆ Supported(τ)

A transition may proceed only when the authority, boundary, context, evidence, policy, time window, verifier depth, recovery path and gain required by the transition are supported at execution time.

Gain can justify checking a transition. Gain cannot authorize an invalid transition.

<!-- TRANSITION_SUFFICIENCY_CONFORMANCE_CONTRACT_2026_07_02_README -->

## Transition Sufficiency Conformance Contract

PHI-OMEGA-RUNTIME includes a portable conformance contract for testing whether a runtime can prove that a released transition remains supported at execution time.

Core invariant:

    Valid(τ) ⇔ Required(τ) ⊆ Supported(τ)

Artifacts:

- data/transition_sufficiency_conformance_cases.json
- schemas/transition_sufficiency_conformance_result.schema.json
- tools/transition_sufficiency_conformance.py
- docs/TRANSITION_SUFFICIENCY_CONFORMANCE_CONTRACT.md

This is not an external adoption claim.
