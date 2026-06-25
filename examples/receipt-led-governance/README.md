# Receipt-led governance

Catalog entry: `agentic` pattern 10

Source heading: Receipt-led governance pattern

Pattern: **Every meaningful action writes a tamper-evident receipt**

## Scenario

A harness performs a dependency audit and records all material inputs, outputs, tools, and verdicts.

## Flow

1. Hash inputs and planned outputs before action.
2. Record agent, model, tool calls, cost, latency, risk, and verdict.
3. Hash-chain the receipt to the previous receipt.
4. Expose the receipt for audit and replay.

## Agent Roles

- Action Worker
- Tool Auditor
- Verifier
- Receipt Logger

## Policy Gates

- Material actions without receipts are treated as incomplete.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py receipt-led-governance
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py receipt-led-governance --check
```

## Expected Output

The flow should produce `governance_receipt` with these required fields:

- input_hash
- output_hash
- agent
- model
- tool_calls
- cost
- latency
- risk
- verdict
- previous_hash
- current_hash

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
