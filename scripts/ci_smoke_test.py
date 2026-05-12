from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.agent_orchestrator.main import orchestrate
from app.intelligence_hub.main import summarize
from app.models.anomaly.main import predict as predict_anomaly
from app.models.failure.main import predict as predict_demand
from app.models.quality.main import predict as predict_stockout
from app.preprocessing.main import preprocess_payload
from app.shared.contracts import AgentOrchestrationRequest, AggregateRequest, ModelPrediction, RawRetailRecord
from app.shared.demo_data import get_scenarios


def run_pipeline_for_scenario(scenario: dict) -> dict:
    raw_record = RawRetailRecord(**scenario["payload"])
    processed = preprocess_payload(raw_record)
    predictions = [
        ModelPrediction(**predict_demand(processed)),
        ModelPrediction(**predict_anomaly(processed)),
        ModelPrediction(**predict_stockout(processed)),
    ]
    summary = summarize(AggregateRequest(sales_record=processed, predictions=predictions))
    return orchestrate(AgentOrchestrationRequest(summary=summary))


def main() -> None:
    scenarios = get_scenarios()
    expected_severities = {"stable", "elevated", "critical"}

    print("Running RetailPulse ML smoke test")
    for scenario in scenarios:
        result = run_pipeline_for_scenario(scenario)
        assert result["scenario_id"] == scenario["id"]
        assert result["severity"] in expected_severities
        assert len(result["model_predictions"]) == 3
        assert len(result["agent_trace"]) == 3
        assert result["agent_plan"] is not None
        assert result["agent_plan"]["next_actions"]
        print(
            f"- {scenario['id']}: severity={result['severity']}, "
            f"forecast_units={result['forecast_units']}, "
            f"coordination={result['agent_plan']['coordination_mode']}"
        )

    print("RetailPulse ML smoke test passed")


if __name__ == "__main__":
    main()
