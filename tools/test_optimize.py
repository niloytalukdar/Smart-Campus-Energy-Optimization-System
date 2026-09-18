import httpx

payload = {
    "scenario_id": "TEST-UI",
    "operator_notes": [
        "Solar output will drop to 20% from 13:00 to 15:00",
        "Do not charge battery between 17 and 20"
    ],
    "battery": {
        "capacity_kwh": 100.0,
        "initial_energy_kwh": 50.0,
        "max_charge_rate_kwh": 25.0,
        "max_discharge_rate_kwh": 25.0,
        "charge_efficiency": 0.95,
        "discharge_efficiency": 0.95
    },
    "hours": []
}
for i in range(24):
    payload['hours'].append({
        'hour': i,
        'demand_kwh': 20.0,
        'solar_kwh': 10.0 if 8 <= i <= 17 else 0.0,
        'price': 0.1 if i < 12 else 0.5
    })

with httpx.Client(timeout=30.0) as c:
    r = c.post('http://127.0.0.1:8000/optimize-energy', json=payload)
    print(r.status_code)
    try:
        print(r.json())
    except Exception:
        print(r.text)
