# RetailPulse ML Architecture Notes

## System intent

The platform is structured like a production retail analytics stack rather than a single notebook. Each concern is isolated into a service so the demo reflects how ML is deployed in a commercial planning workflow, including an explicit agentic coordination layer.

## Data path

1. The dashboard selects or submits a retail scenario.
2. The ingestion service validates the sales observation payload.
3. The preprocessing service derives normalized retail features:
   - sales velocity
   - demand pressure
   - promotion lift
   - stock cover
   - replenishment gap
4. The router submits the processed record to three ML services.
5. The decision hub combines their outputs into one replenishment summary.
6. The agent orchestrator runs specialist planner agents:
   - demand sensing agent
   - inventory guardian agent
   - merchandising agent
   - supervisor agent
7. The dashboard shows the forecast summary, agent trace, and replenishment timeline.

## Model roles

- Demand model: random forest regressor for short-term unit forecasting.
- Demand anomaly model: isolation forest for unusual retail behavior.
- Stockout model: logistic classifier for replenishment urgency.

## Agent roles

- Demand sensing agent: interprets forecast strength and expected sales acceleration.
- Inventory guardian agent: evaluates stock cover and replenishment urgency.
- Merchandising agent: examines whether promotions or traffic distort the demand signal.
- Supervisor agent: merges agent opinions into one execution plan.

## Why this design is industry-oriented

- Independent model deployment supports versioning and scaling.
- API isolation allows teams to update one model without changing the others.
- Planner-facing aggregation avoids showing raw model scores without action context.
- The agent layer demonstrates how model outputs can be operationalized into coordinated planning actions.
- Docker Compose provides an accessible local analogue to container orchestration.
