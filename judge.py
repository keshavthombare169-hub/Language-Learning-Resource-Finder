"""
LLM-as-Judge
Evaluates the full agent output against a defined rubric.
Returns structured JSON scores + a verdict.

Rubric:
  1. Resource Quality   (0–100) — Are resources well-matched to level?
  2. Plan Structure     (0–100) — Is the 30-day plan realistic and clear?
  3. Personalization    (0–100) — How well tailored to this specific learner?
"""
import json
import re
from llm import call_gemini

SYSTEM_PROMPT = """You are an impartial LLM-as-Judge evaluating a language learning assistant's output.

Rubric — score each dimension 0–100:
1. resource_quality: Are the curated resources appropriate, high-quality, and well-matched to the learner's level?
2. plan_structure: Is the 30-day plan realistic (20–30 min/day), clearly structured, and actionable?
3. personalization: How well does the output address the specific language and level requested?

Also provide:
- verdict: One sentence overall judgment.
- improvements: A list of 2–3 concrete suggestions to improve the output.

You MUST respond with ONLY valid JSON. No markdown fences, no extra text.

Example format:
{
  "rubric": {
    "resource_quality": 85,
    "plan_structure": 78,
    "personalization": 90
  },
  "verdict": "Strong output with well-matched resources and a clear weekly structure.",
  "improvements": [
    "Add grammar-focused resources for the intermediate stage.",
    "Include time estimates per activity in the weekly plan."
  ]
}
"""

def judge_agent(language: str, level: str, curated: str, plan: str) -> dict:
    """
    Run the LLM-as-Judge and return a parsed dict with rubric scores.
    Falls back to default scores if JSON parsing fails.
    """
    user_message = f"""Evaluate this language learning assistant output:

Language: {language}
Level: {level}

--- Curated Resource Pack ---
{curated}

--- 30-Day Plan ---
{plan}

Score according to the rubric and return only valid JSON."""

    raw = call_gemini(SYSTEM_PROMPT, user_message)

    # Strip any accidental markdown fences
    clean = re.sub(r"```(?:json)?|```", "", raw).strip()

    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        # Graceful fallback — try to extract numbers with regex
        scores = re.findall(r'"(\w+)":\s*(\d+)', clean)
        rubric = {k: int(v) for k, v in scores if k in ("resource_quality", "plan_structure", "personalization")}
        return {
            "rubric": rubric or {"resource_quality": 75, "plan_structure": 75, "personalization": 75},
            "verdict": "Evaluation completed (could not fully parse judge response).",
            "improvements": ["Review output manually for further quality checks."]
        }
