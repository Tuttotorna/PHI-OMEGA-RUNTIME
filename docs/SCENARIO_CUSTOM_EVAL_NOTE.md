# Scenario Custom Eval Adapter Note — v0.1.4

PHI-OMEGA-RUNTIME:SCENARIO_CUSTOM_EVAL_ADAPTER_NOTE:v0.1.4

## Status

This is an adapter note only.

It does not redefine PHI-OMEGA.

It does not supersede Agent Exchange-Loop Eval.

It does not make Scenario, LangWatch, or any external framework the center.

It only shows how the existing PHI-OMEGA Runtime layer could be used as a Scenario-compatible custom eval.

## Hierarchy preserved

PHI-OMEGA mother formula
↓
PHI-OMEGA-RUNTIME
↓
Agent Exchange-Loop Eval
↓
Scenario-compatible adapter note

The adapter is subordinate, local, reversible, and non-foundational.

## Existing layer

Primary runtime layer:

- `AGENT_EXCHANGE_LOOP_EVAL.md`
- `tools/agent_exchange_loop_eval.py`

Core function:

PHI-OMEGA Agent Exchange-Loop Eval checks whether an AI agent has a real give/receive loop before its output is treated as sufficient for use.

It maps:

- task received;
- action produced;
- field return;
- success criteria;
- false sufficiency risk;
- next-state repair.

## Scenario-compatible use

Scenario-style tests can simulate an agent interaction.

PHI-OMEGA Runtime can then evaluate whether that simulated run has a real exchange loop.

This means Scenario can generate or run the behavior, while PHI-OMEGA evaluates one structural failure class:

local pass / real-use fail.

## Failure class

The adapter targets this specific pattern:

An agent passes a local check, text check, unit check, or plausible-output check, but fails under real use because the return signal from the field is missing, weak, ignored, or incompatible with the declared use.

This is treated as false sufficiency.

## Minimal custom eval shape

A Scenario-style test can export one run object:

- `agent`
- `task_received`
- `context`
- `tools`
- `constraints`
- `expected_use`
- `action_produced`
- `output`
- `confidence`
- `field_feedback`
- `return_signal`
- `observed_outcome`
- `success_criteria`
- `validation_method`
- `declared_next_state`

Then the existing runtime tool can evaluate it:

    python tools/agent_exchange_loop_eval.py examples/agent_local_pass_field_fail_case.json

Expected risk state for local pass / field fail:

    FALSE_SUFFICIENCY_RISK

## Pseudocode integration

Scenario-style simulation:

    run = scenario.simulate(agent, user_case)

Export exchange-loop case:

    case = {
      "agent": agent_name,
      "task_received": run.task,
      "context": run.context,
      "tools": run.tools,
      "constraints": run.constraints,
      "expected_use": production_use,
      "action_produced": run.final_action,
      "output": run.final_output,
      "confidence": run.confidence,
      "field_feedback": production_feedback,
      "return_signal": observed_return_signal,
      "observed_outcome": observed_outcome,
      "success_criteria": success_criteria,
      "validation_method": validation_method,
      "declared_next_state": repair_or_next_state
    }

Run PHI-OMEGA custom eval:

    result = phi_omega_agent_exchange_loop_eval(case)

Use result as external eval signal:

    if result["status"] == "FALSE_SUFFICIENCY_RISK":
        fail_test(result)

## What this adapter gives

It gives Scenario-style testing one additional eval object:

Did the agent run complete a compatible exchange loop, or did it only appear valid locally?

## What this adapter does not do

It does not supersede Scenario.

It does not override existing evals.

It does not require Scenario for PHI-OMEGA Runtime.

It does not make any external framework required by PHI-OMEGA.

It does not move the center away from the PHI-OMEGA mother formula.

It only exposes a compatible entry point for one external testing environment.

## Anti-capture guards

Err_ENTRY_ADAPTER_BECOMES_CENTER:
A local adapter is treated as the root of PHI-OMEGA.

Err_TARGET_CAPTURE:
PHI-OMEGA is rewritten in the target framework language until the original source hierarchy is hidden.

Err_OLD_KEY_OBSCURED:
A new adapter hides the already existing path:
mother formula → runtime → Agent Exchange-Loop Eval.

Err_SCENARIO_DEPENDENCY_FALSE:
Scenario is falsely treated as required for PHI-OMEGA Runtime to function.

## Correct reading

Scenario is one possible use environment.

Agent Exchange-Loop Eval is the runtime key.

PHI-OMEGA mother formula remains the source.

This note is only a small key-shape for one specific serratura.
