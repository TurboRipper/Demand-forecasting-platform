from collections import deque
from datetime import datetime, timezone

from fastapi import FastAPI

from app.shared.contracts import AgentInsight, AgentOrchestrationRequest, AgentPlan, AggregateResponse

app = FastAPI(title="RetailPulse ML Agent Orchestrator", version="1.0.0")
PLANS: deque[dict] = deque(maxlen=20)


def demand_sensing_agent(summary: AggregateResponse) -> AgentInsight:
    forecast_units = summary.forecast_units or 0.0
    demand_prediction = next(item for item in summary.model_predictions if item.model_name == "demand-forecast")
    priority = "high" if forecast_units >= 140 else "medium" if forecast_units >= 90 else "low"
    conclusion = f"Demand agent expects {forecast_units:.0f} units/day with {demand_prediction.label} velocity."
    rationale = (
        "Recent sales velocity, promotion lift, and seasonal demand are the dominant demand signals."
    )
    recommended_action = (
        "Reserve additional forward stock and increase forecast refresh cadence."
        if priority != "low"
        else "Keep the baseline forecast cycle and review only if intraday velocity shifts."
    )
    return AgentInsight(
        agent_id="demand-sensing-agent",
        role="Demand sensing",
        priority=priority,
        conclusion=conclusion,
        rationale=rationale,
        recommended_action=recommended_action,
    )


def inventory_guardian_agent(summary: AggregateResponse) -> AgentInsight:
    stock_cover_days = float(summary.product_snapshot["stock_cover_days"])
    stockout_prediction = next(item for item in summary.model_predictions if item.model_name == "stockout-risk")
    priority = "critical" if stockout_prediction.risk_score >= 0.8 else "high" if stock_cover_days <= 3.0 else "medium"
    conclusion = (
        f"Inventory agent sees {stock_cover_days:.1f} days of cover with stockout status {stockout_prediction.label}."
    )
    rationale = "Current stock cover, supplier lead time, and replenishment gap determine inventory fragility."
    recommended_action = (
        "Raise an urgent replenishment ticket and source transfer stock from adjacent stores."
        if priority in {"critical", "high"}
        else "Keep standard replenishment timing but watch cover against the next forecast cycle."
    )
    return AgentInsight(
        agent_id="inventory-guardian-agent",
        role="Inventory protection",
        priority=priority,
        conclusion=conclusion,
        rationale=rationale,
        recommended_action=recommended_action,
    )


def merchandising_agent(summary: AggregateResponse) -> AgentInsight:
    anomaly_prediction = next(item for item in summary.model_predictions if item.model_name == "demand-anomaly")
    discount = float(summary.product_snapshot["effective_price"])
    priority = "high" if anomaly_prediction.risk_score >= 0.72 else "medium" if anomaly_prediction.risk_score >= 0.48 else "low"
    conclusion = (
        f"Merchandising agent flags {anomaly_prediction.label} demand behavior around the current price point of {discount:.2f}."
    )
    rationale = "Price changes, promotions, and unusual traffic patterns can distort true baseline demand."
    recommended_action = (
        "Audit promotion execution and isolate whether uplift is campaign-driven or demand-driven."
        if priority != "low"
        else "Maintain current pricing and merchandising posture."
    )
    return AgentInsight(
        agent_id="merchandising-agent",
        role="Merchandising review",
        priority=priority,
        conclusion=conclusion,
        rationale=rationale,
        recommended_action=recommended_action,
    )


def supervisor_agent(summary: AggregateResponse, agent_trace: list[AgentInsight]) -> AgentPlan:
    priority_weight = {"low": 0.25, "medium": 0.5, "high": 0.8, "critical": 0.95}
    confidence = round(
        min(
            0.98,
            0.42 * summary.overall_score
            + 0.2
            + sum(priority_weight[item.priority] for item in agent_trace) / (len(agent_trace) * 4),
        ),
        4,
    )
    escalation = any(item.priority in {"critical", "high"} for item in agent_trace)
    coordination_mode = "active-intervention" if escalation else "monitoring-loop"
    next_actions = [item.recommended_action for item in agent_trace]
    next_actions.append(summary.recommended_action)
    supervisor_summary = (
        "Supervisor agent aligned demand, inventory, and merchandising signals into one replenishment plan."
        if escalation
        else "Supervisor agent recommends maintaining routine planning with targeted monitoring."
    )
    return AgentPlan(
        coordination_mode=coordination_mode,
        supervisor_summary=supervisor_summary,
        confidence=confidence,
        next_actions=next_actions,
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "agent-orchestrator", "stored_plans": len(PLANS)}


@app.get("/history")
def history() -> dict:
    return {"forecasts": list(PLANS)}


@app.post("/orchestrate")
def orchestrate(request: AgentOrchestrationRequest) -> dict:
    summary = request.summary
    agent_trace = [
        demand_sensing_agent(summary),
        inventory_guardian_agent(summary),
        merchandising_agent(summary),
    ]
    plan = supervisor_agent(summary, agent_trace)
    enriched = summary.model_copy(update={"agent_trace": agent_trace, "agent_plan": plan})
    response = enriched.model_dump()
    response["created_at"] = datetime.now(timezone.utc).isoformat()
    PLANS.appendleft(response)
    return response
