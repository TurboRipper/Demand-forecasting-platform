from fastapi import FastAPI, HTTPException

from app.shared.config import get_settings
from app.shared.contracts import RawRetailRecord
from app.shared.http import post_json

app = FastAPI(title="RetailPulse ML Ingestion Service", version="1.0.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "ingestion"}


@app.post("/ingest")
def ingest(payload: RawRetailRecord) -> dict:
    try:
        result = post_json(get_settings().preprocessing_url, payload.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Preprocessing unavailable: {exc}") from exc
    return {
        "pipeline_stage": "ingestion",
        "accepted": True,
        "scenario_id": payload.scenario_id,
        "downstream_result": result,
    }
