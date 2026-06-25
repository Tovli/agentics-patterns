# Planner executor verifier

Catalog entry: `agentic` pattern 3

Source heading: Planner–Executor–Verifier pattern

Pattern: **Planner -> executor -> verifier**

## Scenario

A coding harness must fix a bug while keeping the approver independent from the patch author.

## Flow

1. Planner decomposes the issue into small steps and acceptance checks.
2. Executor edits files or drafts the patch within the plan.
3. Verifier runs tests and reviews the diff independently.
4. Verifier rejects, requests retry, or approves with residual risk.

## Agent Roles

- Planner
- Executor
- Verifier

## Policy Gates

- The same agent cannot create and approve the output.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py planner-executor-verifier
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py planner-executor-verifier --check
```

## Expected Output

The flow should produce `verification_packet` with these required fields:

- plan
- patch_summary
- test_results
- diff_risks
- verifier_verdict

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
