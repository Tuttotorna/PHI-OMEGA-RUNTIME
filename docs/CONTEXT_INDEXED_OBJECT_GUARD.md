# Context-Indexed Object Guard — v0.1.1

PHI-OMEGA-RUNTIME v0.1.1 adds an executable first-contact guard:

A named object is not yet an operational object.

An object becomes audit-ready only when mode, use, accessible field, traces, and limits fix its operational form.

Core distinction:

Name(x) != Object_{A,m,U}(x)

The runtime is not an AI interpreter. It does not infer hidden context. If the input is raw text, a single word, a symbol, or a non-object JSON value, the runtime rejects it as invalid input.

If the input is a JSON case but contains generic, totalizing, autoreferential, or context-unfixed fields, the runtime returns REQUIRES_REPAIR rather than treating the case as fully valid.

This preserves the first-contact rule:

raw material != runtime case

and adds:

declared object != audit-ready operational object
fields present != operational substance

New guard families:
- Err_REQUIRED_FIELD_NOT_STRING
- Err_EXTERNAL_EVIDENCE_NOT_OBJECT
- Err_DECLARED_OBJECT_REQUIRES_CONTEXT
- Err_DECLARED_OBJECT_NOT_AUDITABLE_AS_DECLARED
- Err_ACCESSIBLE_FIELD_TOTALIZED
- Err_OPERATIONAL_SUBSTANCE_INSUFFICIENT
- Err_REALIGNMENT_AUTOREFERENTIAL
- Err_DEPENDENCY_OPERATIONALLY_EMPTY

The guard does not replace the parent repository. It ports one operational principle from the parent guard corpus into the compact runtime entry layer.
