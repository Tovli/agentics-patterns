# ComPilot loop auto-scheduling

Catalog entry: `agentic` pattern 16

Source heading: ComPilot loop auto-scheduling

Pattern: **Analyze loop -> propose schedule -> legality gate -> compile and benchmark -> feed back and keep best**

## Reference

This pattern is adapted from **ComPilot**: Agentic Auto-Scheduling: An Experimental Study of LLM-Guided Loop Optimization.

Paper: https://arxiv.org/abs/2511.00592

## Scenario

A compiler optimization harness must speed up a nested loop kernel by letting an LLM propose schedule transformations that a compiler validates for legality and benchmarks for real speedup before any schedule is accepted.

## Flow

1. Analyze the loop nest IR, data dependencies, and baseline performance.
2. Propose candidate schedule transformations such as tiling, fusion, interchange, and parallelization.
3. Check each proposed schedule for legality with dependence analysis before it runs.
4. Compile only legal schedules and benchmark real speedup against the baseline.
5. Feed measured results back to the proposer, iterate within budget, and keep the best legal schedule.

## Agent Roles

- Loop Analyzer
- Schedule Proposer
- Legality Checker
- Compiler Benchmarker
- Feedback Coordinator

## Policy Gates

- Only legal, dependence-preserving schedules may be compiled or executed.
- Speedup claims must come from real compiler benchmarks, not from model estimates.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py compilot-loop-autoscheduling
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py compilot-loop-autoscheduling --check
```

## Expected Output

The flow should produce `optimized_schedule_packet` with these required fields:

- baseline_profile
- proposed_transformations
- legality_verdict
- rejected_schedules
- speedup_evidence
- best_schedule
- iteration_summary

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
