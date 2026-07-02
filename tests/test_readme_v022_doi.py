from pathlib import Path


def test_readme_contains_v022_doi():
    text = Path("README.md").read_text(encoding="utf-8")

    assert "v0.2.2 DOI" in text
    assert "https://doi.org/10.5281/zenodo.21130843" in text
    assert "Support Freshness / Fragment-Level Support Refinement" in text
    assert "Fresh(FragmentLevelSupported(τ))" in text


def test_provenance_contains_v022_doi():
    text = Path("PROVENANCE.md").read_text(encoding="utf-8")

    assert "2026-07-02 — v0.2.2 DOI" in text
    assert "https://doi.org/10.5281/zenodo.21130843" in text
    assert "does not move or recreate the release tag" in text
    assert "does not claim external adoption" in text
