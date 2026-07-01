# Transition Schema Surface — v0.2.0

The Transition Sufficiency Framework uses two public schema surfaces.

## Input schema

Path:

schemas/transition_case.schema.json

Required top-level fields:
- transition_id
- proposed_action
- required
- supported

Main support dimensions:
- authority
- boundary
- context
- evidence
- policy
- time_window
- recovery

Hard support dimensions:
- hard_authority
- hard_boundary
- hard_policy

Verifier and gain fields:
- verifier_depth
- minimum_gain
- estimated_gain

## Output schema

Path:

schemas/transition_result.schema.json

Stable result fields:
- transition_id
- decision
- valid
- formula
- state_before
- proposed_action
- state_after
- missing_requirements
- hard_block_reasons
- required_subset_supported
- verifier_depth_required
- verifier_depth_supported
- verifier_depth_ok
- minimum_gain_required
- estimated_gain_supported
- gain_ok
- reason
- next_allowed_transition

## Core invariant

Valid(tau) iff Required(tau) subset Supported(tau)

## Hard-block condition

HARD_BLOCK is produced when a required hard support field is missing from supported hard support.

Hard support fields:
- hard_authority
- hard_boundary
- hard_policy
