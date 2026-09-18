from typing import List, Tuple
from app.models.request_models import HourData, BatterySpec
from app.models.response_models import HourlyPlanItem

def validate_plan(plan: List[HourlyPlanItem], hours: List[HourData], battery: BatterySpec) -> Tuple[bool, List[str], float]:
    is_valid = True
    warnings = []
    
    soc = battery.initial_energy_kwh
    total_cost = 0.0
    
    for h in range(24):
        item = plan[h]
        hour_data = hours[h]
        
        charge = item.battery_kwh if item.battery_action == "charge" else 0.0
        discharge = item.battery_kwh if item.battery_action == "discharge" else 0.0
        
        # 1. Energy balance
        provided = item.grid_kwh + item.solar_used_kwh + discharge - charge
        if abs(provided - hour_data.demand_kwh) > 0.01:
            warnings.append(f"Energy balance mismatch at hour {h}")
            is_valid = False
            
        # 2. State of charge
        soc = soc + charge * battery.charge_efficiency - discharge / battery.discharge_efficiency
        if soc < -0.01 or soc > battery.capacity_kwh + 0.01:
            warnings.append(f"SOC violation at hour {h}: {soc}")
            is_valid = False
            
        # 3. Mutual exclusion
        if charge > 0 and discharge > 0:
            warnings.append(f"Simultaneous charge and discharge at hour {h}")
            is_valid = False
            
        # 4. Total cost
        total_cost += item.grid_kwh * hour_data.price
        
    return is_valid, warnings, round(total_cost, 2)
