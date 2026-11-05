// app.js - Client-side script for RxGuardian
// Written by Khushboo for our AWS Strands Hackathon project
// Connects our UI to our FastAPI backend and handles audio speech for patients!

let currentAnalysisData = null;

// When the browser finishes loading the page
document.addEventListener("DOMContentLoaded", () => {
  console.log("RxGuardian loaded successfully!");
  
  // 1. Fetch our 1-click sample cases so visitors can test quickly
  loadSamplePresets();

  // 2. Listen for when user submits the prescription form
  const form = document.getElementById("prescriptionForm");
  form.addEventListener("submit", handleFormSubmit);

  // 3. Listen for Read Aloud speech button
  const speakBtn = document.getElementById("speakBtn");
  speakBtn.addEventListener("click", readInstructionsAloud);

  // 4. Listen for Print button
  const printBtn = document.getElementById("printBtn");
  printBtn.addEventListener("click", () => window.print());
});

// Load the 3 preset patient scenarios from our API
async function loadSamplePresets() {
  const container = document.getElementById("presetButtons");
  try {
    const res = await fetch("/api/presets");
    const presets = await res.json();

    container.innerHTML = "";
    presets.forEach((preset) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "btn-preset";
      btn.textContent = preset.title;
      btn.title = preset.description;
      
      btn.addEventListener("click", () => {
        // Fill form fields with preset data
        document.getElementById("patientAge").value = preset.age;
        document.getElementById("patientLanguage").value = preset.language;
        document.getElementById("patientConditions").value = preset.conditions.join(", ");
        document.getElementById("prescriptionText").value = preset.raw_text;

        // Automatically trigger analysis for an instant demo!
        handleFormSubmit(new Event("submit"));
      });

      container.appendChild(btn);
    });
  } catch (err) {
    console.error("Could not load presets:", err);
  }
}

// When user clicks 'Run Strands Agent Swarm'
async function handleFormSubmit(e) {
  if (e && e.preventDefault) e.preventDefault();

  const age = parseInt(document.getElementById("patientAge").value, 10) || 65;
  const language = document.getElementById("patientLanguage").value;
  const conditionsRaw = document.getElementById("patientConditions").value;
  const rawText = document.getElementById("prescriptionText").value.trim();

  if (!rawText) {
    alert("Please enter or paste a prescription to analyze!");
    return;
  }

  // Parse conditions into an array
  const conditions = conditionsRaw
    .split(",")
    .map((c) => c.trim())
    .filter((c) => c.length > 0);

  // Show loading spinner and hide empty/old results
  showLoading(true);
  resetAgentFlow();

  // Animate the 5 agent steps so visitors can see the Strands swarm in action
  animateAgentSteps();

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prescription_raw_text: rawText,
        patient: {
          age: age,
          preferred_language: language,
          health_conditions: conditions,
          allergies: []
        }
      })
    });

    if (!response.ok) {
      throw new Error(`Server returned error code: ${response.status}`);
    }

    const data = await response.json();
    currentAnalysisData = data;

    // Render results onto the page
    renderResults(data);
    markAllStepsDone();
  } catch (err) {
    console.error("Error running agent analysis:", err);
    alert("Something went wrong while running the agents. Check the console for details.");
  } finally {
    showLoading(false);
  }
}

// Helper to switch between empty, loading, and result cards
function showLoading(isLoading) {
  const emptyState = document.getElementById("emptyState");
  const loadingState = document.getElementById("loadingState");
  const resultsContent = document.getElementById("resultsContent");

  if (isLoading) {
    emptyState.classList.add("hidden");
    loadingState.classList.remove("hidden");
    resultsContent.classList.add("hidden");
  } else {
    loadingState.classList.add("hidden");
    resultsContent.classList.remove("hidden");
  }
}

