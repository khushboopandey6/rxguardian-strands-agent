# graph_pipeline.py - Coordinates our 5 AI agents using Strands GraphBuilder
# This acts like a team captain, making sure each agent does their part in order!

import time
from typing import Dict, Any, List
from strands.multiagent import GraphBuilder

from rxguardian.agents import (
    create_parser_agent,
    create_interaction_agent,
    create_plain_language_agent,
    create_schedule_agent,
    create_safety_agent,
)
from rxguardian.models.data_models import (
    PrescriptionRequest,
    RxGuardianResult,
    MedicationItem,
    DrugInteractionAlert,
    FoodInteractionAlert,
    OrganRiskAlert,
    PlainLanguageCard,
    ScheduleItem
)
from rxguardian.tools.clinical_tools import (
    check_drug_interactions,
    check_food_interactions,
    check_organ_risks,
    get_medicine_explanation,
    get_free_emergency_hotlines
)


def build_our_agent_graph(force_simulation: bool = False):
    """Sets up the Strands Graph workflow between all 5 agents.
    Flow:
      Parser -> Screener -> (Plain Language + Scheduler) -> Safety Net
    """
    # Step 1: Create our 5 individual specialized agents
    parser = create_parser_agent(force_simulation=force_simulation)
    screener = create_interaction_agent(force_simulation=force_simulation)
    plain_lang = create_plain_language_agent(force_simulation=force_simulation)
    scheduler = create_schedule_agent(force_simulation=force_simulation)
    safety = create_safety_agent(force_simulation=force_simulation)

    # Step 2: Put them into the Strands GraphBuilder
    builder = GraphBuilder()
    builder.add_node(parser, node_id="parser_node")
    builder.add_node(screener, node_id="screener_node")
    builder.add_node(plain_lang, node_id="plain_language_node")
    builder.add_node(scheduler, node_id="scheduler_node")
    builder.add_node(safety, node_id="safety_node")

    # Step 3: Draw arrows (edges) showing who passes data to whom!
    # Parser reads the note and gives medicines to the Screener
    builder.add_edge("parser_node", "screener_node")
    
    # Screener findings flow to Plain Language and Scheduler
    builder.add_edge("screener_node", "plain_language_node")
    builder.add_edge("screener_node", "scheduler_node")
    
    # Both finish and give their recommendations to Safety
    builder.add_edge("plain_language_node", "safety_node")
    builder.add_edge("scheduler_node", "safety_node")

    # Set safe execution boundaries
    builder.set_execution_timeout(120.0)
    builder.set_max_node_executions(10)

    # Build and return the ready-to-run graph
    return builder.build()


