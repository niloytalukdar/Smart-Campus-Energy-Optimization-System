# GridWise AI

Smart Campus Energy Optimization AI System.

## Running Locally

1. Set up the `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
   Add your `OPENAI_API_KEY` to the `.env` file.

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Example cURL Requests

**GET /health**
```bash
curl -X GET http://localhost:8000/health
```

**POST /optimize-energy**
```bash
curl -X POST http://localhost:8000/optimize-energy \
-H "Content-Type: application/json" \
-d '{
  "scenario_id": "GRID-101",
  "operator_notes": [
    "Do not charge the battery between 2 PM and 4 PM"
  ],
  "battery": {
    "capacity_kwh": 100.0,
    "initial_energy_kwh": 50.0,
    "max_charge_rate_kwh": 25.0,
    "max_discharge_rate_kwh": 25.0,
    "charge_efficiency": 0.95,
    "discharge_efficiency": 0.95
  },
  "hours": [
    {"hour": 0, "demand_kwh": 20.0, "solar_kwh": 0.0, "price": 0.1},
    {"hour": 1, "demand_kwh": 18.0, "solar_kwh": 0.0, "price": 0.1},
    {"hour": 2, "demand_kwh": 15.0, "solar_kwh": 0.0, "price": 0.1},
    {"hour": 3, "demand_kwh": 15.0, "solar_kwh": 0.0, "price": 0.1},
    {"hour": 4, "demand_kwh": 16.0, "solar_kwh": 0.0, "price": 0.1},
    {"hour": 5, "demand_kwh": 20.0, "solar_kwh": 0.0, "price": 0.1},
    {"hour": 6, "demand_kwh": 30.0, "solar_kwh": 5.0, "price": 0.2},
    {"hour": 7, "demand_kwh": 40.0, "solar_kwh": 15.0, "price": 0.3},
    {"hour": 8, "demand_kwh": 50.0, "solar_kwh": 30.0, "price": 0.5},
    {"hour": 9, "demand_kwh": 55.0, "solar_kwh": 45.0, "price": 0.5},
    {"hour": 10, "demand_kwh": 60.0, "solar_kwh": 60.0, "price": 0.5},
    {"hour": 11, "demand_kwh": 60.0, "solar_kwh": 70.0, "price": 0.5},
    {"hour": 12, "demand_kwh": 58.0, "solar_kwh": 75.0, "price": 0.5},
    {"hour": 13, "demand_kwh": 55.0, "solar_kwh": 70.0, "price": 0.5},
    {"hour": 14, "demand_kwh": 50.0, "solar_kwh": 60.0, "price": 0.5},
    {"hour": 15, "demand_kwh": 45.0, "solar_kwh": 45.0, "price": 0.5},
    {"hour": 16, "demand_kwh": 40.0, "solar_kwh": 25.0, "price": 0.5},
    {"hour": 17, "demand_kwh": 45.0, "solar_kwh": 10.0, "price": 0.8},
    {"hour": 18, "demand_kwh": 60.0, "solar_kwh": 0.0, "price": 1.0},
    {"hour": 19, "demand_kwh": 65.0, "solar_kwh": 0.0, "price": 1.0},
    {"hour": 20, "demand_kwh": 55.0, "solar_kwh": 0.0, "price": 0.8},
    {"hour": 21, "demand_kwh": 45.0, "solar_kwh": 0.0, "price": 0.5},
    {"hour": 22, "demand_kwh": 35.0, "solar_kwh": 0.0, "price": 0.3},
    {"hour": 23, "demand_kwh": 25.0, "solar_kwh": 0.0, "price": 0.1}
  ]
}'
```

*Note: battery.max_charge_rate_kwh defaults to capacity/4 if not provided. The demand_increase factor is capped at 5.0.*
