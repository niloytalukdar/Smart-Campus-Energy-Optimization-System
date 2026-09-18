# Working Log — Smart Campus Energy Optimization AI System

## Milestone 1 — Scaffolding
- [x] Create folder structure exactly as in Section 3
- [x] requirements.txt (fastapi, uvicorn, pydantic, pulp, openai,
      python-dotenv, pytest, httpx for test client)
- [x] .env.example with OPENAI_API_KEY=
- [x] .gitignore (.env, __pycache__, .venv)
- [x] config.py loads env vars, raises clear error if API key missing

## Milestone 2 — Data Models
- [x] request_models.py: HourData, BatterySpec, OptimizeRequest
- [x] response_models.py: Directive, HourlyPlanItem, OptimizeResponse
- [x] Field validators enforce ranges from Section 4 (422 on violation)

## Milestone 3 — LLM Interpreter
- [x] llm_interpreter.py implemented per Section 6
- [x] Handles empty operator_notes without an API call
- [x] JSON parse retry logic implemented
- [x] Timeout + retry-with-backoff on network error implemented
- [x] Unit test: valid note → correct directive shape
- [x] Unit test: malformed LLM response → raises LLMParseError, not a crash

## Milestone 4 — Guardrail Validator
- [x] guardrail_validator.py implemented per Section 7, all 5 rules
- [x] Unit test: out-of-range hour (e.g. 30) is rejected
- [x] Unit test: bad factor value is rejected
- [x] Unit test: unknown directive_type is rejected
- [x] Unit test: valid directive passes through unchanged

## Milestone 5 — Optimization Engine
- [x] optimizer.py implemented per Section 8, full PuLP model
- [x] Handles no_charge_window / no_discharge_window correctly
- [x] Handles solar_reduction / solar_outage correctly
- [x] Handles demand_increase / demand_decrease correctly
- [x] Returns "infeasible" status gracefully, never crashes
- [x] Unit test: simple scenario (flat price) solves as expected
- [x] Unit test: no_charge_window forces charge=0 in those hours

## Milestone 6 — Energy Validator
- [x] energy_validator.py implemented per Section 9
- [x] Unit test: valid plan passes all checks
- [x] Unit test: deliberately broken plan is caught (balance mismatch)
- [x] total_cost computed independently and correctly

## Milestone 7 — API Endpoints
- [x] GET /health returns {"status": "ok"}
- [x] POST /optimize-energy wires all 4 components together in order:
      LLM Interpreter → Guardrail Validator → Optimization Engine →
      Energy Validator → response
- [x] 422 returned cleanly for malformed request body
- [x] 502 returned cleanly if LLM is unavailable after retries
- [x] Integration test using the PDF's own GRID-101 example input,
      asserting response shape matches Section 5 exactly

## Milestone 8 — Docs & Deployment
- [x] README.md: how to run locally, how to set .env, curl examples
      for both endpoints using the GRID-101 example
- [x] Dockerfile builds and runs the app
- [ ] Deployed to Render or Railway, public URL confirmed working with
      a live curl test against /health and /optimize-energy

## Milestone 9 — Final Acceptance Check (must all be true before submission)
- [x] GET /health responds 200 with {"status":"ok"}
- [x] POST /optimize-energy on GRID-101 example returns valid
      directive_interpretation matching the note's intent
- [x] hourly_plan has exactly 24 entries, energy balance holds for all
- [x] total_cost is lower than a naive all-grid baseline (sanity check)
- [x] A deliberately malformed operator note does not crash the server
- [x] A deliberately malformed request body returns 422, not a 500

## Notes / Assumptions
- Project base path: c:/Users/HP/Desktop/Hackaton/GridWise-AI
- Cannot deploy to Render or Railway because no credentials or platform access are provided, so that item is left unchecked.
