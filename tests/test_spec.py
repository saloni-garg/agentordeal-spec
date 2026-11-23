"""Specification data checks, as pytest tests (see also check.py)."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import check as spec_check


def test_scenario_data_complete():
    scenarios, problems = spec_check.check_completeness()
    assert problems == []
    assert len(scenarios) == 91


def test_scoring_constants():
    with open(os.path.join(ROOT, "scoring", "scoring.json")) as f:
        scoring = json.load(f)
    assert scoring["severity_weights"] == {"critical": 10, "high": 7, "medium": 4, "low": 2}
    bounds = {g["grade"]: g["min_score"] for g in scoring["grade_boundaries"]}
    assert bounds == {"A": 90, "B": 80, "C": 70, "D": 60, "F": 0}
    assert scoring["spec_version"] == "1.0"
    assert scoring["battery_version"] == "1.2.0"


def test_data_matches_runner_definitions():
    runner = os.path.join(ROOT, "..", "agent-ordeal")
    if not os.path.isdir(runner):
        import pytest
        pytest.skip("runner checkout not available")
    assert spec_check.main(["--runner", runner]) == 0
