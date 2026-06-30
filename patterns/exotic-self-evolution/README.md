# Self-evolution

Catalog entry: `catalog` pattern 19

Source heading: `exotic` — Self-Evolution Pattern

Pattern: **Hypothesize -> sandbox experiment -> record -> maybe federate**

## Scenario

A harness proposes changing retrieval weights after repeated low-confidence answers.

## Flow

1. Propose a falsifiable improvement with a declared metric.
2. Run the experiment only in a sandbox.
3. Write success or failure to a witness-signed evolution log.
4. Preserve failed experiments as learning.
5. Federate only vetted, non-sensitive improvements.

## Agent Roles

- Hypothesizer
- Experimenter
- Witness Logger
- Federator

## Policy Gates

- Self-evolution is opt-in and sandboxed.
- Production self-mutation and proxy-metric optimization require review.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py exotic-self-evolution
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py exotic-self-evolution --check
```

## Expected Output

The flow should produce `evolution_record` with these required fields:

- hypothesis
- metric
- sandbox_config
- result
- keep_kill_decision
- rollback_path
- federation_eligibility

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
