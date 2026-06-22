# Strict Bare Limit Object Guard — v0.1.2

PHI-OMEGA-RUNTIME v0.1.2 fixes the remaining weakness found by quasi-valid JSON stress testing.

Core rule:

Weak context is not operational context.

v0.1.1 correctly rejected raw text, non-string required fields, missing fields, malformed external evidence, fake pre-use reading, generic cosmetic cases, and autoreferential realignment. But stress testing found that some bare limit objects still passed when weak context words appeared elsewhere in the case.

Example of the false pass class:

object = "time"
mode = "validity"
use = "audit it itself"
accessible_field = "project field, operational dependencies, locally observed trace"

This must not pass.

For limit objects, the declared object itself must be context-fixed.

Examples that require repair:
- object = "nothing"
- object = "time"
- object = "identity"
- object = "outside Ω"
- object = "infinity"
- object = "totality"
- object = "origin of totality"

Examples that can pass when the rest of the case is operationally sufficient:
- object = "the word 'nothing' as a linguistic concept"
- object = "project approval deadline"
- object = "identity record version"
- object = "formal infinity symbol"
- object = "local fragment origin"
- object = "bounded accessible field"

New error:
- Err_WEAK_CONTEXT_AS_CONTEXT_FIX

Definition:
The runtime treats weak context appearing elsewhere in the case as if it fixed the declared object. v0.1.2 blocks that route.

This preserves the parent principle:

A name is not yet an operational object.
An object becomes audit-ready only when mode, use, accessible field, traces, and limits fix its operational form.
