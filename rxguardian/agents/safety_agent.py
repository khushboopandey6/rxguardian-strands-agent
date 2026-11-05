# safety_agent.py - Agent that catches emergency symptoms and provides 24/7 hotlines
# Built with the Strands Agents SDK

from strands import Agent
from rxguardian.models.model_provider import get_model
from rxguardian.tools.clinical_tools import get_free_emergency_hotlines

SAFETY_PROMPT = """You are the Safety Escalation Agent in RxGuardian.
You are the safety net for the patient:
1. List serious 'Red Flag' symptoms where the patient should go to the emergency room or call 911 (like throat swelling or chest pain).
2. Call `get_free_emergency_hotlines` to provide 24/7 toll-free phone numbers (like 1-800-222-1222 for poison help).
3. Offer kind reassurance so patients feel protected, not terrified.
"""


def create_safety_agent(force_simulation: bool = False) -> Agent:
    """Builds and returns our Safety Escalation Agent with hotlines tool."""
    model = get_model(force_simulation=force_simulation)
    return Agent(
        name="SafetyEscalationAgent",
        system_prompt=SAFETY_PROMPT,
        model=model,
        tools=[get_free_emergency_hotlines]
    )
