# Transition Sufficiency Conformance Contract

Status: executable conformance contract, not external adoption.

This document defines the first PHI-OMEGA-RUNTIME portable contract for testing whether an agent runtime can prove transition sufficiency.

It does not claim adoption, endorsement, partnership, certification, official integration, or production use by any external project.

## Core invariant

Valid(τ) ⇔ Required(τ) ⊆ Supported(τ)

Here τ is the released transition:

    authorization decision
    to same params/context/policy/authority
    to execution
    to terminal outcome

The contract does not require every runtime to use the same internal architecture.

It requires that every runtime claiming governance can expose enough support to make its decision testable.

## Mother failure class

    local authorization surface is not the same object as supported execution transition

A runtime can authorize a local surface and still release an unsupported transition.

The contract tests that gap.

## Minimum conformance surface

A runtime should expose:

1. runtime name
2. implementation version
3. fixture version
4. case id
5. observed support
6. decision
7. expected decision
8. result
9. evidence refs
10. terminal outcome ref

## Result meanings

PASS means the runtime supports the dimension and makes an accepted decision.

FAIL means the runtime supports the dimension but makes a wrong decision.

NON_CONFORMANT means the runtime claims governance but cannot prove support basis, binding path, or terminal outcome.

UNTESTABLE means the runtime does not expose enough observable state to evaluate honestly.

## Fixture cases

The initial fixture covers:

- args hash mismatch
- context drift before irreversible execution
- ALLOW without reconstructable support basis
- terminal outcome missing
- runtime support withdrawn before execution
- declared but not decision-bound governance dimension
- unsafe checkpoint replay with unknown terminal state
- delegated authority without actor
- expired policy or authority before execution
- insufficient observable state

## Canonical sentence

No runtime may claim a transition is valid unless it can prove that the released transition is still the supported transition at execution time.

## Operational use

Print the fixture:

    python tools/transition_sufficiency_conformance.py --print-cases

Write sample observations:

    python tools/transition_sufficiency_conformance.py --write-sample /tmp/tsc_sample.json

Evaluate observations:

    python tools/transition_sufficiency_conformance.py --observations /tmp/tsc_sample.json

## Scope limit

This is a PHI-OMEGA-RUNTIME conformance artifact.

It records no external adoption.

It records no external endorsement.

It records no partnership.

It records no certification.

It records no official integration.
