# ML lifecycle

Catalog entry: `catalog` pattern 11

Source heading: `ai` — ML Lifecycle Pattern

Pattern: **Data -> train -> evaluate -> deploy behind guardrails**

## Scenario

An ML team wants to ship a classifier for support-ticket routing only if it beats the baseline across slices.

## Flow

1. Build a dataset card with provenance and limits.
2. Run reproducible training or fine-tuning.
3. Compare against baseline, subgroup slices, and failure cases.
4. Deploy only if evaluation gates pass.
5. Monitor post-deploy drift and regressions.

## Agent Roles

- Data Curator
- Trainer
- Evaluator
- Deployer
- Drift Monitor

## Policy Gates

- Evaluator is independent; training metrics alone cannot drive deployment.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py ai-ml-lifecycle
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py ai-ml-lifecycle --check
```

## Expected Output

The flow should produce `eval_report` with these required fields:

- dataset_summary
- baseline_delta
- metrics
- subgroup_performance
- risks
- ship_no_ship_decision
- deployment_guardrails

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
