# app.py - FastAPI web server for RxGuardian
# Connects our Strands AI agents to our user-friendly web page

import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from rxguardian.models.data_models import PrescriptionRequest, RxGuardianResult
from rxguardian.workflows.graph_pipeline import run_rxguardian_analysis
from rxguardian.config import PORT, HOST

# Create our web app
app = FastAPI(
    title="RxGuardian - AI Prescription Safety Agent",
    description="Built for AWS Builder Center Hackathon with Strands Agents SDK",
    version="1.0.0"
)

# Folder where our HTML, CSS, and JS files live
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.api_route("/", methods=["GET", "HEAD"])
def home_page():
    """Serves the main web application page."""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/api/health")
def health_check():
    """Simple check to make sure the server is healthy and alive."""
    return {"status": "healthy", "project": "RxGuardian", "agent_sdk": "AWS Strands Agents SDK"}


@app.get("/api/presets")
def get_sample_prescriptions():
    """Returns sample real-world prescription cases for judges and visitors to try with 1 click!"""
    return [
        {
            "id": "senior_kidney",
            "title": "Elderly Patient with Kidney Disease & Polypharmacy",
            "description": "72yo patient with Stage 3 Chronic Kidney Disease taking blood pressure and diabetes meds, plus over-the-counter Ibuprofen for knee pain.",
            "language": "English",
            "age": 72,
            "conditions": ["Chronic Kidney Disease (CKD)", "Hypertension", "Type 2 Diabetes"],
            "raw_text": "Rx: Metformin 500mg PO BID with meals. Lisinopril 10mg PO daily in AM. Patient also taking OTC Ibuprofen (Advil) 400mg TID PRN for severe knee osteoarthritis."
        },
        {
            "id": "warfarin_blood_thinner",
            "title": "Blood Thinner & Clot Prevention Hazard",
            "description": "68yo post-DVT patient on Warfarin who was also advised to take Baby Aspirin by a neighbor, plus eats inconsistent dark leafy salads.",
            "language": "English",
            "age": 68,
            "conditions": ["Deep Vein Thrombosis (DVT)", "Atrial Fibrillation"],
            "raw_text": "Warfarin 5mg daily at 6pm. Aspirin 81mg daily. Patient reports eating spinach and kale salad frequently. High bruising noted on arms."
        },
        {
            "id": "spanish_hypertension",
            "title": "Spanish-Speaking Patient with High Blood Pressure & Statin",
            "description": "64yo native Spanish speaker taking Lisinopril and Atorvastatin, loves drinking fresh grapefruit juice every morning.",
            "language": "Spanish",
            "age": 64,
            "conditions": ["Hypertension", "High Cholesterol"],
            "raw_text": "Lisinopril 10mg diario por la mañana. Atorvastatin 20mg por la noche. El paciente bebe jugo de toronja (grapefruit juice) natural todos los días."
        }
    ]


@app.post("/api/analyze", response_model=RxGuardianResult)
def analyze_prescription(request: PrescriptionRequest):
    """Main API endpoint called by our web page.
    Runs the 5 Strands AI agents in our graph pipeline and returns the result!
    """
    try:
        # Run our Strands pipeline!
        result = run_rxguardian_analysis(request)
        return result
    except Exception as err:
        print(f"[Error] Failed to analyze prescription: {err}")
        raise HTTPException(status_code=500, detail=str(err))
