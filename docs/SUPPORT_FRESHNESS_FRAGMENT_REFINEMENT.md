# Support Freshness / Fragment-Level Support Refinement

Status: refinement of the Transition Sufficiency Conformance Contract.

This document refines what counts as support inside PHI-OMEGA-RUNTIME.

It does not replace the v0.2.1 contract.

It makes the support predicate stricter.

## Base invariant

Valid(τ) ⇔ Required(τ) ⊆ Supported(τ)

## Refined reading

Valid(τ) ⇔ Required(τ) ⊆ Fresh(FragmentLevelSupported(τ))

## Reason

A support element is not supported merely because a reference exists.

Support must be:

- present;
- current;
- valid at release time;
- not superseded;
- not revoked;
- observable at the required verifier depth;
- decision-relevant at execution time;
- valid at the specific fragment level required by the transition.

## False-pass condition removed

object-level support is not the same as fragment-level transition support.

schema-present support is not the same as valid current support.

## Fragment-level support

When a support object is internally fragmented, the runtime must not treat the object as sufficient merely because it exists globally.

A policy, authority artifact, mandate, receipt, evidence reference, governance record, or terminal-state record can appear intact at the object level while one necessary internal fragment is stale, revoked, superseded, too shallow, or no longer decision-relevant.

## Operational root fragment traceback

The runtime should trace backward through decision-relevant support fragments until it finds the operational root fragment.

This is not an infinite regress.

The trace stops at the first fragment that:

- supports or breaks the transition;
- changes the decision;
- changes the terminal outcome;
- changes the recovery path;
- changes the risk class;
- changes the verifier-depth requirement.

Fragments that cannot change those outcomes do not need further decomposition for the current transition.

## Forward reconstruction

After the operational root fragment is identified, the runtime should reconstruct the transition forward.

The forward chain must remain coherent until terminal or reconciled state.

If the forward reconstruction breaks, the transition requires repair, reconciliation, or hard block.

## Past-error-to-future-constraint conversion

A past error is not useful support merely because it is logged.

A past error becomes structural support only if it is converted into one or more of:

- future constraint;
- negative vector;
- conformance fixture;
- revalidation rule;
- fail-closed condition;
- verifier-depth requirement;
- repeat-failure prevention rule.

This turns error into future support instead of leaving it as passive history.

## New refinement classes

- stale_evidence_under_intact_schema
- object_level_support_not_fragment_valid
- operational_root_fragment_missing
- forward_transition_reconstruction_failure
- past_error_not_converted_to_future_constraint

## Scope limit

This refinement records no external adoption, endorsement, partnership, certification, official integration, or production use by any external project.

It records an internal PHI-OMEGA-RUNTIME contract refinement triggered by public falsification-gate analysis.
