# Memory distillation

Catalog entry: `agentic` pattern 7

Source heading: Memory distillation pattern

Pattern: **Retrieve -> judge -> distill -> consolidate**

## Scenario

A coding harness stores only durable lessons from a failed dependency upgrade, not the full noisy trace.

## Flow

1. Retrieve relevant prior task traces and lessons.
2. Judge whether the current trajectory produced useful learning.
3. Distill durable patterns, failures, and verified decisions.
4. Consolidate into namespace-specific memory with decay metadata.

## Agent Roles

- Memory Retriever
- Trajectory Judge
- Distiller
- Consolidator

## Policy Gates

- Do not store raw sensitive task history when a distilled lesson is sufficient.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py memory-distillation
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py memory-distillation --check
```

## Expected Output

The flow should produce `memory_update_packet` with these required fields:

- retrieved_context
- judge_verdict
- distilled_lesson
- namespace
- decay_policy
- excluded_raw_data

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
