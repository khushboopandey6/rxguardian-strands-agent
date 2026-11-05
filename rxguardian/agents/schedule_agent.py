# schedule_agent.py - Agent that plans an easy daily routine for pills
# It stops people from forgetting their doses or accidentally taking them twice

from strands import Agent
from rxguardian.models.model_provider import get_model

SCHEDULE_PROMPT = """You are the Schedule Planner Agent in RxGuardian.
Taking lots of pills can be confusing. Your goal is to make a calm, simple daily schedule:
1. Divide the day into 4 friendly time blocks:
   - Morning (Breakfast time ~8 AM)
   - Noon (Lunch time ~12:30 PM)
   - Evening (Dinner time ~6:30 PM)
   - Bedtime (Around 10 PM)
2. Pair pills with food when needed so patients don't get an upset stomach.
3. Make sure medicines that don't like each other are spaced out safely.
"""


def create_schedule_agent(force_simulation: bool = False) -> Agent:
    """Builds and returns our Schedule Planner Agent."""
    model = get_model(force_simulation=force_simulation)
    return Agent(
        name="SchedulePlannerAgent",
        system_prompt=SCHEDULE_PROMPT,
        model=model,
    )
