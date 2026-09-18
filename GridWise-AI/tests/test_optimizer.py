from app.models.request_models import HourData, BatterySpec
from app.models.response_models import Directive
from app.services.optimizer import solve_schedule

def test_solve_schedule_simple():
    hours = [
        HourData(hour=h, demand_kwh=10.0, solar_kwh=0.0, price=0.1)
        for h in range(24)
    ]
    battery = BatterySpec(capacity_kwh=20.0, initial_energy_kwh=10.0, max_charge_rate_kwh=5.0, max_discharge_rate_kwh=5.0)
    
    plan, status = solve_schedule(hours, battery, [])
    assert status == "ok"
    assert len(plan) == 24

def test_solve_schedule_no_charge_window():
    hours = [
        HourData(hour=h, demand_kwh=10.0, solar_kwh=5.0, price=0.1 if h < 12 else 0.5)
        for h in range(24)
    ]
    battery = BatterySpec(capacity_kwh=20.0, initial_energy_kwh=10.0, max_charge_rate_kwh=5.0, max_discharge_rate_kwh=5.0)
    directives = [Directive(directive_type="no_charge_window", hours=[1, 2])]
    
    plan, status = solve_schedule(hours, battery, directives)
    assert status == "ok"
    
    # Ensure hour 1 and 2 has charge = 0.0
    for h in [1, 2]:
        assert plan[h].battery_action in ("idle", "discharge")
        if plan[h].battery_action == "charge":
            assert plan[h].battery_kwh == 0.0
