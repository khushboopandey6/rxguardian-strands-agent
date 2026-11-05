# model_provider.py - Connects our agents to Amazon Bedrock or a local test runner
# Written by Khushboo for our hackathon project

import json
from typing import Any, AsyncGenerator, List, Optional
from pydantic import BaseModel

from strands.models import Model
from strands.types.streaming import StreamEvent
from rxguardian.config import (
    HAS_BEDROCK_CREDENTIALS,
    BEDROCK_MODEL_ID,
    AWS_REGION
)


class StudentTestModel(Model):
    """A simple test model so our project works even if judges or teachers
    run it on a laptop without AWS keys!
    It implements the required Strands Model functions: stream and structured_output.
    """

    def __init__(self, model_id: str = "student-bedrock-simulator"):
        self.model_id = model_id
        self.turn = 0

    def get_config(self) -> dict:
        return {"model_id": self.model_id, "streaming": True}

    def update_config(self, **kwargs: Any) -> None:
        pass

    async def structured_output(
        self, output_model: type[BaseModel], prompt: Any, system_prompt: Optional[str] = None, **kwargs: Any
    ) -> AsyncGenerator[dict[str, Any], None]:
        yield {"status": "ok"}

    async def stream(
        self,
        messages: Any,
        tool_specs: Optional[List[Any]] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncGenerator[StreamEvent, None]:
        """Streams responses chunk-by-chunk just like Amazon Bedrock does."""
        self.turn += 1
        system_text = (system_prompt or "").lower()

        # Check if the last turn was a tool result
        saw_tool_result = False
        for msg in messages:
            if isinstance(msg, dict) and msg.get("role") == "user":
                content = msg.get("content", [])
                if isinstance(content, list):
                    for blk in content:
                        if isinstance(blk, dict) and "toolResult" in blk:
                            saw_tool_result = True

        # If this agent has tools and hasn't called one yet, let's trigger a tool call!
        if tool_specs and not saw_tool_result and ("interaction" in system_text or "screener" in system_text):
            # Gather drug names mentioned in conversation
            history_str = " ".join([str(m) for m in messages]).lower()
            detected_meds = []
            for candidate in ["warfarin", "aspirin", "lisinopril", "metformin", "ibuprofen", "spironolactone", "atorvastatin"]:
                if candidate in history_str:
                    detected_meds.append(candidate.capitalize())
            
            if not detected_meds:
                detected_meds = ["Metformin", "Lisinopril", "Ibuprofen"]

            yield {"messageStart": {"role": "assistant"}}
            yield {
                "contentBlockStart": {
                    "start": {
                        "toolUse": {
                            "toolUseId": f"tool_step_{self.turn}",
                            "name": "check_drug_interactions"
                        }
                    }
                }
            }
            yield {
                "contentBlockDelta": {
                    "delta": {
                        "toolUse": {"input": json.dumps({"medications": detected_meds})}
                    }
                }
            }
            yield {"contentBlockStop": {}}
            yield {"messageStop": {"stopReason": "tool_use"}}
            return

        # Otherwise, write a friendly agent response for this role
        yield {"messageStart": {"role": "assistant"}}

        if "parser" in system_text:
            text = (
                "Hi! I am the Prescription Parser Agent.\n"
                "I read the doctor's note and identified 3 key medicines:\n"
                "1. Metformin 500mg (for diabetes)\n"
                "2. Lisinopril 10mg (for high blood pressure)\n"
                "3. Ibuprofen 400mg (for knee pain)\n"
                "I also noticed the patient has kidney concerns. Handing off to our Safety Screener!"
            )
        elif "screener" in system_text or "interaction" in system_text:
            text = (
                "Safety Alert from Screener Agent:\n"
                "I checked our clinical database and found an important warning!\n"
                "- Ibuprofen can hurt your kidneys and fight against Lisinopril.\n"
                "- It is much safer to ask your doctor for an alternative pain relief."
            )
        elif "plain" in system_text:
            text = (
                "Hello! I am the Plain Language Agent.\n"
                "I turned the complicated pharmacy leaflet into easy everyday English!\n"
                "- Metformin helps unlock insulin safely.\n"
                "- Lisinopril relaxes blood vessels like loosening a garden hose."
            )
        elif "schedule" in system_text:
            text = (
                "Daily Routine from Schedule Agent:\n"
                "Morning: Take Lisinopril and Metformin with breakfast.\n"
                "Evening: Take your second Metformin with dinner.\n"
                "Drink plenty of water throughout the day!"
            )
        elif "safety" in system_text:
            text = (
                "Emergency Guardrails from Safety Agent:\n"
                "If you ever feel dizzy or have swelling of your lips or face, call 911 immediately!\n"
                "For medicine overdose questions, free poison control is at 1-800-222-1222."
            )
        else:
            text = "RxGuardian analysis finished successfully! Reviewing all safety checks."

        yield {"contentBlockDelta": {"delta": {"text": text}}}
        yield {"contentBlockStop": {}}
        yield {"messageStop": {"stopReason": "end_turn"}}


def get_model(force_simulation: bool = False) -> Model:
    """Helper function to pick the right model.
    If you configured AWS Bedrock keys, it uses real Amazon Bedrock.
    Otherwise, it uses our student test model so the app never crashes!
    """
    if HAS_BEDROCK_CREDENTIALS and not force_simulation:
        try:
            from strands.models.bedrock import BedrockModel
            print(f"[Bedrock] Connecting to Amazon Bedrock: {BEDROCK_MODEL_ID} in {AWS_REGION}...")
            return BedrockModel(model_id=BEDROCK_MODEL_ID, region_name=AWS_REGION)
        except Exception as err:
            print(f"[Warning] Could not start BedrockModel ({err}). Falling back to student test model.")
            return StudentTestModel()
    else:
        # Running in student simulation mode
        return StudentTestModel()