// Animate the 5 agent boxes on the left panel
function animateAgentSteps() {
  const steps = ["step-parser", "step-screener", "step-plain", "step-scheduler", "step-safety"];
  
  steps.forEach((id, index) => {
    setTimeout(() => {
      const el = document.getElementById(id);
      if (el) {
        el.classList.add("active");
        el.querySelector(".step-status").textContent = "Working...";
      }
    }, index * 250);
  });
}

function markAllStepsDone() {
  const steps = ["step-parser", "step-screener", "step-plain", "step-scheduler", "step-safety"];
  steps.forEach((id) => {
    const el = document.getElementById(id);
    if (el) {
      el.classList.remove("active");
      el.classList.add("done");
      el.querySelector(".step-status").textContent = "Done ✓";
    }
  });
}

function resetAgentFlow() {
  const steps = ["step-parser", "step-screener", "step-plain", "step-scheduler", "step-safety"];
  steps.forEach((id) => {
    const el = document.getElementById(id);
    if (el) {
      el.classList.remove("active", "done");
      el.querySelector(".step-status").textContent = "Waiting";
    }
  });
}

// Renders the structured agent output into beautiful cards
function renderResults(data) {
  // 1. Telemetry badge
  document.getElementById("telemetryTime").textContent = `${data.patient_summary.seconds_taken || 0.8}s`;
  document.getElementById("telemetryAgents").textContent = data.patient_summary.agents_coordinated || 5;

  // 2. High-Risk Banner
  const alertBanner = document.getElementById("highRiskAlert");
  const hasHighRisk = data.drug_interactions.some((d) => d.severity === "HIGH") || data.organ_risks.some((o) => o.severity === "HIGH");

  if (hasHighRisk) {
    alertBanner.classList.remove("hidden");
  } else {
    alertBanner.classList.add("hidden");
  }

  // 3. Drug Interaction Warnings
  const drugList = document.getElementById("drugInteractionsList");
  drugList.innerHTML = "";

  if (data.drug_interactions.length === 0 && data.organ_risks.length === 0) {
    drugList.innerHTML = `<div class="warning-card"><p>✅ No dangerous drug clashes or organ risks detected for these medicines.</p></div>`;
  } else {
    // Render drug clashes
    data.drug_interactions.forEach((item) => {
      const card = document.createElement("div");
      const isHigh = item.severity === "HIGH";
      card.className = `warning-card ${isHigh ? "severity-high" : "severity-moderate"}`;
      card.innerHTML = `
        <div class="warning-header">
          <span class="warning-drugs">⚠️ ${item.drugs_involved.join(" + ").toUpperCase()}</span>
          <span class="severity-pill ${isHigh ? "pill-high" : "pill-mod"}">${item.severity} RISK</span>
        </div>
        <p class="plain-warning-text">${item.plain_warning}</p>
        <div class="action-tip">👉 <strong>What to do:</strong> ${item.what_to_do}</div>
      `;
      drugList.appendChild(card);
    });

    // Render organ warnings
    data.organ_risks.forEach((organ) => {
      const card = document.createElement("div");
      card.className = "warning-card severity-high";
      card.innerHTML = `
        <div class="warning-header">
          <span class="warning-drugs">⚠️ ${organ.medicine} vs ${organ.organ_at_risk}</span>
          <span class="severity-pill pill-high">${organ.severity} RISK</span>
        </div>
        <p class="plain-warning-text">${organ.simple_warning}</p>
      `;
      drugList.appendChild(card);
    });
  }

  // 4. Food & Drink Precautions
  const foodList = document.getElementById("foodInteractionsList");
  foodList.innerHTML = "";
  if (data.food_interactions.length === 0) {
    foodList.innerHTML = `<div class="warning-card"><p>✅ No common food or drink restrictions found for these medications.</p></div>`;
  } else {
    data.food_interactions.forEach((item) => {
      const card = document.createElement("div");
      card.className = "warning-card severity-moderate";
      card.innerHTML = `
        <div class="warning-header">
          <span class="warning-drugs">🚫 Avoid: ${item.food_to_avoid}</span>
          <span class="severity-pill pill-mod">Diet Precaution</span>
        </div>
        <p class="plain-warning-text">${item.simple_warning}</p>
        <div class="action-tip">👉 <strong>Advice:</strong> ${item.what_to_do}</div>
      `;
      foodList.appendChild(card);
    });
  }

  // 5. Daily Schedule Calendar
  const timeline = document.getElementById("scheduleTimeline");
  timeline.innerHTML = "";
  data.daily_schedule.forEach((slot) => {
    const card = document.createElement("div");
    card.className = "timeline-card";
    
    let pillsHtml = slot.medicines
      .map((p) => `<li class="timeline-pill-item">💊 <strong>${p.name}</strong> (${p.dose})<small>${p.note}</small></li>`)
      .join("");

    card.innerHTML = `
      <div class="timeline-time">${slot.time_of_day}</div>
      <ul class="timeline-pills">${pillsHtml}</ul>
      <div class="timeline-tip">💡 ${slot.friendly_tip}</div>
    `;
    timeline.appendChild(card);
  });

  // 6. Plain-Language Medicine Cards
  const plainList = document.getElementById("plainCardsList");
  plainList.innerHTML = "";
  data.plain_cards.forEach((cardData) => {
    const card = document.createElement("div");
    card.className = "plain-card";
    card.innerHTML = `
      <div class="plain-card-top">
        <span class="plain-card-name">💊 ${cardData.name}</span>
        <span class="pronounce-tag">Say it: "${cardData.say_it_like}"</span>
      </div>
      <p class="plain-card-desc"><strong>What it does:</strong> ${cardData.what_it_does}</p>
      <div class="plain-card-meta">
        <div><strong>How to take:</strong> ${cardData.how_to_take}</div>
        <div><strong>Foods to skip:</strong> ${cardData.foods_to_skip.join(", ") || "None"}</div>
        <div><strong>Call doctor if:</strong> ${cardData.warning_signs.join(", ")}</div>
      </div>
    `;
    plainList.appendChild(card);
  });

  // 7. Free Emergency Hotlines
  const hotlines = document.getElementById("hotlinesList");
  hotlines.innerHTML = "";
  data.emergency_contacts.forEach((contact) => {
    const card = document.createElement("div");
    card.className = "hotline-card";
    card.innerHTML = `
      <div class="hotline-name">${contact.name}</div>
      <div class="hotline-phone">${contact.phone}</div>
      <div class="hotline-desc">${contact.when_to_call} (${contact.hours})</div>
    `;
    hotlines.appendChild(card);
  });
}

