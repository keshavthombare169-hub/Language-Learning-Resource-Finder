"""
Agent 2 — Curator
Reads Agent 1's resource list and picks the 3 best for the learner's level,
explaining the reasoning for each choice.
"""
from llm import call_gemini

SYSTEM_PROMPT = """You are the Curator agent for a language learning assistant.

You will receive:
1. A target language and level
2. A list of 6 resources found by the Resource Finder agent

Your job:
- Select the 3 BEST resources that are most appropriate for this exact level
- For each chosen resource, explain in 2 sentences WHY it's the best fit for this learner
- End with a one-line "Your Pack Summary" that motivates the learner

Format:
### Your Curated Pack

**1. [Resource Name]**
Why it's perfect for you: [2 sentences]

**2. [Resource Name]**
Why it's perfect for you: [2 sentences]

**3. [Resource Name]**
Why it's perfect for you: [2 sentences]

---
**Your Pack Summary:** [One motivating sentence]
"""

def curator_agent(language: str, level: str, resources: str) -> str:
    """
    Pick the 3 best resources from the finder's output.
    """
    user_message = f"""Target language: {language}
Level: {level}

Resources found by the Resource Finder agent:
{resources}

Please select and explain the 3 best resources for this learner."""

    return call_gemini(SYSTEM_PROMPT, user_message)
