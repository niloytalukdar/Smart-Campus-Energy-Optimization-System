# GridWise AI

GridWise AI is a Smart Campus Energy Optimization AI System. It combines large language models (LLMs) with mathematical optimization (PuLP) to interpret natural language operator notes and enforce energy constraints across a microgrid campus.

---

## 📖 Project Details

**Objective:**
The primary goal is to minimize peak energy costs and respect thermal grid constraints while factoring in real-world scenarios (solar outages, demand spikes, battery maintenance). Operators can type in natural language restrictions, and the system intelligently applies them.

**System Architecture:**
The architecture relies on 4 core modules acting in a pipeline:
1. **LLM Interpreter** (`app/services/llm_interpreter.py`): Translates human text into strict JSON directives.
2. **Guardrail Validator** (`app/services/guardrail_validator.py`): Ensures that AI-generated directives obey physical system limits (e.g. valid hours, reasonable load factors).
3. **Optimization Engine** (`app/services/optimizer.py`): Formulates and solves a Mixed Integer Linear Programming (MILP) problem to schedule battery charging and discharging.
4. **Energy Validator** (`app/services/energy_validator.py`): A final check that the scheduled hourly plan is mathematically sound and energy balances zero out.

---

## 🚀 Step-by-Step Setup

Follow these steps to run the GridWise AI backend locally:

### Step 1: Clone and Configure Environment
1. Clone the repository and navigate to the root directory.
2. Copy the example environment variables file:
   ```bash
   cp .env.example .env
   ```
3. Open the `.env` file and paste in your active `OPENAI_API_KEY`. The LLM interpreter requires this to parse operator notes.

### Step 2: Install Dependencies
Ensure you have Python 3.9+ installed, then install the necessary dependencies via pip:
```bash
pip install -r requirements.txt
```
*(Dependencies include FastAPI, Uvicorn, PuLP, OpenAI, and Pydantic).*

### Step 3: Run the Application
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
The server will start at `http://localhost:8000`.

---

## 🖥️ User Interface (UI)
The system includes a sleek, telemetry-styled user interface for Operators to run scenarios.
- **Location:** The UI HTML files are stored in `system_ui/`.
- **How to view:** Simply open `system_ui/ai_interpretation/code.html` in your web browser. You can use the "Load Random Example" button to automatically generate complex constraints and send them to the backend API!

---

## 🔗 Example API Usage

If you prefer to hit the API directly using tools like `cURL` or Postman, you can use the `/optimize-energy` endpoint.

### Example cURL Request

```bash
curl -X POST http://localhost:8000/optimize-energy \
-H "Content-Type: application/json" \
-d '{
  "scenario_id": "GRID-101",
  "operator_notes": [
    "Solar output will drop to 20% from 13:00 to 15:00 due to maintenance."
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
    {"hour": 12, "demand_kwh": 58.0, "solar_kwh": 75.0, "price": 0.5},
    {"hour": 13, "demand_kwh": 55.0, "solar_kwh": 70.0, "price": 0.5}
  ]
}'
```

*(Note: The hours array should ideally contain all 24 hours. Battery `max_charge_rate_kwh` defaults to capacity/4 if not provided.)*
