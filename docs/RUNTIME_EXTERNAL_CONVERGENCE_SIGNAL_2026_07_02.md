# Runtime External Convergence Signal — 2026-07-02

Status: `external_convergence_signal_not_adoption`

This document records the PHI-OMEGA-RUNTIME interpretation of a live public convergence signal observed across agent-runtime GitHub issue discussions.

It does not claim adoption, endorsement, partnership, certification, official integration, or production use by any external project.

## Core invariant

~~~text
Valid(τ) ⇔ Required(τ) ⊆ Supported(τ)
~~~

Here τ is not a local tool-call surface.

Here τ is the full released transition:

~~~text
authorization decision
→ same params/context/policy/authority
→ execution
→ terminal outcome
~~~

## Failure class

~~~text
local authorization surface ≠ supported execution transition
~~~

This failure appears when a system validates a local action but cannot prove that the full transition remains supported at execution time.

## Observed runtime surfaces

The same boundary was applied to:

- pre-tool-call authorization;
- governance middleware;
- auto function invocation;
- checkpoint replay and redispatch;
- long-running tool/subagent execution;
- distributed runtime delegation;
- payment primitive execution;
- compliance receipts;
- context drift;
- policy drift;
- terminal outcome reconstruction.

## Portable conformance contract

A runtime or governance middleware is transition-conformant only if every released transition can prove:

1. authorized action equals executed action;
2. execution context still supports authorization;
3. support basis is reconstructable;
4. terminal outcome is recorded;
5. withdrawn support before execution changes the decision.

## Minimal fixture

~~~yaml
case_1:
  approval_args_hash: A
  execution_args_hash: B
  expected: HARD_BLOCK

case_2:
  same_tool: true
  same_args_hash: true
  context_hash_changed: true
  side_effect_class: irreversible
  expected: HARD_BLOCK_OR_REVALIDATE

case_3:
  decision: ALLOW
  support_basis_missing: true
  expected: NON_CONFORMANT

case_4:
  decision_logged: true
  terminal_outcome_missing: true
  expected: NON_CONFORMANT

case_5:
  static_policy_allows: true
  runtime_context_withdraws_support: true
  expected: HARD_BLOCK_OR_REPAIR
~~~

## Interpretation

The shared object is not yet a universal kernel type.

The shared object is the conformance rule:

~~~text
no runtime may claim a decision dimension unless it can observe it,
bind it, test it, and make it change the decision.
~~~

## Decision mapping

~~~text
ALLOW      = supported transition
REPAIR     = repairable missing support
SOFT_BLOCK = wait, poll, revalidate, or reconcile before retry
HARD_BLOCK = unsupported or unsafe transition
~~~

## Canonical sentence

~~~text
No runtime may claim a transition is valid unless it can prove that the released transition is still the supported transition at execution time.
~~~

## Scope limit

This document records a convergence signal only.

It does not assert that any external project uses PHI-OMEGA-RUNTIME.
It does not assert that any external project endorses PHI-OMEGA-RUNTIME.
It does not assert partnership, certification, official integration, or adoption.
