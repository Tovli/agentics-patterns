# Algorithmic control plane

Catalog entry: `agentic` pattern 1

Source heading: Algorithmic control-plane pattern

Pattern: **Model proposes; harness decides; algorithms verify**

## Scenario

A user asks the harness to update dependencies, but confidence, risk, cost, and verification gates must pass first.

## Flow

1. Classify intent, risk, expected cost, and verification strategy.
2. Create a plan and route each step to the right worker or model.
3. Broker tool access under policy.
4. Verify outputs independently before applying results.
5. Write receipt and memory update after verified completion.

## Agent Roles

- Intent Classifier
- Planner
- Router
- Tool Broker
- Verifier
- Receipt Logger

## Policy Gates

- Execution is blocked unless confidence, risk, cost, and verification gates pass.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py algorithmic-control-plane
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py algorithmic-control-plane --check
```

## Expected Output

The flow should produce `control_plane_receipt` with these required fields:

- intent
- risk
- plan
- tool_grants
- verification
- receipt_hash
- result

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
