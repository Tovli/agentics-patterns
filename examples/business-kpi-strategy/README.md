# KPI-grounded strategy

Catalog entry: `catalog` pattern 7

Source heading: `business` — KPI-Grounded Strategy Pattern

Pattern: **Analyze -> choose bet -> operationalize**

## Scenario

A business unit must choose one quarterly growth bet after pipeline conversion slowed.

## Flow

1. Turn current metrics into findings.
2. Choose one strategic bet and state trade-offs.
3. Translate the bet into owners, actions, milestones, and KPIs.
4. Review feasibility and metric alignment.

## Agent Roles

- Analyst
- Strategist
- Ops Coordinator
- Feasibility Reviewer

## Policy Gates

- Strategic recommendations must tie directly to metrics.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py business-kpi-strategy
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py business-kpi-strategy --check
```

## Expected Output

The flow should produce `quarterly_plan` with these required fields:

- findings
- strategic_choice
- rejected_alternatives
- action_owners
- kpis
- milestones
- review_cadence

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
