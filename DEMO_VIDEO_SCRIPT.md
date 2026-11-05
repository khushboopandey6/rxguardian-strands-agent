# RxGuardian: 3-Minute Video Demo Script
**Hackathon Submission Video for "Strands SDK: Workshop to Ship"**  
**Presenter:** Khushboo Pandey  
**Target Duration:** 2 minutes 45 seconds (Under 3 minutes requirement)

---

## Video Outline & Timestamp Guide

| Time | Screen Display | Voiceover Script |
| :--- | :--- | :--- |
| **0:00 - 0:30** | **Camera on Khushboo / Title Slide**<br>Display RxGuardian title: *"AI Health Equity with AWS Strands Agents SDK"* | "Hi everyone! My name is Khushboo, and this is RxGuardian — an AI prescription safety agent built with the AWS Strands Agents SDK.<br><br>Every year, over 1.5 million people suffer preventable harm from medication errors. Elderly patients taking multiple pills and families with limited English face the highest risk because pharmacy labels are filled with tiny print and confusing medical jargon. I built RxGuardian to solve this health equity challenge!" |
| **0:30 - 0:55** | **Switch to RxGuardian Web UI**<br>Point out clean layout, patient age, language dropdown, and 1-click preset buttons | "Here is the RxGuardian application. To make testing easy, I included one-click real-world scenarios. Let's select this scenario: a 72-year-old patient with Kidney Disease who was prescribed Metformin for diabetes and Lisinopril for high blood pressure, but is also taking over-the-counter Ibuprofen for knee pain." |
| **0:55 - 1:25** | **Click "Run Strands Agent Swarm"**<br>Highlight the 5 agent boxes on the left as they light up in real-time | "When I click 'Run Strands Agent Swarm', watch our 5 specialized Strands agents activate in sequence!<br><br>First, the **Prescription Parser Agent** extracts the active pills and dosages.<br>Next, the **Interaction Screener Agent** calls its Strands `@tool` functions to check our clinical database.<br>Then, the **Plain Language Agent** and **Schedule Planner** work in parallel, and finally, the **Safety Escalation Agent** verifies emergency guardrails. All in under one second!" |
| **1:25 - 1:55** | **Scroll through Results Panel**<br>Zoom into the Red Warning Banner & Clash Cards | "Look at the results! RxGuardian immediately detected two critical clashes:<br>First, **Lisinopril plus Ibuprofen**: the painkiller cancels out the blood pressure pill and places heavy stress on vulnerable kidneys.<br>Second, an **Organ Toxicity Warning** alerting that frequent Ibuprofen can cause acute kidney injury in Stage 3 CKD patients.<br>Instead of scary jargon, it gives the patient a gentle, actionable recommendation: ask their doctor about safer alternatives like Acetaminophen." |
| **1:55 - 2:20** | **Show Plain Language Cards & Click "Read Aloud"**<br>Demonstrate phonetic pronunciation and browser speech | "Now look at the Plain Language cards. Instead of 'antihypertensive ACE inhibitor', it explains: *'Relaxes blood vessels like unkinking a garden hose so your heart doesn't have to pump so hard.'*<br><br>And for low-vision patients, I built this accessible 'Read Aloud' button: *(Click Speak Button)*<br>*(Audio plays: 'Hello! Here is your RxGuardian safety summary. Important safety alert... Take Lisinopril in the morning...')*" |
| **2:20 - 2:45** | **Show Daily Calendar & Closing**<br>Show 4-block schedule and 24/7 hotlines | "Finally, RxGuardian organizes all pills into a clean 4-block daily calendar — Morning, Noon, Evening, and Bedtime — and embeds free 24/7 hotlines like Poison Control and 911.<br><br>RxGuardian proves that with AWS Strands Agents SDK and Amazon Bedrock, we can turn complex healthcare into an accessible, life-saving assistant for every family. Thank you!" |

---

## Recording Tips for Khushboo:
1. **Screen Recording:** Use QuickTime Player on your Mac (File -> New Screen Recording) or Loom.
2. **Audio:** Speak clearly and with a warm, caring tone.
3. **Pacing:** Keep it lively and under 3 minutes.
4. **YouTube / Loom Link:** Upload as Unlisted on YouTube or Loom and paste the link into your Builder Center submission!
