from fastapi import FastAPI, HTTPException

from app.shared.config import get_settings
from app.shared.contracts import AgentOrchestrationRequest, AggregateRequest, AggregateResponse, ModelPrediction, ProcessedRetailRecord
from app.shared.http import post_json

app = FastAPI(title="RetailPulse ML Router Service", version="1.0.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "router"}


@app.post("/route")
def route(payload: ProcessedRetailRecord) -> dict:
    settings = get_settings()
    try:
        demand = ModelPrediction(**post_json(settings.failure_model_url, payload.model_dump()))
        anomaly = ModelPrediction(**post_json(settings.anomaly_model_url, payload.model_dump()))
        stockout = ModelPrediction(**post_json(settings.quality_model_url, payload.model_dump()))
        aggregate_request = AggregateRequest(
            sales_record=payload,
            predictions=[demand, anomaly, stockout],
        )
        summary = AggregateResponse(**post_json(settings.intelligence_hub_url, aggregate_request.model_dump()))
        orchestrated = post_json(
            settings.agent_orchestrator_url,
            AgentOrchestrationRequest(summary=summary).model_dump(),
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Downstream scoring failed: {exc}") from exc

    return {
        "pipeline_stage": "router",
        "scenario_id": payload.scenario_id,
        "predictions": [demand.model_dump(), anomaly.model_dump(), stockout.model_dump()],
        "decision_summary": summary.model_dump(),
        "agentic_summary": orchestrated,
    }
