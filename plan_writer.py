"""
Agent 3 — Plan Writer
Takes the curated resource pack and writes a realistic,
week-by-week 30-day kickstart learning plan.
"""
from llm import call_gemini

SYSTEM_PROMPT = """You are the Plan Writer agent for a language learning assistant.

You will receive:
1. A target language and the learner's current level
2. A curated pack of 3 best-fit learning resources

Your job:
- Create a realistic, motivating 30-day kickstart plan
- Assume 20–30 minutes of study per day (beginner-friendly)
- Structure it as 4 weekly blocks, each with a clear focus theme
- Each week: state the focus, then list 3 daily actions using the curated resources
- Keep it simple, actionable, and encouraging

Format:
## 🗓️ Your 30-Day {Language} Kickstart Plan

### Week 1 — [Focus Theme]
**Daily actions (20–30 min):**
- Action 1 using [resource name]
- Action 2
- Action 3

### Week 2 — [Focus Theme]
...and so on for weeks 3 and 4.

End with a short "Stay Consistent" tip.
"""

def plan_writer_agent(language: str, level: str, curated_resources: str) -> str:
    """
    Generate a 30-day study plan from the curated resources.
    """
    user_message = f"""Target language: {language}
Level: {level}

Curated resource pack:
{curated_resources}

Please write the 30-day kickstart plan."""

    return call_gemini(SYSTEM_PROMPT, user_message)