// Web Speech API: Reads out loud for low-vision patients or elderly caregivers
function readInstructionsAloud() {
  if (!('speechSynthesis' in window)) {
    alert("Sorry, your web browser does not support text-to-speech audio.");
    return;
  }

  // Cancel any ongoing speech
  window.speechSynthesis.cancel();

  if (!currentAnalysisData) {
    alert("Please run an analysis first to read aloud!");
    return;
  }

  let speechText = "Hello! Here is your RxGuardian safety summary. ";

  if (currentAnalysisData.drug_interactions.length > 0) {
    speechText += "Important safety alert. We found medication clashes: ";
    currentAnalysisData.drug_interactions.forEach((d) => {
      speechText += `${d.plain_warning}. ${d.what_to_do}. `;
    });
  }

  speechText += "Here is your morning routine: ";
  const morningSlot = currentAnalysisData.daily_schedule.find((s) => s.time_of_day.includes("Morning"));
  if (morningSlot) {
    morningSlot.medicines.forEach((m) => {
      speechText += `Take ${m.name}, ${m.dose}, ${m.note}. `;
    });
  }

  speechText += "For free 24-hour poison or medicine questions, call 1-800-222-1222. Stay safe!";

  const utterance = new SpeechSynthesisUtterance(speechText);
  utterance.rate = 0.95; // slightly slower for clarity
  utterance.pitch = 1.0;
  
  window.speechSynthesis.speak(utterance);
}
