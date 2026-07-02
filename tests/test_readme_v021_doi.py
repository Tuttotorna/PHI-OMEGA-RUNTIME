from pathlib import Path


def test_readme_contains_v021_doi():
    text = Path("README.md").read_text(encoding="utf-8")

    assert "v0.2.1" in text
    assert "10.5281/zenodo.21126013" in text
    assert "https://doi.org/10.5281/zenodo.21126013" in text
    assert "Transition Sufficiency Conformance Contract" in text


def test_readme_doi_scope_limit_present():
    text = Path("README.md").read_text(encoding="utf-8").lower()

    assert "does not imply external adoption" in text
    assert "endorsement" in text
    assert "partnership" in text
    assert "certification" in text
    assert "official integration" in text
