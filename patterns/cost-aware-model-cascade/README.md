# Cost-aware model cascade

Catalog entry: `agentic` pattern 9

Source heading: Cost-aware model cascade pattern

Pattern: **Cheap draft -> verify -> stronger retry only if needed -> record cost and quality**

## Scenario

A CI triage agent drafts issue labels cheaply and escalates only uncertain cases to a stronger model.

## Flow

1. Attempt the task with the cheapest suitable model.
2. Verify confidence, quality, and safety.
3. Escalate to a stronger model only when verification fails or uncertainty is high.
4. Record cost, latency, and quality outcome.

## Agent Roles

- Cheap Drafter
- Verifier
- Escalation Router
- Cost Logger

## Policy Gates

- Escalation is evidence-driven, not automatic.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py cost-aware-model-cascade
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py cost-aware-model-cascade --check
```

## Expected Output

The flow should produce `model_cascade_record` with these required fields:

- initial_model
- verification_result
- escalated_model
- cost
- latency
- quality_outcome

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
