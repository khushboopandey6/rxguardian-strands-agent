# RxGuardian 💊🛡️
### AI Health Equity & Prescription Safety Agent
**Built with the AWS Strands Agents SDK for Social Good**  
**Author:** Khushboo Pandey  
**Hackathon:** AWS Builder Center — *Strands SDK: Workshop to Ship*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Strands](https://img.shields.io/badge/AWS%20Strands%20SDK-v1.64-orange.svg)](https://github.com/strands-agents/harness-sdk)
[![Demo Video](https://img.shields.io/badge/Demo%20Video-YouTube-red.svg)](https://youtu.be/w7UrhKnoiq0)
[![Tests](https://img.shields.io/badge/Tests-100%25%20Passing-brightgreen.svg)]()
[![Social Good](https://img.shields.io/badge/Track-Health%20Equity-teal.svg)]()

> 📺 **Watch the Demo Video on YouTube:** [https://youtu.be/w7UrhKnoiq0](https://youtu.be/w7UrhKnoiq0)

---

## 🌟 What is RxGuardian?

**RxGuardian** is an AI agent system that helps protect elderly patients, non-English speaking immigrant families, and low-literacy communities from preventable prescription errors.

Every year, **over 1.5 million people** are harmed by taking medicines that clash with each other or by misunderstanding confusing medical leaflets. RxGuardian uses a team of **5 specialized AI agents coordinated by the AWS Strands Agents SDK** to:
1. **Detect Dangerous Drug & Food Clashes:** Catches when two pills fight against each other or when foods like grapefruit turn cholesterol medicine into an accidental overdose!
2. **Translate Medical Jargon to 5th-Grade Language:** Replaces scary words with simple, caring explanations and phonetic pronunciation guides (e.g. *Lisinopril -> lye-SIN-oh-pril*).
3. **Support Multilingual Families:** Offers translations in Spanish, Hindi, and Tagalog.
4. **Organize a 4-Block Daily Calendar:** Tells patients exactly which pills to take in the Morning, at Noon, in the Evening, and at Bedtime.
5. **Provide Low-Vision "Read Aloud" Audio:** Reads directions aloud with one click so visually impaired seniors don't have to strain their eyes on tiny bottles.

---

## 🤖 Multi-Agent Architecture (Strands GraphBuilder)

Rather than using a single AI prompt, RxGuardian uses a deterministic **Directed Acyclic Graph (DAG)** built with `strands.multiagent.GraphBuilder`:

```
               [Raw Doctor Note / Prescription]
                              │
                              ▼
                 ┌─────────────────────────┐
                 │ PrescriptionParserAgent │
                 │ (Pulls out meds & dose) │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │ InteractionScreener     │
                 │ (Executes safety @tools)│
                 └──────┬───────────┬──────┘
                        │           │
             ┌──────────▼──┐     ┌──▼──────────────┐
             │PlainLanguage│     │ SchedulePlanner │
             │(5th-grade   │     │ (Chronotherapy  │
             │ translation)│     │  calendar)      │
             └──────────┬──┘     └──┬──────────────┘
                        │           │
                        └─────┬─────┘
                              ▼
                 ┌─────────────────────────┐
                 │ SafetyEscalationAgent   │
                 │ (Emergency hotlines 911)│
                 └─────────────────────────┘
```

### Strands SDK Features Used:
- **`strands.multiagent.GraphBuilder`**: Deterministic multi-agent sequencing with typed graph results.
- **`@tool` Decorators**: Clinical search tools (`check_drug_interactions`, `check_food_interactions`, `check_organ_risks`, `get_free_emergency_hotlines`).
- **Amazon Bedrock (`BedrockModel`)**: Seamless connection to Anthropic Claude 3.5 Sonnet on Amazon Bedrock.
- **Student Simulation Mode**: Intelligent local fallback so anyone can test the code without needing active AWS cloud billing!

---

## 🚀 Quick Start (Running Locally)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/rxguardian-strands-agent.git
cd rxguardian-strands-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Configure AWS Bedrock
If you want to use live Amazon Bedrock, copy `.env.example` to `.env` and add your AWS credentials:
```bash
cp .env.example .env
```
*(If you don't have AWS credentials, don't worry! RxGuardian will automatically use our local test model so you can test every feature immediately).*

### 4. Run the Web Application
```bash
python main.py
```
Then open your browser to: **`http://localhost:8000`**

### 5. Run the Command-Line Demo
```bash
python main.py --cli
```

### 6. Run the Test Suite
```bash
python -m unittest tests/test_rxguardian.py
```
*(All 7 unit tests pass in under 0.01s!)*

---

## 📁 Project Structure

```
rxguardian-strands-agent/
├── README.md                          # Project documentation
├── requirements.txt                   # Project dependencies
├── pyproject.toml                     # Package definition
├── .env.example                       # Environment config template
├── main.py                            # Web server & CLI runner
├── rxguardian/
│   ├── config.py                      # App settings & Bedrock detection
│   ├── models/
│   │   ├── data_models.py             # Pydantic schemas for prescriptions & alerts
│   │   └── model_provider.py          # BedrockModel wrapper + Student test model
│   ├── tools/
│   │   ├── clinical_db.py             # Embedded clinical pharmacopeia data
│   │   └── clinical_tools.py          # Strands @tool decorated functions
│   ├── agents/
│   │   ├── parser_agent.py            # Extracts meds from doctor notes
│   │   ├── interaction_agent.py       # Screens drug, food & organ risks
│   │   ├── plain_language_agent.py    # Translates into 5th-grade English & Spanish
│   │   ├── schedule_agent.py          # Formulates 4-block daily calendar
│   │   └── safety_agent.py            # Connects 24/7 emergency hotlines
│   ├── workflows/
│   │   └── graph_pipeline.py          # Strands GraphBuilder pipeline
│   └── web/
│       ├── app.py                     # FastAPI web server
│       └── static/
│           ├── index.html             # Accessible, modern web UI
│           ├── styles.css             # Glassmorphic, responsive styles
│           └── app.js                 # Dynamic UI logic & Web Speech API
└── tests/
    └── test_rxguardian.py             # 100% passing test suite
```

---

## 💡 Social Good Impact

| Problem in Underserved Communities | RxGuardian Solution |
| :--- | :--- |
| **High Health Illiteracy:** 53% of adults read below an 8th-grade level. | Automatically translates all instructions into friendly **5th-grade words**. |
| **Polypharmacy Risk:** Seniors take 5+ pills daily without knowing if they clash. | **Under 1-second AI clash screening** against FDA interaction databases. |
| **Language Barriers:** Immigrant families struggle with English-only labels. | Multilingual support in **Spanish, Hindi, and Tagalog**. |
| **Visual Impairment:** Elderly patients struggle to read 6pt printed pill labels. | Built-in **1-click Read Aloud audio** powered by browser speech synthesis. |
| **Accidental Overdoses:** Confusion over when to take which pill. | **Clear 4-block visual calendar** (Morning, Noon, Evening, Bedtime). |

---

## 📜 License
MIT License. Created with ❤️ by Khushboo Pandey for the AWS Builder Center Hackathon.
