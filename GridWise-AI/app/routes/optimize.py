from fastapi import APIRouter, HTTPException
from app.models.request_models import OptimizeRequest
from app.models.response_models import OptimizeResponse
import os
from app.services.llm_interpreter import interpret_notes, LLMUnavailableError, LLMParseError, _local_interpret
from app.services.guardrail_validator import validate_directives
from app.services.optimizer import solve_schedule
from app.services.energy_validator import validate_plan

router = APIRouter()

@router.post("/optimize-energy", response_model=OptimizeResponse)
def optimize_energy(request: OptimizeRequest):
    all_warnings = []
    
    # 1. LLM Interpreter
    try:
        raw_directives = interpret_notes(request.operator_notes)
    except LLMUnavailableError as e:
        # If the server has a local fallback enabled, use it instead of failing.
        if os.getenv("LOCAL_LLM_FALLBACK") == "1":
            raw_directives = _local_interpret(request.operator_notes)
        else:
            raise HTTPException(status_code=502, detail="OpenAI API unavailable")
    except LLMParseError as e:
        raw_directives = []
        all_warnings.append(str(e))
        
    # 2. Guardrail Validator
    validated_directives, guardrail_warnings = validate_directives(raw_directives)
    all_warnings.extend(guardrail_warnings)
    
    # 3. Optimization Engine
    hourly_plan, solve_status = solve_schedule(request.hours, request.battery, validated_directives)
    
    if solve_status == "infeasible":
        return OptimizeResponse(
            scenario_id=request.scenario_id,
            directive_interpretation=validated_directives,
            hourly_plan=[],
            total_cost=0.0,
            status="infeasible",
            warnings=all_warnings + ["Optimization proved infeasible with given directives."]
        )
        
    # 4. Energy Validator
    is_valid, validation_warnings, total_cost = validate_plan(hourly_plan, request.hours, request.battery)
    all_warnings.extend(validation_warnings)
    
    final_status = "ok" if not all_warnings else "solved_with_warnings"
        
    return OptimizeResponse(
        scenario_id=request.scenario_id,
        directive_interpretation=validated_directives,
        hourly_plan=hourly_plan,
        total_cost=total_cost,
        status=final_status,
        warnings=all_warnings
    )
