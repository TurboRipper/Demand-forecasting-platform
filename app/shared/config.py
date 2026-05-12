import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    preprocessing_url: str = os.getenv("PREPROCESSING_URL", "http://preprocessing:8000/preprocess")
    router_url: str = os.getenv("ROUTER_URL", "http://router:8000/route")
    failure_model_url: str = os.getenv("FAILURE_MODEL_URL", "http://failure-model:8000/predict")
    anomaly_model_url: str = os.getenv("ANOMALY_MODEL_URL", "http://anomaly-model:8000/predict")
    quality_model_url: str = os.getenv("QUALITY_MODEL_URL", "http://quality-model:8000/predict")
    intelligence_hub_url: str = os.getenv("INTELLIGENCE_HUB_URL", "http://intelligence-hub:8000/aggregate")
    intelligence_hub_base_url: str = os.getenv("INTELLIGENCE_HUB_BASE_URL", "http://intelligence-hub:8000")
    agent_orchestrator_url: str = os.getenv("AGENT_ORCHESTRATOR_URL", "http://agent-orchestrator:8000/orchestrate")
    agent_orchestrator_base_url: str = os.getenv("AGENT_ORCHESTRATOR_BASE_URL", "http://agent-orchestrator:8000")
    ingestion_url: str = os.getenv("INGESTION_URL", "http://ingestion:8000/ingest")
    request_timeout_seconds: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "12"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
