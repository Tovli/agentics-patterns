# Controlled swarm

Catalog entry: `catalog` pattern 12

Source heading: `agentics` — Controlled Swarm Pattern

Pattern: **Orchestrator -> planner -> workers -> critic**

## Scenario

A harness must evaluate three independent integration options without exceeding a fixed budget.

## Flow

1. Set objective, budget, max depth, and stopping condition.
2. Decompose work into dependency-aware tasks.
3. Run bounded worker tasks.
4. Review outputs through a critic before landing them.
5. Decide whether to continue, retry, or stop and store distilled lessons.

## Agent Roles

- Orchestrator
- Planner
- Worker Pool
- Critic
- Memory Curator

## Policy Gates

- No run starts without budget, max depth, stopping condition, and critic gate.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py agentics-controlled-swarm
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py agentics-controlled-swarm --check
```

## Expected Output

The flow should produce `run_report` with these required fields:

- goal
- plan
- task_graph
- worker_outputs
- critic_findings
- final_result
- cost
- unresolved_issues

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
