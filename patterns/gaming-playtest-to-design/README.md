# Playtest-to-design

Catalog entry: `catalog` pattern 15

Source heading: `gaming` — Playtest-to-Design Pattern

Pattern: **Read playtest -> critique balance -> model economy -> preserve narrative**

## Scenario

A playtest shows players abandoning the second dungeon while economy telemetry shows gold inflation.

## Flow

1. Extract signal from telemetry, feedback, and design docs.
2. Identify mechanic imbalance and propose changes.
3. Check loops, sinks, inflation, and progression.
4. Review lore and story consistency.
5. Write a build-to-build design diff.

## Agent Roles

- Playtest Reader
- Balance Critic
- Economy Modeler
- Narrative Keeper
- Design Diff Writer

## Policy Gates

- Player anecdotes are separated from telemetry-backed findings.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py gaming-playtest-to-design
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py gaming-playtest-to-design --check
```

## Expected Output

The flow should produce `playtest_recap` with these required fields:

- player_pain_points
- balance_issues
- economy_risks
- narrative_conflicts
- proposed_changes
- build_to_build_diff

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
