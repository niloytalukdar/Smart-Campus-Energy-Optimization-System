from app.services.energy_validator import validate_plan
from app.models.request_models import HourData, BatterySpec
from app.models.response_models import HourlyPlanItem

def test_validate_plan_valid():
    hours = [HourData(hour=h, demand_kwh=10.0, solar_kwh=0.0, price=0.1) for h in range(24)]
    battery = BatterySpec(capacity_kwh=20.0, initial_energy_kwh=10.0, max_charge_rate_kwh=5.0, max_discharge_rate_kwh=5.0)
    plan = [
        HourlyPlanItem(hour=h, grid_kwh=10.0, solar_used_kwh=0.0, battery_action="idle", battery_kwh=0.0, battery_soc_kwh=10.0)
        for h in range(24)
    ]
    
    is_valid, warnings, total_cost = validate_plan(plan, hours, battery)
    assert is_valid is True
    assert len(warnings) == 0
    assert total_cost == 24.0

def test_validate_plan_invalid_balance():
    hours = [HourData(hour=h, demand_kwh=10.0, solar_kwh=0.0, price=0.1) for h in range(24)]
    battery = BatterySpec(capacity_kwh=20.0, initial_energy_kwh=10.0, max_charge_rate_kwh=5.0, max_discharge_rate_kwh=5.0)
    plan = [
        HourlyPlanItem(hour=h, grid_kwh=5.0, solar_used_kwh=0.0, battery_action="idle", battery_kwh=0.0, battery_soc_kwh=10.0)
        for h in range(24)
    ]
    
    is_valid, warnings, total_cost = validate_plan(plan, hours, battery)
    assert is_valid is False
    assert len(warnings) > 0
    assert "Energy balance mismatch" in warnings[0]
