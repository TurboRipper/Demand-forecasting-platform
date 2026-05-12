from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.shared.config import get_settings
from app.shared.demo_data import get_scenario_by_id, get_scenarios
from app.shared.http import get_json, post_json

app = FastAPI(title="RetailPulse ML Dashboard", version="1.0.0")
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(static_dir / "index.html")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "dashboard"}


@app.get("/api/scenarios")
def scenarios() -> dict:
    return {"scenarios": get_scenarios()}


@app.post("/api/demo/{scenario_id}")
def run_demo(scenario_id: str) -> dict:
    scenario = get_scenario_by_id(scenario_id)
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    try:
        return post_json(get_settings().ingestion_url, scenario["payload"])
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Pipeline unavailable: {exc}") from exc


@app.get("/api/history")
def history() -> dict:
    try:
        return get_json(f"{get_settings().agent_orchestrator_base_url}/history")
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"History unavailable: {exc}") from exc
