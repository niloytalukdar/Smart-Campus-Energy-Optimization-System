from pydantic import BaseModel, Field, model_validator
from typing import List, Optional

class HourData(BaseModel):
    hour: int = Field(..., ge=0, le=23)
    demand_kwh: float = Field(..., ge=0.0)
    solar_kwh: float = Field(..., ge=0.0)
    price: float = Field(..., ge=0.0)

class BatterySpec(BaseModel):
    capacity_kwh: float = Field(..., gt=0.0)
    initial_energy_kwh: float = Field(..., ge=0.0)
    max_charge_rate_kwh: Optional[float] = None
    max_discharge_rate_kwh: Optional[float] = None
    charge_efficiency: Optional[float] = Field(0.95, gt=0.0, le=1.0)
    discharge_efficiency: Optional[float] = Field(0.95, gt=0.0, le=1.0)

    @model_validator(mode='after')
    def check_initial_energy_and_defaults(self) -> 'BatterySpec':
        if self.initial_energy_kwh > self.capacity_kwh:
            raise ValueError('initial_energy_kwh must be <= capacity_kwh')
        
        if self.max_charge_rate_kwh is None:
            self.max_charge_rate_kwh = self.capacity_kwh / 4.0
            
        if self.max_discharge_rate_kwh is None:
            self.max_discharge_rate_kwh = self.capacity_kwh / 4.0
            
        return self

class OptimizeRequest(BaseModel):
    scenario_id: str
    operator_notes: List[str]
    hours: List[HourData]
    battery: BatterySpec

    @model_validator(mode='after')
    def validate_hours(self) -> 'OptimizeRequest':
        if len(self.hours) != 24:
            raise ValueError("hours list must contain exactly 24 items")
        
        for i, h in enumerate(self.hours):
            if h.hour != i:
                raise ValueError(f"hours must be a clean 0..23 sequence, mismatch at index {i} where hour={h.hour}")
        
        return self
