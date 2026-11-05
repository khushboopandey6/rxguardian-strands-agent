# interaction_agent.py - Agent that checks for dangerous clashes between medicines
# Equipped with our clinical tools so it can search our database

from strands import Agent
from rxguardian.models.model_provider import get_model
from rxguardian.tools.clinical_tools import (
    check_drug_interactions,
    check_food_interactions,
    check_organ_risks
)

SCREENER_PROMPT = """You are the Interaction Screener Agent in RxGuardian.
Your #1 priority is patient safety!
You look at the list of medicines and use your tools to catch dangers before they hurt the patient:
1. Call `check_drug_interactions` to see if two medicines clash.
2. Call `check_food_interactions` to see if grapefruit or spinach creates a problem.
3. Call `check_organ_risks` to see if a pill could harm a patient's kidneys, liver, or heart.

Always explain the danger in clear, caring words and suggest what the patient should ask their doctor.
"""


def create_interaction_agent(force_simulation: bool = False) -> Agent:
    """Builds and returns our Screener Agent with clinical tools attached."""
    model = get_model(force_simulation=force_simulation)
    return Agent(
        name="InteractionScreenerAgent",
        system_prompt=SCREENER_PROMPT,
        model=model,
        tools=[
            check_drug_interactions,
            check_food_interactions,
            check_organ_risks
        ]
    )
