# Human approval gate

Catalog entry: `agentic` pattern 12

Source heading: Human approval gate pattern

Pattern: **Draft -> explain risk -> request approval -> execute approved action -> record receipt**

## Scenario

An agent wants to publish a package release after tests pass but before human release approval.

## Flow

1. Draft the proposed action and explain risk.
2. Request approval for the exact action.
3. Execute only the approved operation.
4. Record approval, execution, and receipt.

## Agent Roles

- Drafting Agent
- Risk Explainer
- Approval Gate
- Executor
- Receipt Logger

## Policy Gates

- Dangerous actions execute only after explicit approval of the exact action.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py human-approval-gate
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py human-approval-gate --check
```

## Expected Output

The flow should produce `approval_gate_record` with these required fields:

- draft_action
- risk_explanation
- approval_request
- approved_action
- execution_result
- receipt

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
