# data_models.py - Simple data shapes for our project
# We use Pydantic models so our inputs and outputs stay tidy and typed!

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# Information about the patient
class PatientProfile(BaseModel):
    age: int = Field(default=68, description="How old the patient is")
    preferred_language: str = Field(default="English", description="Language they feel most comfortable reading")
    health_conditions: List[str] = Field(default_factory=list, description="Conditions like Diabetes or Kidney Disease")
    allergies: List[str] = Field(default_factory=list, description="Medicines they are allergic to")


# One medicine item parsed from the doctor's note
class MedicationItem(BaseModel):
    name: str = Field(description="Name of the medicine")
    dosage: str = Field(description="Amount to take, e.g. 500mg or 1 tablet")
    frequency: str = Field(description="How often, e.g. Twice daily")
    instructions: str = Field(default="Take with water", description="Special notes like taking with food")
    condition_targeted: str = Field(default="", description="Why they are taking it")


# The request body sent by the web page
class PrescriptionRequest(BaseModel):
    prescription_raw_text: str = Field(description="The pasted doctor note or medicine list")
    patient: Optional[PatientProfile] = Field(default_factory=PatientProfile, description="Patient details")


# Warning about two medicines fighting each other
class DrugInteractionAlert(BaseModel):
    severity: str = Field(description="HIGH, MODERATE, or LOW")
    drugs_involved: List[str] = Field(description="The two medicines that clash")
    clinical_reason: str = Field(description="Why they clash")
    plain_warning: str = Field(description="Easy explanation for the patient")
    what_to_do: str = Field(description="Simple step the patient should take")


# Warning about food or drinks
class FoodInteractionAlert(BaseModel):
    medicine: str
    food_to_avoid: str
    simple_warning: str
    what_to_do: str


# Warning about organ safety (kidneys/liver/heart)
class OrganRiskAlert(BaseModel):
    medicine: str
    organ_at_risk: str
    severity: str
    simple_warning: str


# One row in our daily calendar schedule
class ScheduleItem(BaseModel):
    time_of_day: str  # Morning, Noon, Evening, Bedtime
    medicines: List[Dict[str, str]]
    friendly_tip: str


# Friendly card explaining one medicine
class PlainLanguageCard(BaseModel):
    name: str
    say_it_like: str
    what_it_does: str
    how_to_take: str
    foods_to_skip: List[str]
    warning_signs: List[str]


# Final package sent back to the browser
class RxGuardianResult(BaseModel):
    status: str = "success"
    patient_summary: Dict[str, Any]
    medications: List[MedicationItem]
    drug_interactions: List[DrugInteractionAlert]
    food_interactions: List[FoodInteractionAlert]
    organ_risks: List[OrganRiskAlert]
    plain_cards: List[PlainLanguageCard]
    daily_schedule: List[ScheduleItem]
    safety_notes: List[str]
    emergency_contacts: List[Dict[str, str]]
    language: str
    execution_trace: List[Dict[str, Any]]
