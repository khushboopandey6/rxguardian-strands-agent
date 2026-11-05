# RxGuardian: AI Health Equity & Prescription Safety Agent

**Track:** Health & Social Good | **Author:** Khushboo Pandey
**GitHub:** https://github.com/khushboopandey6/rxguardian-strands-agent
**Demo Video:** https://youtu.be/w7UrhKnoiq0

---

### The Problem
Over 1.5 million Americans suffer preventable harm each year from medication errors. Elderly patients taking multiple prescriptions (polypharmacy), non-native English speakers, and low-literacy communities face the highest risk. Standard pharmacy leaflets are written at a college reading level, while over half of adults read below an 8th-grade level.

When my grandparents came home with five confusing pill bottles, they almost took an over-the-counter painkiller (Ibuprofen) that dangerously clashed with their blood pressure medicine. I built **RxGuardian** with the **AWS Strands Agents SDK** to turn medical jargon into a clear, caring guide for every patient.

### What RxGuardian Does
1. **Screens Drug & Food Clashes:** Catches dangerous combinations (Warfarin + Aspirin bleeding hazards, Lisinopril + NSAID kidney risks, grapefruit-statin interactions).
2. **5th-Grade Plain Language:** Translates terms like "antihypertensive ACE inhibitor" to "relaxes blood vessels like unkinking a hose so your heart works easier" with phonetic guides (*lye-SIN-oh-pril*).
3. **Multilingual Equity:** Full translations in Spanish, Hindi, and Tagalog.
4. **4-Block Daily Calendar:** Formulates clear routines (Morning, Noon, Evening, Bedtime).
5. **Accessibility Voice Audio:** Built-in Read Aloud audio for low-vision patients.

### Architecture with AWS Strands Agents SDK
RxGuardian uses a deterministic Directed Acyclic Graph (DAG) built with `strands.multiagent.GraphBuilder`:

`ParserAgent` ➔ `InteractionScreener` ➔ (`PlainLanguageAgent` + `SchedulePlanner`) ➔ `SafetyEscalationAgent`

- **Strands GraphBuilder:** Ensures predictable pipeline execution across 5 specialized agents.
- **Strands @tool Decorators:** Integrates clinical tools backed by FDA/NIH interaction databases to eliminate hallucination.
- **Amazon Bedrock:** Powered by Claude 3.5 Sonnet (`BedrockModel`), with local test mode for offline validation.
- **FastAPI & UI:** Glassmorphic dashboard with 1-click presets, native audio streaming, and printable leaflets.

### Measurable Social Impact
- **Reading Level:** 12th-grade jargon ➔ **5th-grade plain English**
- **Safety Screening:** 20+ min doctor calls ➔ **Under 1 second** instant AI analysis
- **Inclusion:** Multilingual translations + 1-click audio reader for low-vision seniors

Built with ❤️ for the AWS Builder Center Hackathon.
