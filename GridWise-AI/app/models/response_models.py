from pydantic import BaseModel
from typing import List, Optional, Literal

class Directive(BaseModel):
    directive_type: Literal[
        "solar_reduction",
        "solar_outage",
        "no_charge_window",
        "no_discharge_window",
        "demand_increase",
        "demand_decrease"
    ]
    hours: List[int]
    factor: Optional[float] = None
    structured_adjustment: Optional[dict] = None

class HourlyPlanItem(BaseModel):
    hour: int
    grid_kwh: float
    solar_used_kwh: float
    battery_action: Literal["charge", "discharge", "idle"]
    battery_kwh: float
    battery_soc_kwh: float

class OptimizeResponse(BaseModel):
    scenario_id: str
    directive_interpretation: List[Directive]
    hourly_plan: List[HourlyPlanItem]
    total_cost: float
    status: Literal["ok", "solved_with_warnings", "infeasible"]
    warnings: List[str]
