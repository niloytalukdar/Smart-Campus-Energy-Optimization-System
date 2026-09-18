import json
import time
import os
from typing import List, Dict
import openai
from app.config import OPENAI_API_KEY

class LLMParseError(Exception):
    pass

class LLMUnavailableError(Exception):
    pass

SYSTEM_PROMPT = """You convert campus energy-operator notes into strict JSON directives.
You will be given a list of plain-language notes. For each note,
output one directive object. A note may sometimes map to zero
directives if it carries no actionable energy instruction — in that
case, skip it.

Each directive object must have exactly these fields:
- directive_type: one of
  ["solar_reduction","solar_outage","no_charge_window",
   "no_discharge_window","demand_increase","demand_decrease"]
- hours: array of integers 0-23 that the directive applies to
- factor: a number between 0 and 1 for solar_reduction/demand_decrease,
  a number greater than 1 for demand_increase, or null for the window
  types (no_charge_window, no_discharge_window, solar_outage)

Respond with ONLY a JSON array of directive objects. No prose, no
markdown code fences, no explanation — the response must be valid
JSON and nothing else, because it will be parsed directly."""

def _call_openai_with_retry(messages: List[Dict]) -> str:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    retries = [1, 2]
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=1024,
                temperature=0.1,
                messages=messages,
                timeout=10.0
            )
            return response.choices[0].message.content
        except (openai.APIConnectionError, openai.InternalServerError, openai.RateLimitError, openai.APITimeoutError) as e:
            if attempt < 2:
                time.sleep(retries[attempt])
            else:
                raise LLMUnavailableError(f"OpenAI API unavailable after retries: {str(e)}")
        except Exception as e:
            if attempt < 2:
                time.sleep(retries[attempt])
            else:
                raise LLMUnavailableError(f"OpenAI API unavailable after retries: {str(e)}")

def interpret_notes(operator_notes: List[str]) -> List[dict]:
    return _local_interpret(operator_notes)


def _local_interpret(operator_notes: List[str]) -> List[dict]:
    """Very small rule-based interpreter for local development.
    It detects percent-based solar reductions and no-charge windows using simple regexes.
    """
    import re
    directives = []
    for note in operator_notes:
        n = note.lower()
        # percent pattern
        pct_m = re.search(r"(\d{1,3})%", n)
        nums = re.findall(r"\b(1[0-9]|2[0-3]|[0-9])\b", n)

        # no-charge window
        if "no charge" in n or "do not charge" in n or "no-charge" in n:
            hours = []
            if len(nums) >= 2:
                a = int(nums[0])
                b = int(nums[1])
                if a <= b:
                    hours = list(range(a, b + 1))
                else:
                    hours = list(range(a, 24)) + list(range(0, b + 1))
            directives.append({
                "directive_type": "no_charge_window",
                "hours": hours,
                "factor": None,
                "structured_adjustment": {"hours": hours}
            })
            continue

        # solar reduction
        if pct_m and ("solar" in n or "sun" in n or "panel" in n):
            factor = float(pct_m.group(1)) / 100.0
            hours = []
            if len(nums) >= 2:
                a = int(nums[0])
                b = int(nums[1])
                if a <= b:
                    hours = list(range(a, b + 1))
                else:
                    hours = list(range(a, 24)) + list(range(0, b + 1))
            else:
                # default to midday hours if none found
                hours = [13, 14, 15]
            directives.append({
                "directive_type": "solar_reduction",
                "hours": hours,
                "factor": factor,
                "structured_adjustment": {"hours": hours, "factor": factor}
            })
            continue

        # fallback: no directive
    return directives
