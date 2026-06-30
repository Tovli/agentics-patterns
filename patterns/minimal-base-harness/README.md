# Minimal base harness

Catalog entry: `catalog` pattern 0

Source heading: `minimal` — Base Harness Pattern

Pattern: **Kernel smoke-test scaffold**

## Scenario

A new package scaffold needs a single doctor command before any domain agents are added.

## Flow

1. Initialize the harness workspace.
2. Load the kernel and host adapter.
3. Check MCP wiring, memory backend, and host adapter health.
4. Return one PASS/FAIL report with remediation hints.

## Agent Roles

- Harness Doctor

## Policy Gates

- No domain action is allowed from the minimal scaffold.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py minimal-base-harness
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py minimal-base-harness --check
```

## Expected Output

The flow should produce `doctor_report` with these required fields:

- overall_status
- checks
- failed_checks
- remediation

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
