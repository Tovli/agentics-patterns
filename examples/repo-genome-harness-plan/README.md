# Repo genome to harness plan

Catalog entry: `agentic` pattern 2

Source heading: Repo Genome → Harness Plan pattern

Pattern: **Static repo genome -> recommended harness plan**

## Scenario

A meta-harness analyzes a repository without executing code and recommends the safest generated harness shape.

## Flow

1. Scan repository structure, languages, tests, and release surfaces without execution.
2. Score test confidence, MCP risk, and publish readiness.
3. Recommend agent topology, tool surface, memory namespaces, and approvals.
4. Emit a harness plan with constraints and required human gates.

## Agent Roles

- Repo Scanner
- Risk Profiler
- Topology Recommender
- Plan Writer

## Policy Gates

- Repo analysis does not execute repository code.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py repo-genome-harness-plan
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py repo-genome-harness-plan --check
```

## Expected Output

The flow should produce `repo_genome_plan` with these required fields:

- repo_profile
- agent_topology
- tool_surface
- risk_budget
- memory_namespaces
- recommended_vertical
- required_human_approvals

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
