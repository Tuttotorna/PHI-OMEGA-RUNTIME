# PHI-OMEGA Runtime Failure Map

Status: field map, not endorsement.

Core invariant:

```text
Valid(tau) iff Required(tau) subset Supported(tau)
```

## Purpose

This map collects public runtime and agentic-system failure signals and classifies them as transition sufficiency cases.

The map does not claim that any listed project uses PHI-OMEGA-RUNTIME.

It only records that independent systems are encountering the same structural boundary:

```text
a proposed action changes downstream state before transition sufficiency is proven
```

## Pattern

The recurring structure is:

```text
tool call / approval / checkpoint / retry / permission / cryptographic state
→ proposed transition tau
→ Required(tau)
→ Supported(tau)
→ missing support
→ ALLOW / REPAIR / SOFT_BLOCK / HARD_BLOCK
```

## Cases

| System | Issue | Runtime decision | Observed failure class | Minimal gate |
|---|---:|---:|---|---|
| CrewAI | [crewAIInc/crewAI #4877](https://github.com/crewAIInc/crewAI/issues/4877) | REPAIR | missing pre-tool-call authorization boundary | GuardrailProvider returns ALLOW/BLOCK before each tool call. |
| CrewAI | [crewAIInc/crewAI #6165](https://github.com/crewAIInc/crewAI/issues/6165) | REPAIR | tool-call release decision boundary | Emit a structured decision object for every tool-call release. |
| Anthropic Claude Code | [anthropics/claude-code #65910](https://github.com/anthropics/claude-code/issues/65910) | HARD_BLOCK | approval identity replacement / LIFO prompt ambiguity | Block execution if approval_id, command_hash, and visible prompt do not match. |
| Anthropic Claude Code | [anthropics/claude-code #66173](https://github.com/anthropics/claude-code/issues/66173) | HARD_BLOCK | filesystem boundary access without explicit permission transition | Require explicit authorization before any file operation outside declared workspace boundary. |
| Microsoft VS Code / Copilot | [microsoft/vscode #308999](https://github.com/microsoft/vscode/issues/308999) | REPAIR | permission stream closes before final response state | Do not close permission stream until response completion or explicit cancellation state is recorded. |
| Microsoft Semantic Kernel | [microsoft/semantic-kernel #14072](https://github.com/microsoft/semantic-kernel/issues/14072) | HARD_BLOCK | auto function invocation without runtime access control | Block auto function invocation unless function authority is explicitly supported at runtime. |
| LangGraph | [langchain-ai/langgraph #7417](https://github.com/langchain-ai/langgraph/issues/7417) | REPAIR | checkpoint replay without transition identity preservation | Before replay, compare checkpoint execution identity and require replay authorization. |
| Kubernetes | [kubernetes/kubernetes #138950](https://github.com/kubernetes/kubernetes/issues/138950) | HARD_BLOCK | state validity extended despite unhealthy support dependency | Do not extend DEK expiration when KMS health support is invalid. |
| Microsoft AutoGen | [microsoft/autogen #7372](https://github.com/microsoft/autogen/issues/7372) | REPAIR | distributed agent governance needs cryptographic transition authority | Bind distributed agent action to verifiable identity, authority, and recomputable decision evidence. |
| Ibex Agent Verification | [safal207/ibex-agent-verification #59](https://github.com/safal207/ibex-agent-verification/issues/59) | ALLOW | verifier depth becomes transition authority | Use verifier depth as a first-class transition authority field. |
| Microsoft Agent Governance Toolkit | [microsoft/agent-governance-toolkit #3204](https://github.com/microsoft/agent-governance-toolkit/issues/3204) | REPAIR | governance requires transition sufficiency before downstream state change | Require a transition sufficiency result before downstream state change. |

## Non-claims

- No endorsement is claimed.
- No partnership is claimed.
- No adoption is claimed.
- No certification is claimed.
- No theoretical proof is claimed.

## Operational claim

The operational claim is narrower:

```text
PHI-OMEGA-RUNTIME provides a reusable transition gate for classifying and repairing unsupported runtime transitions before downstream state change.
```

## Public formulation

Do not say:

```text
PHI-OMEGA solves everything.
```

Say:

```text
These are not separate bugs. They are transition sufficiency failures.
```