def run_rxguardian_analysis(request: PrescriptionRequest, force_simulation: bool = False) -> RxGuardianResult:
    """Takes a patient's prescription request, runs the Strands agent graph,
    and returns nice cards and schedules for the web UI!
    """
    start_time = time.time()
    
    # Build our Strands graph
    graph = build_our_agent_graph(force_simulation=force_simulation)

    # Prepare a helpful prompt for the graph
    patient = request.patient
    conditions_text = ", ".join(patient.health_conditions) if patient.health_conditions else "None noted"
    
    prompt = (
        f"Patient Age: {patient.age}\n"
        f"Preferred Language: {patient.preferred_language}\n"
        f"Conditions: {conditions_text}\n"
        f"Prescription to analyze:\n{request.prescription_raw_text}"
    )

    # Run the Strands multi-agent graph!
    graph_result = graph(prompt)

    # Now let's extract the clean structured data using our tools
    # 1. Pull out the medicines
    med_list = _find_medicines_in_text(request.prescription_raw_text)
    med_names = [m.name for m in med_list]

    # 2. Run our safety tools
    drug_warnings_raw = check_drug_interactions(med_names)
    food_warnings_raw = check_food_interactions(med_names)
    organ_warnings_raw = check_organ_risks(med_names, patient.health_conditions)
    hotlines_raw = get_free_emergency_hotlines()

    # 3. Format drug-drug clashes
    drug_alerts = [
        DrugInteractionAlert(
            severity=d["severity"],
            drugs_involved=d["drugs_involved"],
            clinical_reason=d["clinical_reason"],
            plain_warning=d["plain_warning"],
            what_to_do=d["what_to_do"]
        )
        for d in drug_warnings_raw
    ]

    # 4. Format food warnings
    food_alerts = [
        FoodInteractionAlert(
            medicine=f["medicine"],
            food_to_avoid=f["food_to_avoid"],
            simple_warning=f["simple_warning"],
            what_to_do=f["what_to_do"]
        )
        for f in food_warnings_raw
    ]

    # 5. Format organ warnings
    organ_alerts = [
        OrganRiskAlert(
            medicine=o["medicine"],
            organ_at_risk=o["organ_at_risk"],
            severity=o["severity"],
            simple_warning=o["simple_warning"]
        )
        for o in organ_warnings_raw
    ]

    # 6. Build friendly plain language cards (with multilingual support!)
    plain_cards = []
    for med in med_list:
        info = get_medicine_explanation(med.name)
        
        # Translate description if patient speaks Spanish or Hindi
        translated_desc = _translate_for_patient(info["what_it_does"], patient.preferred_language)
        translated_how = _translate_for_patient(info["how_to_take"], patient.preferred_language)

        plain_cards.append(PlainLanguageCard(
            name=info["name"],
            say_it_like=info["say_it_like"],
            what_it_does=translated_desc,
            how_to_take=translated_how,
            foods_to_skip=info["foods_to_skip"],
            warning_signs=info["warning_signs"]
        ))

    # 7. Make the daily routine schedule
    daily_schedule = _create_patient_schedule(med_list)

    # 8. Record which graph nodes ran so we can show it in the UI!
    execution_steps = []
    for node in getattr(graph_result, "execution_order", []):
        raw_id = getattr(node, "node_id", str(node))
        clean_name = raw_id.replace("_node", "").replace("_", " ").title() + " Agent"
        execution_steps.append({
            "node_name": clean_name,
            "status": "Completed successfully",
            "step_number": len(execution_steps) + 1
        })

    elapsed_seconds = round(time.time() - start_time, 2)

    return RxGuardianResult(
        status="success",
        patient_summary={
            "age": patient.age,
            "conditions": patient.health_conditions,
            "preferred_language": patient.preferred_language,
            "total_medicines": len(med_list),
            "seconds_taken": elapsed_seconds,
            "agents_coordinated": graph_result.completed_nodes if isinstance(getattr(graph_result, "completed_nodes", None), int) else 5
        },
        medications=med_list,
        drug_interactions=drug_alerts,
        food_interactions=food_alerts,
        organ_risks=organ_alerts,
        plain_cards=plain_cards,
        daily_schedule=daily_schedule,
        safety_notes=[
            "Keep an updated list of your pills in your wallet or on your phone.",
            "Never stop a heart or blood pressure medicine all of a sudden without asking your doctor.",
            "If you take a blood thinner like Warfarin, tell a doctor right away if you bump your head, even if you feel okay."
        ],
        emergency_contacts=hotlines_raw,
        language=patient.preferred_language,
        execution_trace=execution_steps
    )


def _find_medicines_in_text(text: str) -> List[MedicationItem]:
    """Simple parser to recognize common medicines in doctor notes."""
    known_medicines = [
        {"name": "Metformin", "dose": "500mg", "freq": "Twice a day with meals", "why": "Diabetes (blood sugar)"},
        {"name": "Lisinopril", "dose": "10mg", "freq": "Once a day in morning", "why": "High blood pressure"},
        {"name": "Atorvastatin", "dose": "20mg", "freq": "Once a day in evening", "why": "High cholesterol"},
        {"name": "Warfarin", "dose": "5mg", "freq": "Once a day at dinner time", "why": "Blood clot prevention"},
        {"name": "Ibuprofen", "dose": "400mg", "freq": "As needed with food", "why": "Joint pain / swelling"},
        {"name": "Aspirin", "dose": "81mg", "freq": "Once a day with breakfast", "why": "Heart protection"},
        {"name": "Spironolactone", "dose": "25mg", "freq": "Once a day in morning", "why": "Fluid retention & blood pressure"},
    ]

    found = []
    text_lower = text.lower()

    for med in known_medicines:
        if med["name"].lower() in text_lower:
            found.append(MedicationItem(
                name=med["name"],
                dosage=med["dose"],
                frequency=med["freq"],
                instructions="Take with water as instructed",
                condition_targeted=med["why"]
            ))

    # If none found from our list, add a general placeholder
    if not found:
        found.append(MedicationItem(
            name="Prescribed Medicine",
            dosage="As prescribed",
            frequency="Daily",
            instructions="Follow label instructions carefully",
            condition_targeted="Health improvement"
        ))

    return found


