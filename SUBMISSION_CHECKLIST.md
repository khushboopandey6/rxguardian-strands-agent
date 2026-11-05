# RxGuardian: Final Hackathon Submission Checklist
**AWS Builder Center: "Strands SDK: Workshop to Ship"**  
**Deadline:** November 4, 2026 at 11:59 PM PST (Tonight!)

---

### ✅ Step 1: Verify Free Sandbox Workshop Completion
The rules state:
> *"Complete the free Strands SDK workshop on Builder Center during the hackathon window (October 28 to November 4). Workshop completion is required to qualify."*
- [ ] Go to [AWS Builder Center Workshops](https://builder.aws.com)
- [ ] Ensure the workshop **"Building AI Agents with Strands SDK: From Simple Loops to Multi-Agent Swarms"** is marked as completed on your profile.

---

### ✅ Step 2: Push Your Code to a Public GitHub Repository
The rules state:
> *"A link to a public repository with the agent's source code."*

Run these commands in your terminal to initialize and push your repository:

```bash
cd /Users/kashi/.gemini/antigravity-ide/scratch/rxguardian-strands-agent
git init
git add .
git commit -m "Initial commit: RxGuardian AI agent built with AWS Strands Agents SDK"
# Create a new public repo on your GitHub (e.g. https://github.com/your-username/rxguardian-strands-agent)
git branch -M main
git remote add origin https://github.com/khushboopandey6/rxguardian-strands-agent
git push -u origin main
```

---

### ✅ Step 3: Record & Upload Your 3-Minute Demo Video
The rules state:
> *"A short, publicly available demo video, under three minutes, showing the agent working."*
- [ ] Launch the web app locally:
  ```bash
  cd /Users/kashi/.gemini/antigravity-ide/scratch/rxguardian-strands-agent
  python3 main.py
  ```
- [ ] Open `http://localhost:8000` in Google Chrome.
- [ ] Open **QuickTime Player** on your Mac (File -> New Screen Recording) or Loom.
- [ ] Follow [DEMO_VIDEO_SCRIPT.md](file:///Users/kashi/.gemini/antigravity-ide/scratch/rxguardian-strands-agent/DEMO_VIDEO_SCRIPT.md) (takes ~2 minutes 45 seconds).
- [ ] Upload the video to YouTube (set to **Public** or **Unlisted**) or Loom.
- [ ] Copy the video URL.

---

### ✅ Step 4: Submit Your Project Article on Builder Center
The rules state:
> *"A project article on Builder Center describing the agent, what it does, and the social good problem it addresses."*
- [ ] Go to the hackathon page on AWS Builder Center:
  **"Strands SDK: Workshop to Ship"** -> Click **"Create post"** or **"Your project"** -> **Submit Project**.
- [ ] Title: `RxGuardian: AI Health Equity & Prescription Safety Agent with AWS Strands SDK`
- [ ] Focus Area: **Health**
- [ ] Paste the markdown content from [BUILDER_CENTER_ARTICLE.md](file:///Users/kashi/.gemini/antigravity-ide/scratch/rxguardian-strands-agent/BUILDER_CENTER_ARTICLE.md).
- [ ] Paste your **Public GitHub Repository Link**.
- [ ] Paste your **Demo Video URL**.
- [ ] Submit before 11:59 PM PST!

---

### 🏆 Rubric Alignment Check:
- **Social Impact (25%):** Tackles 1.5M annual preventable medication errors; delivers 5th-grade plain language, multilingual support, and low-vision accessibility.
- **Technical Execution (25%):** Utilizes Strands `GraphBuilder` DAG, `@tool` decorators, Amazon Bedrock connectivity, and 100% passing test suite.
- **Communication Quality (25%):** Authentic student storytelling, clear before/after comparison table, step-by-step video script.
- **Originality (25%):** Novel health equity multi-agent architecture with chronotherapy scheduling and direct alignment with AWS Social Impact Credits.
