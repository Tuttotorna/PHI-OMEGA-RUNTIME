# PHI-OMEGA-RUNTIME CLI Reference — v0.2.0

This document stabilizes the public command surface introduced by the runtime.

## Stable commands

### phi-omega-demo

Runs the packaged Transition Sufficiency Framework demo.

Expected behavior:
- produces JSON;
- returns a transition decision;
- demonstrates that positive gain does not authorize execution when required support is missing.

### phi-omega-check <case.json>

Evaluates a transition case JSON file.

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

### phi-omega-runtime <case.json> --json

Runs the historical PHI-OMEGA runtime audit surface.

This command remains an operational audit surface, not proof of the parent theory.

### phi-omega-agent-eval <case.json>

Runs the Agent Exchange-Loop Eval surface.

This command evaluates whether an agent output has a real receive/give/field-return loop before being treated as sufficient for use.

## Decision values

- ALLOW: execute.
- REPAIR: repair missing ordinary support before execution.
- SOFT_BLOCK: verifier depth or gain threshold insufficient.
- HARD_BLOCK: explicit non-repairable hard support missing.

## Non-expansion rule

v0.2.0 stabilizes the public interface. It does not add a new theoretical layer.
