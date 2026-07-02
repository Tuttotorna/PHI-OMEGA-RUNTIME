from pathlib import Path


def test_runtime_external_convergence_log_exists():
    text = Path("PHI_OMEGA_RUNTIME_AUDIT_LOG_1.md").read_text(encoding="utf-8")

    assert "External Runtime Convergence Signal" in text
    assert "Valid(τ) ⇔ Required(τ) ⊆ Supported(τ)" in text
    assert "local authorization surface ≠ supported execution transition" in text
    assert "No runtime may claim a transition is valid" in text


def test_runtime_external_convergence_scope_is_non_adoption():
    text = Path("PHI_OMEGA_RUNTIME_AUDIT_LOG_1.md").read_text(encoding="utf-8").lower()

    assert "does not claim adoption" in text
    assert "endorsement" in text
    assert "partnership" in text
    assert "official integration" in text
    assert "certification" in text


def test_runtime_external_convergence_conformance_contract_present():
    text = Path("docs/RUNTIME_EXTERNAL_CONVERGENCE_SIGNAL_2026_07_02.md").read_text(encoding="utf-8")

    required_phrases = [
        "authorized action equals executed action",
        "execution context still supports authorization",
        "support basis is reconstructable",
        "terminal outcome is recorded",
        "withdrawn support before execution changes the decision",
        "approval_args_hash",
        "execution_args_hash",
        "HARD_BLOCK",
        "NON_CONFORMANT",
    ]

    for phrase in required_phrases:
        assert phrase in text
