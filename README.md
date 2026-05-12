# RetailPulse ML

Docker-native multi-model demand forecasting platform for retail demos.

## What this project shows

RetailPulse ML is a demo-ready microservice system that connects multiple machine-learning services with Docker Compose. It simulates a retail planning workflow where sales observations flow through ingestion, preprocessing, model routing, demand forecasting, demand anomaly detection, stockout risk scoring, a central decision hub, and an agent orchestrator before appearing on a dashboard.

## Project objective

Build an industry-oriented retail ML deployment showcase that demonstrates:

- containerized model serving
- multi-model orchestration
- agentic decision coordination
- demand forecasting and stockout analysis
- replenishment recommendations for planners
- a presentable dashboard for live demos

## Novelty

- Uses three specialized ML services instead of a single monolithic model.
- Connects every stage through API-driven Docker microservices.
- Uses synthetic but realistic retail sales scenarios for live walkthroughs.
- Produces combined replenishment decisions through a decision hub layer.
- Adds specialist planning agents that critique the forecast before final action is proposed.
- Demonstrates both AI inference and deployment architecture in one project.

## Architecture

```text
Retail Scenarios / Planner Input
                |
                v
         Ingestion Service
                |
                v
       Preprocessing Service
                |
                v
           Router Service
       /          |          \
      v           v           v
 Demand ML   Demand Anomaly   Stockout Risk
      \           |           /
       \          |          /
        v         v         v
        Decision Hub Service
                |
                v
        Agent Orchestrator
                |
                v
 Dashboard + Agent Trace + Timeline
```

## Services

- `ingestion`: receives raw retail sales observations and forwards them.
- `preprocessing`: derives demand and replenishment features.
- `router`: fans retail records out to the model services and decision hub.
- `failure-model`: forecasts short-term demand.
- `anomaly-model`: detects unusual sales behaviour.
- `quality-model`: predicts stockout risk.
- `intelligence-hub`: merges model results into planner actions.
- `agent-orchestrator`: runs specialist retail agents and supervisor coordination.
- `dashboard`: hosts the live demo UI and scenario runner.

## Tech stack

- Python
- FastAPI
- scikit-learn
- Docker
- Docker Compose

## Demo scenarios included

- `steady_baseline`: normal weekday demand with balanced stock
- `promo_surge`: promotion-led jump in demand
- `festival_peak`: holiday demand and footfall spike
- `inventory_crunch`: low stock with rising replenishment pressure

## Run the demo

### 1. Build and start the stack

```bash
docker compose up --build
```

On Windows PowerShell you can also use:

```powershell
.\scripts\start-demo.ps1
```

### 2. Open the dashboard

[http://localhost:8080](http://localhost:8080)

### 3. Optional direct APIs

- Ingestion API: [http://localhost:8001/docs](http://localhost:8001/docs)
- Decision Hub API: [http://localhost:8007/docs](http://localhost:8007/docs)

## Demo flow for presentation

1. Open the dashboard and introduce the platform architecture.
2. Trigger `steady_baseline` to establish the healthy retail baseline.
3. Trigger `promo_surge` to show promotion-led forecast growth.
4. Trigger `festival_peak` to show seasonal anomaly pressure.
5. Trigger `inventory_crunch` to show stockout-led replenishment urgency.
6. Explain how the decision hub combines forecast, anomaly, and stockout outputs.
7. Show how the agent orchestrator turns those outputs into specialist recommendations and a supervisor plan.

## Suggested industry explanation

RetailPulse ML is designed for retailers, supermarket chains, and e-commerce planning teams that want to forecast demand earlier, detect unusual sales behavior, avoid stockouts, and coordinate planning recommendations through an agentic workflow. Its Docker-based packaging makes deployment portable across developer laptops, test environments, and retail analytics sandboxes.

## Folder structure

```text
app/
  dashboard/
  agent_orchestrator/
  ingestion/
  intelligence_hub/
  models/
    anomaly/
    failure/
    quality/
  preprocessing/
  router/
  shared/
Dockerfile
docker-compose.yml
requirements.txt
README.md
```

## Notes

- The retail data is synthetic and tuned for a reliable classroom or viva demo.
- The ML services train lightweight in-memory models on startup using synthetic retail patterns.
- The agentic layer is deterministic and demo-safe, so it works without an external LLM API key.
- You can present the synthetic dataset as a privacy-safe stand-in for confidential sales records.
- If Docker image builds fail on your machine, check internet access for Python package downloads.
- Docker Desktop must be running with the Linux container engine enabled.

## CI/CD pipeline

The repository now includes GitHub Actions workflows under `.github/workflows/`.

### CI workflow

File: `.github/workflows/ci.yml`

The CI pipeline runs on every push and pull request and checks:

- Python dependency installation
- `python -m compileall app`
- `python scripts/ci_smoke_test.py`
- `docker compose config`
- `docker build -t retailpulse-ml-demo:ci .`

The smoke test executes the full retail logic in-process:

- loads a demo retail scenario
- preprocesses it
- runs the three ML services
- builds the intelligence hub summary
- runs the agent orchestrator
- verifies the final response shape

### CD workflow

File: `.github/workflows/cd.yml`

The CD pipeline runs on pushes to `main` and on manual trigger through `workflow_dispatch`.

It performs these steps:

- logs in to GitHub Container Registry using `GITHUB_TOKEN`
- builds the Docker image from the project `Dockerfile`
- publishes the image to `ghcr.io/<github-owner>/retailpulse-ml-demo`
- tags the image as `latest` and with the current commit SHA

### How to use the published image

After the CD workflow succeeds, the published image can be pulled with:

```bash
docker pull ghcr.io/<github-owner>/retailpulse-ml-demo:latest
```

If you want to use the same published image in another environment, replace the image value in your deployment compose file or CI environment with:

```text
ghcr.io/<github-owner>/retailpulse-ml-demo:latest
```
