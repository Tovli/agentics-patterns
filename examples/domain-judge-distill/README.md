# Domain-specific judge and distill

Catalog entry: `agentic` pattern 8

Source heading: Domain-specific Judge / Distill pattern

Pattern: **Domain judge -> domain distiller -> reusable lesson**

## Scenario

Different verticals evaluate success with their own domain-specific outcome criteria.

## Flow

1. Apply domain-specific success criteria to the completed run.
2. Separate domain verdict from generic task completion.
3. Distill a reusable lesson for that vertical.
4. Store the lesson in the correct namespace with evidence.

## Agent Roles

- Domain Judge
- Distill Provider
- Memory Curator

## Policy Gates

- Generic success metrics cannot replace domain-specific judgment.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py domain-judge-distill
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py domain-judge-distill --check
```

## Expected Output

The flow should produce `domain_learning_packet` with these required fields:

- domain_verdict
- metric_evidence
- distilled_lesson
- namespace
- reuse_conditions

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
