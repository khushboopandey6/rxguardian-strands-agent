# main.py - Main entry point to launch RxGuardian
# Written by Khushboo for the AWS Builder Center Hackathon
# You can run either the web server or the quick command-line demo!

import sys
import uvicorn
from rxguardian.config import PORT, HOST
from rxguardian.models.data_models import PrescriptionRequest, PatientProfile
from rxguardian.workflows.graph_pipeline import run_rxguardian_analysis


def run_cli_demo():
    """Runs a quick demo in the terminal to show how our Strands agents work!"""
    print("\n" + "=" * 65)
    print("  RxGuardian - AI Health Equity & Prescription Safety Agent")
    print("  Powered by AWS Strands Agents SDK")
    print("=" * 65 + "\n")

    sample_text = (
        "Patient: 72yo with Chronic Kidney Disease.\n"
        "Prescriptions: Metformin 500mg BID, Lisinopril 10mg daily in AM.\n"
        "Patient also taking OTC Ibuprofen 400mg TID for knee arthritis."
    )

    print("Analyzing Sample Prescription:\n", sample_text)
    print("\nRunning Strands Multi-Agent Graph...")

    req = PrescriptionRequest(
        prescription_raw_text=sample_text,
        patient=PatientProfile(
            age=72,
            preferred_language="English",
            health_conditions=["Chronic Kidney Disease", "Hypertension", "Type 2 Diabetes"],
            allergies=[]
        )
    )

    result = run_rxguardian_analysis(req)

    print("\n" + "-" * 50)
    print("  ANALYSIS RESULTS FROM STRANDS AGENTS")
    print("-" * 50)
    print(f"Time Taken: {result.patient_summary['seconds_taken']}s")
    print(f"Agents Coordinated: {result.patient_summary['agents_coordinated']}")

    print("\n[!] DANGEROUS DRUG CLASHES DETECTED:")
    for d in result.drug_interactions:
        print(f"  • {d.drugs_involved[0].upper()} + {d.drugs_involved[1].upper()} ({d.severity} RISK)")
        print(f"    Warning: {d.plain_warning}")
        print(f"    Action:  {d.what_to_do}\n")

    print("[!] ORGAN TOXICITY WARNINGS:")
    for o in result.organ_risks:
        print(f"  • {o.medicine} vs {o.organ_at_risk}: {o.simple_warning}")

    print("\n[+] DAILY MEDICINE ROUTINE:")
    for s in result.daily_schedule:
        pills = ", ".join([f"{p['name']} ({p['dose']})" for p in s.medicines])
        print(f"  • {s.time_of_day}: {pills}")

    print("\n[+] 24/7 FREE SUPPORT HOTLINES:")
    for h in result.emergency_contacts:
        print(f"  • {h['name']}: {h['phone']} ({h['hours']})")

    print("\n" + "=" * 65)
    print("CLI Demo completed successfully! To start the web UI, run: python main.py")
    print("=" * 65 + "\n")


def start_web_server():
    """Starts the FastAPI web server so users can use the nice UI in their browser."""
    print("\n" + "=" * 65)
    print("  Starting RxGuardian Web Server on:")
    print(f"  http://localhost:{PORT}")
    print("  Press Ctrl+C to stop.")
    print("=" * 65 + "\n")
    uvicorn.run("rxguardian.web.app:app", host=HOST, port=PORT, reload=False)


if __name__ == "__main__":
    # If user passed --cli, run terminal mode
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli_demo()
    else:
        # Default: launch the web server
        start_web_server()
