# B2B pipeline

Catalog entry: `catalog` pattern 16

Source heading: `sales` — B2B Pipeline Pattern

Pattern: **Prospect -> qualify -> demo -> close honestly**

## Scenario

A sales team evaluates whether a healthcare prospect is ready for a technical demo.

## Flow

1. Research account context and buying signals.
2. Score qualification and list missing facts.
3. Create a personalized demo path.
4. Handle objections within negotiation boundaries.
5. Identify pipeline bottleneck and next step.

## Agent Roles

- Prospector
- Qualifier
- Demo Coach
- Closer
- Pipeline Reporter

## Policy Gates

- No-stretch policy: never exaggerate product capabilities.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py sales-b2b-pipeline
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py sales-b2b-pipeline --check
```

## Expected Output

The flow should produce `deal_brief` with these required fields:

- account_context
- qualification_score
- missing_facts
- demo_angle
- objections
- next_step
- go_no_go

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
