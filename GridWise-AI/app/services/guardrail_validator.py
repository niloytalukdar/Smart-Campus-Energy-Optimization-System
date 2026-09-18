from typing import List, Tuple, Dict, Any
from app.models.response_models import Directive

VALID_TYPES = {
    "solar_reduction",
    "solar_outage",
    "no_charge_window",
    "no_discharge_window",
    "demand_increase",
    "demand_decrease"
}

def validate_directives(raw_directives: List[Dict[str, Any]]) -> Tuple[List[Directive], List[str]]:
    validated = []
    warnings = []

    for raw in raw_directives:
        directive_type = raw.get("directive_type")
        
        # Rule 1
        if not directive_type or directive_type not in VALID_TYPES:
            warnings.append(f"Rejected directive: Unknown or missing directive_type '{directive_type}'")
            continue
            
        # Rule 2
        hours = raw.get("hours")
        if not isinstance(hours, list) or len(hours) == 0:
            warnings.append(f"Rejected directive: 'hours' must be a non-empty list. Type: {directive_type}")
            continue
            
        valid_hours = True
        for h in hours:
            if not isinstance(h, int) or h < 0 or h > 23:
                warnings.append(f"Rejected directive: hour {h} is outside valid range 0-23. Type: {directive_type}")
                valid_hours = False
                break
                
        if not valid_hours:
            continue
            
        # Rule 3 & 4
        factor = raw.get("factor")
        
        if directive_type in {"solar_reduction", "demand_decrease"}:
            if not isinstance(factor, (int, float)):
                warnings.append(f"Rejected directive: 'factor' must be a number for {directive_type}")
                continue
            if factor < 0.0 or factor > 1.0:
                warnings.append(f"Rejected directive: 'factor' {factor} must be in [0, 1] for {directive_type}")
                continue
                
        elif directive_type == "demand_increase":
            if not isinstance(factor, (int, float)):
                warnings.append(f"Rejected directive: 'factor' must be a number for {directive_type}")
                continue
            if factor <= 1.0 or factor > 5.0:
                warnings.append(f"Rejected directive: 'factor' {factor} must be in (1.0, 5.0] for {directive_type}")
                continue
                
        elif directive_type in {"solar_outage", "no_charge_window", "no_discharge_window"}:
            # Ignore factor if present
            factor = None

        # Create validated directive and preserve any structured_adjustment
        structured_adjustment = raw.get("structured_adjustment") if isinstance(raw, dict) else None
        try:
            d = Directive(
                directive_type=directive_type,
                hours=hours,
                factor=factor,
                structured_adjustment=structured_adjustment
            )
            validated.append(d)
        except Exception as e:
            warnings.append(f"Rejected directive: Pydantic validation failed for {directive_type} - {str(e)}")

    return validated, warnings
