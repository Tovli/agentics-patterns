# Default-deny tool broker

Catalog entry: `agentic` pattern 4

Source heading: Default-deny tool-broker pattern

Pattern: **Governed tool surface with explicit grants**

## Scenario

An agent requests shell, network, and file-write access while diagnosing a failing build.

## Flow

1. Declare requested tool, risk, timeout, and call budget.
2. Evaluate request against default-deny policy.
3. Require approval for dangerous or write-capable operations.
4. Execute only approved calls and record the audit trail.

## Agent Roles

- Tool Broker
- Policy Engine
- Agent Worker
- Audit Logger

## Policy Gates

- Network, shell, and file writes are denied unless explicitly granted.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py default-deny-tool-broker
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py default-deny-tool-broker --check
```

## Expected Output

The flow should produce `tool_broker_decision` with these required fields:

- tool_name
- needs
- risk
- approval
- timeout_ms
- max_calls_per_turn
- audit_record

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
