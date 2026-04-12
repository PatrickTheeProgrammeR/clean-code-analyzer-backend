from app.services.code_analysis_service import _coerce_int_score, _parse_analyze_response


def test_coerce_int_score_clamps():
    assert _coerce_int_score(15) == 10
    assert _coerce_int_score(0) == 1
    assert _coerce_int_score("8") == 8
    assert _coerce_int_score("x") == 5


def test_parse_analyze_response_fills_issues_when_score_low():
    raw = '{"score": 3, "summary": "Słabo", "issues": []}'
    out = _parse_analyze_response(raw)
    assert out["score"] == 3
    assert out["summary"] == "Słabo"
    assert len(out["issues"]) == 2
    assert "ponownie" in out["issues"][0]["suggestion"].lower()
