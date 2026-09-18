import pulp
from typing import List, Tuple
from app.models.request_models import HourData, BatterySpec
from app.models.response_models import Directive, HourlyPlanItem

def solve_schedule(hours: List[HourData], battery: BatterySpec, directives: List[Directive]) -> Tuple[List[HourlyPlanItem], str]:
    # Step 1 - Apply directives
    effective_solar = [h.solar_kwh for h in hours]
    effective_demand = [h.demand_kwh for h in hours]
    no_charge_hours = set()
    no_discharge_hours = set()
    
    for d in directives:
        if d.directive_type == "solar_reduction":
            for h in d.hours:
                effective_solar[h] *= d.factor
        elif d.directive_type == "solar_outage":
            for h in d.hours:
                effective_solar[h] = 0.0
        elif d.directive_type == "demand_decrease" or d.directive_type == "demand_increase":
            for h in d.hours:
                effective_demand[h] *= d.factor
        elif d.directive_type == "no_charge_window":
            for h in d.hours:
                no_charge_hours.add(h)
        elif d.directive_type == "no_discharge_window":
            for h in d.hours:
                no_discharge_hours.add(h)
                
    # Step 2 - Build the PuLP MILP model
    prob = pulp.LpProblem("GridWise_Optimization", pulp.LpMinimize)
    
    grid = pulp.LpVariable.dicts("grid", range(24), lowBound=0)
    solar_used = pulp.LpVariable.dicts("solar_used", range(24), lowBound=0)
    charge = pulp.LpVariable.dicts("charge", range(24), lowBound=0, upBound=battery.max_charge_rate_kwh)
    discharge = pulp.LpVariable.dicts("discharge", range(24), lowBound=0, upBound=battery.max_discharge_rate_kwh)
    is_charging = pulp.LpVariable.dicts("is_charging", range(24), cat=pulp.LpBinary)
    soc = pulp.LpVariable.dicts("soc", range(24), lowBound=0, upBound=battery.capacity_kwh)
    
    for h in range(24):
        # cap solar
        prob += solar_used[h] <= effective_solar[h]
        
        # Energy balance
        prob += effective_demand[h] + charge[h] == grid[h] + solar_used[h] + discharge[h]
        
        # Mutual exclusion
        prob += charge[h] <= battery.max_charge_rate_kwh * is_charging[h]
        prob += discharge[h] <= battery.max_discharge_rate_kwh * (1 - is_charging[h])
        
        # State of charge recursion
        if h == 0:
            prev_soc = battery.initial_energy_kwh
        else:
            prev_soc = soc[h-1]
            
        prob += soc[h] == prev_soc + charge[h] * battery.charge_efficiency - discharge[h] / battery.discharge_efficiency
        
        # Directives
        if h in no_charge_hours:
            prob += charge[h] == 0
        if h in no_discharge_hours:
            prob += discharge[h] == 0
            
    # Objective
    prob += pulp.lpSum([grid[h] * hours[h].price for h in range(24)])
    
    # Step 3 - Solve
    solver = pulp.PULP_CBC_CMD(timeLimit=15, msg=False)
    prob.solve(solver)
    
    if pulp.LpStatus[prob.status] != 'Optimal':
        return [], "infeasible"
        
    # Step 4 - Build plan
    plan = []
    for h in range(24):
        c_val = charge[h].varValue
        d_val = discharge[h].varValue
        
        if c_val > 0.001:
            action = "charge"
            bat_kwh = c_val
        elif d_val > 0.001:
            action = "discharge"
            bat_kwh = d_val
        else:
            action = "idle"
            bat_kwh = 0.0
            
        plan.append(HourlyPlanItem(
            hour=h,
            grid_kwh=round(grid[h].varValue, 2),
            solar_used_kwh=round(solar_used[h].varValue, 2),
            battery_action=action,
            battery_kwh=round(bat_kwh, 2),
            battery_soc_kwh=round(soc[h].varValue, 2)
        ))
        
    return plan, "ok"
