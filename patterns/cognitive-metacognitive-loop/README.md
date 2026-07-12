# Cognitive metacognitive loop

Catalog entry: `agentic` pattern 17

Source heading: Cognitive metacognitive loop

Pattern: **Perceive -> attend -> select strategy -> execute -> evaluate -> adapt and remember**

## Reference

This pattern is adapted from **AI Agents in Action**: AI Agents in Action, Second Edition - chapter 10: Exploring the cognitive agent that thinks, monitors, and adapts.

## Scenario

A troubleshooting agent must avoid repeating a failed timeout fix and diagnose an intermittent deployment failure under load.

## Flow

1. Classify the task, ambiguity, complexity, and initial confidence in a shared cognitive workspace.
2. Route attention to memory, planning, execution, evaluation, or metaplanning from active signals.
3. Select a reasoning strategy that fits the task and excludes already failed approaches.
4. Execute one bounded step and record evidence, relevance, quality, and tool outcomes.
5. Evaluate progress, contradictions, confidence trend, stagnation, and knowledge coverage.
6. Present only confidence-gated output; otherwise gather more evidence, pivot strategy, or signal uncertainty.
7. Record a distilled non-sensitive lesson after the cycle terminates.

## Agent Roles

- Perception Agent
- Attention Router
- Strategy Planner
- Execution Agent
- Evaluation Monitor
- Memory Recorder

## Policy Gates

- Responses below the presentation threshold must gather more evidence or explicitly signal uncertainty.
- Stagnation must trigger metaplanning and failed approaches must not be repeated.
- Outside the known knowledge boundary, the agent must degrade gracefully instead of guessing.
- Memory records only evaluated, distilled, non-sensitive lessons.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Deterministic Example Fixture

`flow.json`'s `example_output` is a deterministic fixture and validator input; it is not proof that a live cognitive cycle executed.

## Run

From this directory:

```bash
python ../run_example.py cognitive-metacognitive-loop
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py cognitive-metacognitive-loop --check
```

## Expected Output

The flow should produce `cognitive_cycle_record` with these required fields:

- perception
- cognitive_workspace
- attention_route
- selected_strategy
- execution_evidence
- evaluation
- confidence_gate_decision
- stagnation_response
- knowledge_boundary
- memory_update

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
