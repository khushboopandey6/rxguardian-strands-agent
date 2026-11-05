# clinical_tools.py - Python tools decorated with @tool for Strands Agents
# These functions let our AI agents search through our medicine safety rules!

from typing import List, Dict, Any
from strands import tool

from rxguardian.tools.clinical_db import (
    DRUG_INTERACTIONS,
    FOOD_INTERACTIONS,
    ORGAN_WARNINGS,
    MEDICINE_INFO
)


@tool
def check_drug_interactions(medications: List[str]) -> List[Dict[str, Any]]:
    """Checks if any of the patient's medicines clash or cause dangerous interactions when taken together.
    
    Args:
        medications: List of medicine names like ['Warfarin', 'Aspirin', 'Metformin'].
        
    Returns:
        List of warning cards explaining what clashes and what the patient should do.
    """
    # Lowercase everything so we don't miss matches because of capital letters
    clean_meds = [m.lower().strip() for m in medications]
    warnings_found = []

    # Loop through our known bad combinations
    for rule in DRUG_INTERACTIONS:
        pair = rule["drugs"]
        # Check if both drugs from the rule are in the patient's prescription list
        has_first = any(pair[0] in m for m in clean_meds)
        has_second = any(pair[1] in m for m in clean_meds)

        if has_first and has_second:
            warnings_found.append({
                "severity": rule["severity"],
                "drugs_involved": pair,
                "clinical_reason": rule["why_it_happens"],
                "plain_warning": rule["simple_warning"],
                "what_to_do": rule["what_to_do"]
            })

    return warnings_found


@tool
def check_food_interactions(medications: List[str]) -> List[Dict[str, Any]]:
    """Checks if any common foods or drinks (like grapefruit juice or spinach) interfere with these medicines.
    
    Args:
        medications: List of medicine names.
        
    Returns:
        List of foods to avoid and why.
    """
    clean_meds = [m.lower().strip() for m in medications]
    food_warnings = []

    # Loop through each food warning rule
    for rule in FOOD_INTERACTIONS:
        for med_name in clean_meds:
            if any(k in med_name for k in rule["medicines"]):
                food_warnings.append({
                    "medicine": med_name.capitalize(),
                    "food_to_avoid": rule["food"],
                    "simple_warning": rule["simple_warning"],
                    "what_to_do": rule["what_to_do"]
                })
                break  # Don't add duplicate warnings for the same rule

    return food_warnings


@tool
def check_organ_risks(medications: List[str], health_conditions: List[str]) -> List[Dict[str, Any]]:
    """Checks if any medicine could hurt the patient's existing health conditions (like kidneys or liver).
    
    Args:
        medications: List of medicine names.
        health_conditions: Existing conditions like ['Kidney disease', 'High blood pressure'].
        
    Returns:
        List of organ safety warnings.
    """
    clean_meds = [m.lower().strip() for m in medications]
    clean_conditions = [c.lower().strip() for c in health_conditions]
    organ_alerts = []

    for rule in ORGAN_WARNINGS:
        # Check if the patient has this condition
        has_condition = any(any(k in c for k in rule["condition_keywords"]) for c in clean_conditions)

        if has_condition:
            # Check if they are taking any medicine that is bad for this condition
            for med_name in clean_meds:
                if any(bad in med_name for bad in rule["bad_medicines"]):
                    organ_alerts.append({
                        "medicine": med_name.capitalize(),
                        "organ_at_risk": rule["organ"],
                        "severity": rule["severity"],
                        "simple_warning": rule["simple_warning"]
                    })

    return organ_alerts


@tool
def get_medicine_explanation(medicine_name: str) -> Dict[str, Any]:
    """Gets an easy-to-understand explanation of a medicine with pronunciation and what it does.
    
    Args:
        medicine_name: Name of the pill or liquid.
        
    Returns:
        Friendly explanation card for the patient.
    """
    name_clean = medicine_name.lower().strip()

    # Search our dictionary for this medicine
    for key, info in MEDICINE_INFO.items():
        if key in name_clean:
            return info

    # If it's a medicine we don't have in our dictionary, give a nice default card
    return {
        "name": medicine_name.capitalize(),
        "say_it_like": medicine_name,
        "what_it_does": "Prescribed by your doctor to help you feel better and stay healthy.",
        "how_to_take": "Take regularly with a full glass of water exactly as written on the bottle.",
        "foods_to_skip": ["Avoid alcohol unless approved by your doctor"],
        "warning_signs": ["Sudden rash, hives, or swelling of your face or throat"]
    }


@tool
def get_free_emergency_hotlines() -> List[Dict[str, str]]:
    """Returns free 24/7 phone numbers patients can call for urgent help or questions.
    
    Returns:
        List of verified hotline numbers and descriptions.
    """
    return [
        {
            "name": "Emergency Medical Services",
            "phone": "911",
            "hours": "24/7",
            "when_to_call": "Call right away if having chest pain, difficulty breathing, or sudden face/throat swelling."
        },
        {
            "name": "Poison Help & Medicine Overdose",
            "phone": "1-800-222-1222",
            "hours": "24/7/365 (Free)",
            "when_to_call": "Talk to a real pharmacist or nurse if you took the wrong pill or double-dosed."
        },
        {
            "name": "Crisis & Mental Health Lifeline",
            "phone": "Call or Text 988",
            "hours": "24/7 (Free in 200+ languages)",
            "when_to_call": "Free emotional support and guidance during stressful health moments."
        },
        {
            "name": "Medicine Cost Assistance Hotline",
            "phone": "1-888-477-2669",
            "hours": "Mon-Fri 9am-5pm EST",
            "when_to_call": "Helps people without good insurance get prescriptions for free or low cost."
        }
    ]