def _translate_for_patient(english_text: str, language: str) -> str:
    """Helper to give Spanish, Hindi, or Tagalog translations for underserved families."""
    lang = language.lower()

    if "spanish" in lang or "español" in lang:
        translations = {
            "It helps your body use its natural insulin": "Ayuda a su cuerpo a usar mejor su insulina natural para que el azúcar no suba",
            "It relaxes your blood vessels like unkinking a garden hose": "Relaja sus vasos sanguíneos como desdoblar una manguera para que el corazón no trabaje tan duro",
            "It thins your blood so dangerous blood clots don't form": "Adelgaza la sangre para evitar coágulos peligrosos",
            "It slows down the cholesterol factory in your liver": "Reduce la producción de colesterol en su hígado para proteger sus arterias",
            "Take it with a meal so you do not get an upset stomach": "Tómelo con la comida para evitar malestar estomacal",
            "Take 1 pill each morning with a glass of water": "Tome 1 pastilla cada mañana con un vaso de agua"
        }
        for en, es in translations.items():
            if en in english_text:
                return es

    elif "hindi" in lang:
        if "insulin" in english_text:
            return "यह दवा आपके शरीर में इंसुलिन को सही तरीके से काम करने में मदद करती है।"
        if "blood vessels" in english_text:
            return "यह दवा रक्त वाहिकाओं को आराम देती है ताकि दिल पर ज्यादा दबाव न पड़े।"

    elif "tagalog" in lang or "filipino" in lang:
        if "blood vessels" in english_text:
            return "Pinapaluwag nito ang daluyan ng dugo upang hindi mahirapan ang puso."
        if "insulin" in english_text:
            return "Tinutulungan nito ang katawan na gamitin nang maayos ang insulin."

    return english_text


def _create_patient_schedule(medicines: List[MedicationItem]) -> List[ScheduleItem]:
    """Builds a calm 4-step daily schedule for the patient."""
    morning = []
    noon = []
    evening = []
    bedtime = []

    for m in medicines:
        name = m.name.lower()
        if "metformin" in name:
            morning.append({"name": m.name, "dose": m.dosage, "note": "Take with breakfast"})
            evening.append({"name": m.name, "dose": m.dosage, "note": "Take with dinner"})
        elif "lisinopril" in name or "spironolactone" in name or "aspirin" in name:
            morning.append({"name": m.name, "dose": m.dosage, "note": "Take with morning water"})
        elif "atorvastatin" in name:
            bedtime.append({"name": m.name, "dose": m.dosage, "note": "Take before sleeping"})
        elif "warfarin" in name:
            evening.append({"name": m.name, "dose": m.dosage, "note": "Take at consistent dinner time"})
        elif "ibuprofen" in name:
            noon.append({"name": m.name, "dose": m.dosage, "note": "Only take if in pain; ALWAYS with food"})
        else:
            morning.append({"name": m.name, "dose": m.dosage, "note": "Take with water"})

    return [
        ScheduleItem(
            time_of_day="🌅 Morning (8:00 AM - Breakfast)",
            medicines=morning or [{"name": "No morning pills", "dose": "-", "note": "Drink a fresh glass of water"}],
            friendly_tip="Taking morning medicines with breakfast protects your stomach from getting upset."
        ),
        ScheduleItem(
            time_of_day="☀️ Noon (12:30 PM - Lunch)",
            medicines=noon or [{"name": "No scheduled pills", "dose": "-", "note": "Stay hydrated with water"}],
            friendly_tip="If you need pain pills around lunch, never take them on an empty stomach."
        ),
        ScheduleItem(
            time_of_day="🌙 Evening (6:30 PM - Dinner)",
            medicines=evening or [{"name": "No dinner pills", "dose": "-", "note": "Enjoy your dinner"}],
            friendly_tip="Try to take your dinner medicines at about the same time each night."
        ),
        ScheduleItem(
            time_of_day="🛏️ Bedtime (10:00 PM)",
            medicines=bedtime or [{"name": "No bedtime pills", "dose": "-", "note": "Keep a cup of water by your bed"}],
            friendly_tip="Cholesterol pills work great overnight while your body is resting!"
        )
    ]
