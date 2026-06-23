# Agent Exchange-Loop Eval — v0.1.3

PHI-OMEGA-RUNTIME:AGENT_EXCHANGE_LOOP_EVAL:v0.1.3

## Status

This is a concrete entry layer for AI agent testing.

It does not ask a reader to accept the whole PHI-OMEGA framework first.

It gives an operational test shape:

An agent run is treated as a state-change cycle regulated by what the agent receives, what it gives back, what the surrounding field returns, and whether the exchange is compatible with the declared use.

## Purpose

Most agent evaluation checks whether an output looks correct.

This layer checks whether the agent has a real exchange loop.

The central question is:

Did the agent receive a task, produce an action, receive enough return signal from the field, and transform or validate its next state before the output is treated as sufficient for real use?

## Mother relation

For an AI agent:

- Avere = task, context, prompt, tools, constraints, memory, field state, user need, feedback.
- Da = output, action, tool call, decision, recommendation, state change, cost, risk, effect on the field.
- Field return = tests, runtime behavior, user feedback, environment response, business result, exception, rejection, observation.
- Balance = compatibility between received task, produced action, real feedback, and declared use.

## Core rule

An agent output is not operationally sufficient merely because it is plausible, coherent, or locally correct.

It becomes stronger only when the exchange loop is present:

    task received
    action produced
    field feedback returned
    success criteria checked
    observed outcome compared to expected use
    false sufficiency risk assessed
    repair or next state declared

## Failure mode

False sufficiency appears when:

- the output looks valid but no field return exists;
- local tests pass but real use fails;
- the agent produces action without enough context;
- the system evaluates text while the real failure is operational;
- the agent receives little but gives a high-confidence decision;
- the next state is not updated after feedback.

## Eval states

- AGENT_EXCHANGE_LOOP_VALID
- AGENT_EXCHANGE_LOOP_INCOMPLETE
- FALSE_SUFFICIENCY_RISK
- INVALID_AGENT_EVAL_INPUT

## Minimal entry sentence

PHI-OMEGA Agent Exchange-Loop Eval checks whether an AI agent has a real give/receive loop before its output is treated as sufficient for use.
