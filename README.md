# PHI-OMEGA-RUNTIME

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
