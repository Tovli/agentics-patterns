# CI agent

Catalog entry: `agentic` pattern 11

Source heading: CI agent pattern

Pattern: **Trigger -> bounded task -> GitHub API tools -> PR/comment/status output**

## Scenario

A GitHub Action reviews a pull request and posts a bounded genome report without arbitrary shell access.

## Flow

1. Start from a CI trigger with declared permissions.
2. Run a bounded, non-interactive task.
3. Use GitHub API tools instead of arbitrary shell by default.
4. Post PR comment, status, or release note output.

## Agent Roles

- Trigger Handler
- Bounded Task Runner
- GitHub Tool Broker
- Status Reporter

## Policy Gates

- No arbitrary shell or broad token permissions in CI by default.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py ci-agent
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py ci-agent --check
```

## Expected Output

The flow should produce `ci_agent_output` with these required fields:

- trigger
- bounded_task
- tool_permissions
- findings
- posted_status
- residual_risk

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
