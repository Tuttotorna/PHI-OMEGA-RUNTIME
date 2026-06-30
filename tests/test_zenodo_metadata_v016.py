import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITATION = ROOT / "CITATION.cff"
ZENODO = ROOT / ".zenodo.json"
AGENT_DOC = ROOT / "AGENT_EXCHANGE_LOOP_EVAL.md"
SCENARIO_NOTE = ROOT / "docs" / "SCENARIO_CUSTOM_EVAL_NOTE.md"
TOOL = ROOT / "tools" / "agent_exchange_loop_eval.py"

def read(path):
    return path.read_text(encoding="utf-8")

def test_citation_cff_exists_and_has_valid_basic_shape():
    assert CITATION.exists()
    text = read(CITATION)
    assert "cff-version: 1.2.0" in text
    assert 'title: "PHI-OMEGA-RUNTIME"' in text
    assert "authors:" in text
    assert 'family-names: "Brighindi"' in text
    assert 'given-names: "Massimiliano"' in text
    assert 'repository-code: "https://github.com/Tuttotorna/PHI-OMEGA-RUNTIME"' in text
    assert 'version: "v0.1.7"' in text
    assert 'date-released: "2026-06-30"' in text
    assert "\\u003c" not in text
    assert "\\u003e" not in text

def test_zenodo_json_exists_and_is_valid_json():
    assert ZENODO.exists()
    data = json.loads(read(ZENODO))
    assert data["title"] == "PHI-OMEGA-RUNTIME"
    assert data["upload_type"] == "software"
    assert data["access_right"] == "closed"
    assert data["version"] == "v0.1.7"
    assert data["publication_date"] == "2026-06-23"
    assert data["creators"][0]["name"] == "Brighindi, Massimiliano"

def test_zenodo_json_preserves_all_rights_reserved():
    data = json.loads(read(ZENODO))
    description = data["description"]
    assert "All rights reserved." in description
    assert "No license is granted by this archive record." in description
    assert "license" not in data

def test_zenodo_json_links_runtime_key_and_scenario_note():
    data = json.loads(read(ZENODO))
    identifiers = {item["identifier"] for item in data["related_identifiers"]}
    assert "https://github.com/Tuttotorna/PHI-OMEGA-RUNTIME/blob/main/AGENT_EXCHANGE_LOOP_EVAL.md" in identifiers
    assert "https://github.com/Tuttotorna/PHI-OMEGA-RUNTIME/blob/main/docs/SCENARIO_CUSTOM_EVAL_NOTE.md" in identifiers
    assert "https://github.com/Tuttotorna/PHI-OMEGA-OPERATIONAL-FORMULA/releases/tag/v0.1.66" in identifiers

def test_runtime_key_and_adapter_still_exist():
    assert AGENT_DOC.exists()
    assert TOOL.exists()
    assert SCENARIO_NOTE.exists()
    assert "PHI-OMEGA Agent Exchange-Loop Eval checks whether an AI agent has a real give/receive loop" in read(AGENT_DOC)
    assert "Scenario is one possible use environment." in read(SCENARIO_NOTE)
