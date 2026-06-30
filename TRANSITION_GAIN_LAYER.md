# PHI-OMEGA-RUNTIME — Transition Gain Layer

## Status

Runtime extension layer.

This layer introduces operational convenience and gain estimation into PHI-OMEGA-RUNTIME.

It does not replace transition validity.

It measures the expected gain of preventing invalid transitions before execution.

---

## Core rule

Validity first.

Convenience second.

Gain never authorizes an invalid transition.

A profitable invalid transition remains invalid.

---

## Runtime purpose

The Transition Gain Layer estimates how much preventable loss is removed by applying a PHI-OMEGA runtime gate before execution.

The gain is not only monetary.

It may include:

- money saved;
- time saved;
- energy saved;
- reduced retry churn;
- reduced debugging cost;
- reduced audit cost;
- reduced rollback cost;
- reduced compliance exposure;
- reduced reputational damage;
- faster valid replanning;
- lower cost of delay.

---

## Mother distinction

Capability is not transition validity.

Authorization is not transition sufficiency.

A block is not sufficient if it does not preserve the path toward a valid next transition.

A runtime gate becomes economically useful when it converts preventable invalid execution into valid replanning.

---

## Controlled object

The controlled object for this layer is:

agent action
+ transition validity
+ failure probability
+ average incident cost
+ debug / audit cost
+ compliance / reputation exposure
+ cost of delay
+ retry cost
+ replanning value
+ net gain from prevention

---

## Required runtime fields

A transition-gain evaluation may include:

- attempted_transitions
- baseline_failure_rate
- guarded_failure_rate
- average_failure_cost
- debug_hours_saved_per_prevented_failure
- hourly_operational_cost
- compliance_or_reputation_cost_avoided
- gate_operational_cost
- cost_of_delay
- transition_valid
- decision_path

---

## Output fields

The runtime should produce:

- prevented_invalid_transitions
- expected_cost_avoided
- expected_time_cost_saved
- gross_gain
- net_gain
- preventable_failure_reduction_percent
- gain_multiple
- decision_path
- gain_classification

---

## Decision boundary

ALLOW

The transition is valid and the expected gain is non-negative or strategically justified.

REPAIR

The transition is not yet valid, but missing dependencies can be supplied, bounded, verified, or made explicit.

SOFT_BLOCK

The transition should not execute now, but may become valid after remediation, approval, budget refresh, backoff, or context update.

HARD_BLOCK

The transition violates authority, privacy, legal, tenant, safety, PHI, or irreversible-state boundaries.

It must not retry automatically.

---

## Economic interpretation

The gain is preventable loss removed before execution.

Formula:

prevented_invalid_transitions =
attempted_transitions
x
max(0, baseline_failure_rate - guarded_failure_rate)

expected_cost_avoided =
prevented_invalid_transitions
x
average_failure_cost

expected_time_cost_saved =
prevented_invalid_transitions
x
debug_hours_saved_per_prevented_failure
x
hourly_operational_cost

net_gain =
expected_cost_avoided
+
expected_time_cost_saved
+
compliance_or_reputation_cost_avoided
-
gate_operational_cost
-
cost_of_delay

---

## PHI-OMEGA / PHi-FORMULA classification

The gain is not only more control.

The gain is less wasted execution, less retry churn, less downstream damage, less audit friction, and faster valid replanning.

Runtime economic principle:

Less invalid transition = less loss.
Less loss = higher usable gain.
Higher usable gain = stronger adoption incentive.

---

## Non-override guard

This layer must never convert an invalid transition into an allowed transition because the expected monetary gain is positive.

If transition_valid == False, the result must be REPAIR, SOFT_BLOCK, or HARD_BLOCK.

Profit cannot override invalidity.

---

## Strategic use

This layer is the practical entry point for human adoption.

Do not ask stakeholders to accept PHI-OMEGA because it is total.

Show that the gate reduces loss, time, risk, waste, failed retries, and preventable execution cost.

Human-entry phrase:

Here you are losing value.
This gate prevents that loss before execution.
