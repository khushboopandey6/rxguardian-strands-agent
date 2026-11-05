# plain_language_agent.py - Agent that translates medical jargon into 5th-grade English
# It helps families and grandparents understand their pill bottles easily!

from strands import Agent
from rxguardian.models.model_provider import get_model
from rxguardian.tools.clinical_tools import get_medicine_explanation

PLAIN_LANGUAGE_PROMPT = """You are the Plain Language Agent in RxGuardian.
Doctors often use big medical words that can confuse regular people and make them scared.
Your job is to make health information friendly and super easy to read:
1. Use simple 5th-grade words that anyone in middle school or high school can understand.
2. Teach them how to pronounce the pill name phonetically (like Lisinopril -> lye-SIN-oh-pril).
3. Explain what the pill does using everyday analogies (like 'relaxing your blood vessels like unkinking a hose').
4. If the patient prefers Spanish, Hindi, or Tagalog, provide the translation so their whole family understands.
"""


def create_plain_language_agent(force_simulation: bool = False) -> Agent:
    """Builds and returns our Plain Language Agent with explanation tools."""
    model = get_model(force_simulation=force_simulation)
    return Agent(
        name="PlainLanguageAgent",
        system_prompt=PLAIN_LANGUAGE_PROMPT,
        model=model,
        tools=[get_medicine_explanation]
    )
