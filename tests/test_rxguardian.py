# test_rxguardian.py - Automated tests for RxGuardian
# Written by Khushboo to test our tools, agents, and graph pipeline!

import unittest
from rxguardian.tools.clinical_tools import (
    check_drug_interactions,
    check_food_interactions,
    check_organ_risks,
    get_medicine_explanation,
    get_free_emergency_hotlines
)
from rxguardian.models.data_models import PrescriptionRequest, PatientProfile
from rxguardian.workflows.graph_pipeline import run_rxguardian_analysis


class TestRxGuardian(unittest.TestCase):
    """Test suite to make sure our medicine safety checks work properly."""

    def test_warfarin_aspirin_clash(self):
        """Test that Warfarin and Aspirin trigger a HIGH risk bleeding warning."""
        meds = ["Warfarin 5mg", "Aspirin 81mg"]
        results = check_drug_interactions(meds)
        self.assertTrue(len(results) >= 1)
        self.assertEqual(results[0]["severity"], "HIGH")
        self.assertIn("warfarin", results[0]["drugs_involved"])
        self.assertIn("aspirin", results[0]["drugs_involved"])

    def test_lisinopril_ibuprofen_clash(self):
        """Test that Lisinopril and Ibuprofen clash is flagged."""
        meds = ["Lisinopril 10mg", "Ibuprofen 400mg"]
        results = check_drug_interactions(meds)
        self.assertTrue(len(results) >= 1)
        self.assertIn("lisinopril", results[0]["drugs_involved"])

    def test_grapefruit_interaction(self):
        """Test that grapefruit juice warning is triggered for statins."""
        meds = ["Atorvastatin 40mg"]
        warnings = check_food_interactions(meds)
        self.assertTrue(len(warnings) >= 1)
        self.assertIn("Grapefruit", warnings[0]["food_to_avoid"])

    def test_kidney_disease_organ_risk(self):
        """Test that Ibuprofen is flagged as dangerous for kidney patients."""
        meds = ["Ibuprofen 400mg"]
        conditions = ["Chronic Kidney Disease (CKD)"]
        risks = check_organ_risks(meds, conditions)
        self.assertTrue(len(risks) >= 1)
        self.assertEqual(risks[0]["organ_at_risk"], "Kidneys")

    def test_medicine_plain_explanation(self):
        """Test that we get easy 5th-grade explanation cards."""
        info = get_medicine_explanation("Metformin")
        self.assertIn("insulin", info["what_it_does"].lower())
        self.assertIn("met-for-min", info["say_it_like"].lower())

    def test_emergency_hotlines(self):
        """Test that 24/7 emergency hotlines like 911 and Poison Control exist."""
        hotlines = get_free_emergency_hotlines()
        phones = [h["phone"] for h in hotlines]
        self.assertIn("911", phones)
        self.assertIn("1-800-222-1222", phones)

    def test_full_graph_pipeline(self):
        """Test that the entire 5-agent Strands graph runs from end to end."""
        req = PrescriptionRequest(
            prescription_raw_text="Metformin 500mg BID and Lisinopril 10mg daily. Patient takes Ibuprofen for back pain.",
            patient=PatientProfile(
                age=70,
                preferred_language="English",
                health_conditions=["Kidney disease", "Hypertension"],
                allergies=[]
            )
        )
        res = run_rxguardian_analysis(req)
        self.assertEqual(res.status, "success")
        self.assertTrue(len(res.medications) >= 2)
        self.assertTrue(len(res.daily_schedule) == 4)
        self.assertTrue(len(res.emergency_contacts) >= 3)
        self.assertGreaterEqual(res.patient_summary["agents_coordinated"], 5)


if __name__ == "__main__":
    unittest.main()
