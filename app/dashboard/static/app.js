async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with status ${response.status}`);
  }
  return response.json();
}

function severityClass(value) {
  if (value === "critical") return "critical";
  if (value === "elevated") return "elevated";
  if (value === "stable") return "stable";
  return "neutral";
}

function percent(value) {
  return `${Math.round(value * 100)}%`;
}

function formatProjection(prediction) {
  if (prediction.projected_value === null || prediction.projected_value === undefined) {
    return "";
  }
  return `<p>Projection: ${prediction.projected_value} ${prediction.unit || ""}</p>`;
}

function renderSummary(summary) {
  const container = document.getElementById("forecast-summary");
  const statusPill = document.getElementById("status-pill");

  statusPill.textContent = summary.severity;
  statusPill.className = `pill ${severityClass(summary.severity)}`;

  const predictions = summary.model_predictions.map((prediction) => `
    <article class="prediction-card">
      <span>${prediction.model_name}</span>
      <strong>${percent(prediction.risk_score)}</strong>
      <p>${prediction.explanation}</p>
      ${formatProjection(prediction)}
      <p>Top factors: ${prediction.factors.join(", ")}</p>
    </article>
  `).join("");

  const forecastBlock = summary.forecast_units !== null && summary.forecast_units !== undefined
    ? `
      <div class="mini-card">
        <span>Forecast</span>
        <strong>${summary.forecast_units} units/day</strong>
      </div>
    `
    : "";

  const agentPlan = summary.agent_plan
    ? `
      <div class="agent-plan">
        <strong>Supervisor Agent</strong>
        <p>${summary.agent_plan.supervisor_summary}</p>
        <p>Mode: ${summary.agent_plan.coordination_mode} - Confidence: ${percent(summary.agent_plan.confidence)}</p>
      </div>
    `
    : "";

  container.className = "summary";
  container.innerHTML = `
    <div>
      <h3>${summary.headline}</h3>
      <p>${summary.recommended_action}</p>
    </div>
    ${agentPlan}
    <div class="summary-grid">
      <div class="mini-card">
        <span>Scenario</span>
        <strong>${summary.scenario_id}</strong>
      </div>
      <div class="mini-card">
        <span>Product</span>
        <strong>${summary.product_id}</strong>
      </div>
      <div class="mini-card">
        <span>Store</span>
        <strong>${summary.store_id}</strong>
      </div>
      <div class="mini-card">
        <span>Overall score</span>
        <strong>${percent(summary.overall_score)}</strong>
      </div>
      ${forecastBlock}
    </div>
    <div class="prediction-grid">${predictions}</div>
  `;
}

function renderAgentTrace(summary) {
  const trace = document.getElementById("agent-trace");
  if (!summary.agent_trace || !summary.agent_trace.length) {
    trace.className = "timeline empty-state";
    trace.textContent = "No agent decisions recorded yet.";
    return;
  }

  trace.className = "timeline";
  const nextActions = summary.agent_plan?.next_actions || [];
  const actionBlock = nextActions.length
    ? `<p>Next actions: ${nextActions.join(" | ")}</p>`
    : "";
  trace.innerHTML = `
    ${summary.agent_trace.map((agent) => `
      <article class="timeline-item">
        <header>
          <strong>${agent.role}</strong>
          <span class="pill neutral">${agent.priority}</span>
        </header>
        <p>${agent.conclusion}</p>
        <p>${agent.rationale}</p>
        <p>${agent.recommended_action}</p>
      </article>
    `).join("")}
    ${actionBlock ? `<article class="timeline-item">${actionBlock}</article>` : ""}
  `;
}

function renderTimeline(forecasts) {
  const timeline = document.getElementById("timeline");
  if (!forecasts.length) {
    timeline.className = "timeline empty-state";
    timeline.textContent = "No forecast events recorded yet.";
    return;
  }

  timeline.className = "timeline";
  timeline.innerHTML = forecasts.map((summary) => `
    <article class="timeline-item">
      <header>
        <strong>${summary.product_id} - ${summary.store_id}</strong>
        <span class="pill ${severityClass(summary.severity)}">${summary.severity}</span>
      </header>
      <p>${summary.headline}</p>
      <p>Score: ${percent(summary.overall_score)} - Scenario: ${summary.scenario_id}</p>
    </article>
  `).join("");
}

async function loadHistory() {
  const data = await fetchJson("/api/history");
  renderTimeline(data.forecasts || []);
}

async function runScenario(id) {
  const summary = document.getElementById("forecast-summary");
  summary.className = "empty-state";
  summary.textContent = "Running pipeline...";
  const trace = document.getElementById("agent-trace");
  trace.className = "timeline empty-state";
  trace.textContent = "Agents are reviewing the scenario...";

  try {
    const result = await fetchJson(`/api/demo/${id}`, { method: "POST" });
    const decisionSummary = result.downstream_result?.downstream_result?.agentic_summary;
    if (!decisionSummary) {
      throw new Error("Pipeline response did not include an agentic forecast summary.");
    }
    renderSummary(decisionSummary);
    renderAgentTrace(decisionSummary);
    await loadHistory();
  } catch (error) {
    summary.className = "empty-state";
    summary.textContent = `Unable to run scenario: ${error.message}`;
    trace.className = "timeline empty-state";
    trace.textContent = `Agent orchestration failed: ${error.message}`;
  }
}

async function loadScenarios() {
  const data = await fetchJson("/api/scenarios");
  const list = document.getElementById("scenario-list");
  list.innerHTML = data.scenarios.map((scenario) => `
    <button class="scenario-button" data-scenario-id="${scenario.id}">
      <strong>${scenario.title}</strong>
      <span>${scenario.description}</span>
    </button>
  `).join("");

  list.querySelectorAll("[data-scenario-id]").forEach((button) => {
    button.addEventListener("click", () => runScenario(button.dataset.scenarioId));
  });
}

document.getElementById("refresh-history").addEventListener("click", () => {
  loadHistory().catch((error) => {
    const timeline = document.getElementById("timeline");
    timeline.className = "timeline empty-state";
    timeline.textContent = `Unable to load timeline: ${error.message}`;
  });
});

Promise.all([loadScenarios(), loadHistory()]).catch((error) => {
  const summary = document.getElementById("forecast-summary");
  summary.className = "empty-state";
  summary.textContent = `Dashboard startup issue: ${error.message}`;
});
