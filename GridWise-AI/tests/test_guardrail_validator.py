from app.services.guardrail_validator import validate_directives

def test_validate_directives_valid():
    raw = [{"directive_type": "solar_reduction", "hours": [12, 13], "factor": 0.5}]
    validated, warnings = validate_directives(raw)
    assert len(validated) == 1
    assert len(warnings) == 0
    assert validated[0].directive_type == "solar_reduction"

def test_validate_directives_out_of_range_hour():
    raw = [{"directive_type": "no_charge_window", "hours": [23, 30]}]
    validated, warnings = validate_directives(raw)
    assert len(validated) == 0
    assert len(warnings) == 1
    assert "outside valid range" in warnings[0]

def test_validate_directives_bad_factor():
    raw = [{"directive_type": "demand_increase", "hours": [1], "factor": 0.5}]
    validated, warnings = validate_directives(raw)
    assert len(validated) == 0
    assert len(warnings) == 1
    assert "must be in (1.0, 5.0]" in warnings[0]

def test_validate_directives_unknown_type():
    raw = [{"directive_type": "magic_spell", "hours": [1], "factor": 2.0}]
    validated, warnings = validate_directives(raw)
    assert len(validated) == 0
    assert len(warnings) == 1
    assert "Unknown or missing" in warnings[0]

def test_validate_directives_window_ignores_factor():
    raw = [{"directive_type": "no_charge_window", "hours": [1], "factor": 0.9}]
    validated, warnings = validate_directives(raw)
    assert len(validated) == 1
    assert len(warnings) == 0
    assert validated[0].factor is None
