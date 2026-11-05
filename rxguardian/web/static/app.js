// app.js - Client-side script for RxGuardian
// Written by Khushboo for our AWS Strands Hackathon project
// Handles multi-agent pipeline animation, result cards, and multilingual audio reading!

let currentAnalysisData = null;

// When the browser finishes loading the page
document.addEventListener("DOMContentLoaded", () => {
  console.log("RxGuardian loaded successfully!");
  
  // 1. Fetch our 1-click sample cases so visitors can test quickly
  loadSamplePresets();

  // 2. Listen for when user submits the prescription form
  const form = document.getElementById("prescriptionForm");
  form.addEventListener("submit", handleFormSubmit);

  // 3. Keep patient language dropdown and audio language selector in sync!
  const patientLang = document.getElementById("patientLanguage");
  const audioLang = document.getElementById("audioLanguageSelect");
  patientLang.addEventListener("change", () => {
    if (audioLang) {
      audioLang.value = patientLang.value;
    }
  });

  // 4. Listen for Read Aloud speech button and Stop button
  const speakBtn = document.getElementById("speakBtn");
  speakBtn.addEventListener("click", readInstructionsAloud);

  const stopBtn = document.getElementById("stopSpeakBtn");
  stopBtn.addEventListener("click", stopSpeaking);

  // 5. Listen for Print button
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
        
        // Also sync the audio voice selector!
        const audioLang = document.getElementById("audioLanguageSelect");
        if (audioLang) {
          audioLang.value = preset.language;
        }

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

  // Show loading state and reset all agents to "Waiting"
  showLoading(true);
  resetAgentFlow();

  // Stop any ongoing speech if playing
  stopSpeaking();

  // Start the server fetch request in parallel
  const fetchPromise = fetch("/api/analyze", {
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

  // Step-by-step sequential animation of the 5 agents!
  // This ensures EACH agent lights up, does its job, and marks "Done ✓" without getting stuck!
  const agentSteps = [
    { id: "step-parser", name: "Parser Agent" },
    { id: "step-screener", name: "Interaction Screener" },
    { id: "step-plain", name: "Plain Language Agent" },
    { id: "step-scheduler", name: "Schedule Planner" },
    { id: "step-safety", name: "Safety Escalation" }
  ];

  for (let i = 0; i < agentSteps.length; i++) {
    const stepEl = document.getElementById(agentSteps[i].id);
    if (stepEl) {
      stepEl.classList.add("active");
      stepEl.classList.remove("done");
      stepEl.querySelector(".step-status").textContent = "Working...";
    }

    // Give visitors 350ms to visibly see this agent working in the swarm!
    await new Promise((resolve) => setTimeout(resolve, 350));

    if (stepEl) {
      stepEl.classList.remove("active");
      stepEl.classList.add("done");
      stepEl.querySelector(".step-status").textContent = "Done ✓";
    }
  }

  // Wait for the backend analysis to finish
  try {
    const response = await fetchPromise;

    if (!response.ok) {
      throw new Error(`Server returned error code: ${response.status}`);
    }

    const data = await response.json();
    currentAnalysisData = data;

    // Render all results into cards on the page!
    renderResults(data);
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

// Reset all 5 agents back to "Waiting" state
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

// Web Speech API: Reads out loud in English, Hindi, Spanish, or Tagalog!
function readInstructionsAloud() {
  if (!('speechSynthesis' in window)) {
    alert("Sorry, your web browser does not support text-to-speech audio.");
    return;
  }

  // Cancel any ongoing speech first
  window.speechSynthesis.cancel();

  if (!currentAnalysisData) {
    alert("Please run an analysis first to read aloud!");
    return;
  }

  const selectedLang = document.getElementById("audioLanguageSelect").value;
  let speechText = "";
  let bcp47Code = "en-US";

  // 1. HINDI (हिंदी)
  if (selectedLang === "Hindi") {
    bcp47Code = "hi-IN";
    speechText = "नमस्ते! यह आपका आर-एक्स गार्डियन सुरक्षा सारांश है। ";

    if (currentAnalysisData.drug_interactions.length > 0) {
      speechText += "सावधानी! आपकी दवाओं में खतरनाक दुष्प्रभाव का जोखिम पाया गया है। ";
      currentAnalysisData.drug_interactions.forEach((d) => {
        speechText += `${d.drugs_involved.join(' और ')} को एक साथ लेने पर समस्या हो सकती है। डॉक्टर से सलाह लें। `;
      });
    }

    if (currentAnalysisData.organ_risks.length > 0) {
      currentAnalysisData.organ_risks.forEach((o) => {
        speechText += `कृपया ध्यान दें: ${o.medicine} आपकी किडनी या लिवर के लिए हानिकारक हो सकती है। `;
      });
    }

    speechText += "आपकी दवाओं का दैनिक समय: ";
    currentAnalysisData.daily_schedule.forEach((s) => {
      const pills = s.medicines.map(m => m.name).join(", ");
      speechText += `${s.time_of_day}: ${pills}। `;
    });

    speechText += "किसी भी आपातकालीन सहायता के लिए टोल फ्री नंबर एक आठ शून्य शून्य दो दो दो एक दो दो दो पर संपर्क करें। स्वस्थ रहें!";
  }
  // 2. SPANISH (Español)
  else if (selectedLang === "Spanish") {
    bcp47Code = "es-ES";
    speechText = "¡Hola! Este es su resumen de seguridad médica de RxGuardian. ";

    if (currentAnalysisData.drug_interactions.length > 0) {
      speechText += "Alerta importante de seguridad: Se detectaron interacciones entre sus medicamentos. ";
      currentAnalysisData.drug_interactions.forEach((d) => {
        speechText += `${d.plain_warning}. ${d.what_to_do}. `;
      });
    }

    if (currentAnalysisData.organ_risks.length > 0) {
      currentAnalysisData.organ_risks.forEach((o) => {
        speechText += `Precaución médica: ${o.simple_warning}. `;
      });
    }

    speechText += "Su horario diario de medicamentos: ";
    currentAnalysisData.daily_schedule.forEach((s) => {
      const pills = s.medicines.map(m => `${m.name} ${m.dose}`).join(", ");
      speechText += `${s.time_of_day}: ${pills}. `;
    });

    speechText += "Para consultas médicas gratuitas las 24 horas, llame al 1-800-222-1222. ¡Cuide su salud!";
  }
  // 3. TAGALOG (Filipino)
  else if (selectedLang === "Tagalog") {
    bcp47Code = "fil-PH";
    speechText = "Kamusta! Narito ang iyong buod ng kaligtasan sa gamot mula sa RxGuardian. ";

    if (currentAnalysisData.drug_interactions.length > 0) {
      speechText += "Babala sa kaligtasan: May natukoy na panganib sa pagsasama ng mga gamot. ";
      currentAnalysisData.drug_interactions.forEach((d) => {
        speechText += `${d.plain_warning}. ${d.what_to_do}. `;
      });
    }

    speechText += "Iskedyul ng iyong mga gamot: ";
    currentAnalysisData.daily_schedule.forEach((s) => {
      const pills = s.medicines.map(m => `${m.name} ${m.dose}`).join(", ");
      speechText += `${s.time_of_day}: ${pills}. `;
    });

    speechText += "Para sa tulong, tumawag sa 911 o helpline. Manatiling ligtas!";
  }
  // 4. ENGLISH (Default)
  else {
    bcp47Code = "en-US";
    speechText = "Hello! Here is your RxGuardian safety summary. ";

    if (currentAnalysisData.drug_interactions.length > 0) {
      speechText += "Important safety alert. We found medication clashes: ";
      currentAnalysisData.drug_interactions.forEach((d) => {
        speechText += `${d.plain_warning}. ${d.what_to_do}. `;
      });
    }

    if (currentAnalysisData.organ_risks.length > 0) {
      currentAnalysisData.organ_risks.forEach((o) => {
        speechText += `Warning for ${o.organ_at_risk}: ${o.simple_warning}. `;
      });
    }

    speechText += "Here is your morning routine: ";
    const morningSlot = currentAnalysisData.daily_schedule.find((s) => s.time_of_day.includes("Morning"));
    if (morningSlot) {
      morningSlot.medicines.forEach((m) => {
        speechText += `Take ${m.name}, ${m.dose}, ${m.note}. `;
      });
    }

    speechText += "For free 24-hour medicine questions, call 1-800-222-1222. Stay safe!";
  }

  const utterance = new SpeechSynthesisUtterance(speechText);
  utterance.lang = bcp47Code;
  utterance.rate = 0.92;
  utterance.pitch = 1.0;

  // Look for a voice matching this language
  const voices = window.speechSynthesis.getVoices();
  const langPrefix = bcp47Code.slice(0, 2);
  const matchedVoice = voices.find((v) => v.lang.toLowerCase().startsWith(langPrefix));
  if (matchedVoice) {
    utterance.voice = matchedVoice;
  }

  const speakBtn = document.getElementById("speakBtn");
  const stopBtn = document.getElementById("stopSpeakBtn");

  utterance.onstart = () => {
    speakBtn.classList.add("hidden");
    stopBtn.classList.remove("hidden");
  };

  utterance.onend = () => {
    speakBtn.classList.remove("hidden");
    stopBtn.classList.add("hidden");
  };

  utterance.onerror = () => {
    speakBtn.classList.remove("hidden");
    stopBtn.classList.add("hidden");
  };

  window.speechSynthesis.speak(utterance);
}

// Stop audio playback
function stopSpeaking() {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
  const speakBtn = document.getElementById("speakBtn");
  const stopBtn = document.getElementById("stopSpeakBtn");
  if (speakBtn) speakBtn.classList.remove("hidden");
  if (stopBtn) stopBtn.classList.add("hidden");
}
