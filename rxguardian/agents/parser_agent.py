# parser_agent.py - Agent that reads messy doctor notes and pulls out the medicines
# Built using the AWS Strands Agent SDK

from strands import Agent
from rxguardian.models.model_provider import get_model

# Instructions for our parser agent in simple English
PARSER_PROMPT = """You are the Prescription Parser Agent in RxGuardian.
Your job is to read messy doctor notes, hospital discharge papers, or pill lists, and clearly find:
1. The names of the medicines (like Metformin or Lisinopril).
2. The dose (like 500mg or 1 pill).
3. How often to take it (like twice a day).
4. Any patient conditions mentioned (like kidney disease or diabetes).

Be careful and never invent medicines that were not written down!
"""


def create_parser_agent(force_simulation: bool = False) -> Agent:
    """Builds and returns our Prescription Parser Agent."""
    model = get_model(force_simulation=force_simulation)
    return Agent(
        name="PrescriptionParserAgent",
        system_prompt=PARSER_PROMPT,
        model=model,
    )
