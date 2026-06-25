# Opt-in self-evolution

Catalog entry: `agentic` pattern 13

Source heading: Self-evolution pattern, but opt-in only

Pattern: **Measure baseline -> small exploration -> evaluate -> adopt if better -> rollback on regression**

## Scenario

A harness tests a routing-weight change against historical tasks before adopting it.

## Flow

1. Measure current baseline on declared metrics.
2. Run a small opt-in exploration in sandbox.
3. Evaluate against baseline and regression thresholds.
4. Adopt only if better, otherwise preserve failure learning.
5. Write rollback path and audit log.

## Agent Roles

- Baseline Measurer
- Experiment Runner
- Evaluator
- Rollback Manager
- Audit Logger

## Policy Gates

- Adaptive tuning is opt-in and rollback-ready.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py opt-in-self-evolution
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py opt-in-self-evolution --check
```

## Expected Output

The flow should produce `self_evolution_audit` with these required fields:

- baseline
- experiment
- evaluation
- adopt_reject_decision
- rollback_path
- audit_log

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
