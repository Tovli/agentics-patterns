# Cognitive Metacognitive Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the cognitive agent loop from *AI Agents in Action, Second Edition* as a complete, runnable cross-cutting pattern in the repository.

**Architecture:** Extend the generator's `SPECS` source of truth with one cross-cutting pattern that composes perception, attention routing, strategy planning, execution, evaluation, confidence gating, stagnation recovery, knowledge-boundary awareness, and distilled memory. Regenerate the catalog artifacts, then add the six pattern-scoped Markdown role definitions and update the agent index. A focused catalog test locks the pattern's identity, workflow contract, book reference, and role files.

**Tech Stack:** Python 3 standard library, `unittest`, JSON flow contracts, Markdown agent definitions.

## Global Constraints

- Preserve the repository's deterministic `patterns/run_example.py` runtime and generated-artifact conventions.
- Use the canonical id `cognitive-metacognitive-loop` without taxonomy prefixes.
- Treat confidence gating, stagnation recovery, and knowledge-boundary awareness as non-bypassable policy gates.
- Store only distilled, non-sensitive learning after evaluation.
- Do not add runtime dependencies.

---

### Task 1: Cognitive Metacognitive Loop Pattern

**Files:**
- Modify: `tests/test_examples_catalog.py`
- Modify: `tools/generate_examples.py`
- Modify (generated): `patterns/catalog.json`
- Modify (generated): `patterns/README.md`
- Modify (generated): `EXAMPLE_STATUS.md`
- Create (generated): `patterns/cognitive-metacognitive-loop/README.md`
- Create (generated): `patterns/cognitive-metacognitive-loop/flow.json`
- Create (generated): `patterns/cognitive-metacognitive-loop/input.json`
- Create (generated): `patterns/cognitive-metacognitive-loop/expected-output.json`
- Create: `patterns/cognitive-metacognitive-loop/agents/perception-agent.md`
- Create: `patterns/cognitive-metacognitive-loop/agents/attention-router.md`
- Create: `patterns/cognitive-metacognitive-loop/agents/strategy-planner.md`
- Create: `patterns/cognitive-metacognitive-loop/agents/execution-agent.md`
- Create: `patterns/cognitive-metacognitive-loop/agents/evaluation-monitor.md`
- Create: `patterns/cognitive-metacognitive-loop/agents/memory-recorder.md`
- Modify: `patterns/AGENTS.md`

**Interfaces:**
- Consumes: `example(...) -> dict` and `build_output(flow: dict, input_payload: dict) -> dict`.
- Produces: catalog id `cognitive-metacognitive-loop`, artifact type `cognitive_cycle_record`, and six Markdown role files matching the catalog's `agents` labels.

- [ ] **Step 1: Write the failing catalog and role-definition test**

Add a focused test that raises the expected catalog size from 36 to 37, locates `cognitive-metacognitive-loop`, checks its exact workflow contract and source reference, and verifies these role files exist:

```python
def test_catalog_includes_cognitive_metacognitive_loop(self):
    catalog = self.load_catalog()
    entry = next(
        item for item in catalog["examples"]
        if item["id"] == "cognitive-metacognitive-loop"
    )
    self.assertEqual("agentic", entry["section"])
    self.assertEqual(17, entry["number"])
    self.assertEqual("cognitive_cycle_record", entry["output_contract"]["artifact_type"])
    self.assertIn("confidence_gate_decision", entry["output_contract"]["required_fields"])
    self.assertIn("knowledge_boundary", entry["output_contract"]["required_fields"])
    self.assertEqual("AI Agents in Action", entry["reference"]["system"])

    for filename in [
        "perception-agent.md",
        "attention-router.md",
        "strategy-planner.md",
        "execution-agent.md",
        "evaluation-monitor.md",
        "memory-recorder.md",
    ]:
        self.assertTrue(
            (PATTERNS / entry["id"] / "agents" / filename).is_file(),
            filename,
        )
```

- [ ] **Step 2: Run the focused test to verify it fails**

Run: `python -m unittest tests.test_examples_catalog.ExamplesCatalogTest.test_catalog_includes_cognitive_metacognitive_loop -v`

Expected: FAIL because `cognitive-metacognitive-loop` is not in `patterns/catalog.json`.

- [ ] **Step 3: Add the generator specification**

Append an `agentic` pattern numbered `17` to `SPECS` with:

```python
example(
    "cognitive-metacognitive-loop",
    "agentic",
    17,
    "Cognitive metacognitive loop",
    "Perceive -> attend -> select strategy -> execute -> evaluate -> adapt and remember",
    "A troubleshooting agent must avoid repeating a failed timeout fix and diagnose an intermittent deployment failure under load.",
    [
        "Perception Agent",
        "Attention Router",
        "Strategy Planner",
        "Execution Agent",
        "Evaluation Monitor",
        "Memory Recorder",
    ],
    [
        "Classify the task, ambiguity, complexity, and initial confidence in a shared cognitive workspace.",
        "Route attention to memory, planning, execution, evaluation, or metaplanning from active signals.",
        "Select a reasoning strategy that fits the task and excludes already failed approaches.",
        "Execute one bounded step and record evidence, relevance, quality, and tool outcomes.",
        "Evaluate progress, contradictions, confidence trend, stagnation, and knowledge coverage.",
        "Present only confidence-gated output; otherwise gather more evidence, pivot strategy, or signal uncertainty.",
        "Record a distilled non-sensitive lesson after the cycle terminates.",
    ],
    [
        "Responses below the presentation threshold must gather more evidence or explicitly signal uncertainty.",
        "Stagnation must trigger metaplanning and failed approaches must not be repeated.",
        "Outside the known knowledge boundary, the agent must degrade gracefully instead of guessing.",
        "Memory records only evaluated, distilled, non-sensitive lessons.",
    ],
    {
        "task": "diagnose intermittent deployment pipeline failures that occur only during high traffic",
        "prior_attempts": ["increased timeout thresholds without improvement"],
        "signals": ["high_traffic_correlation", "standard_timeout_fix_failed"],
        "available_strategies": ["fast_path", "react", "hypothesis_test", "tree_of_thought", "reflexion"],
        "confidence_thresholds": {"present": 0.6, "gather_more": 0.3},
        "budget": {"max_iterations": 5, "max_tool_calls": 10},
    },
    "cognitive_cycle_record",
    [
        "perception",
        "cognitive_workspace",
        "attention_route",
        "selected_strategy",
        "execution_evidence",
        "evaluation",
        "confidence_gate_decision",
        "stagnation_response",
        "knowledge_boundary",
        "memory_update",
    ],
    reference={
        "system": "AI Agents in Action",
        "title": "AI Agents in Action, Second Edition - chapter 10: Exploring the cognitive agent that thinks, monitors, and adapts",
        "author": "Micheal Lanham",
    },
)
```

- [ ] **Step 4: Regenerate deterministic pattern artifacts**

Run: `python tools/generate_examples.py`

Expected: `patterns/catalog.json` reports 37 examples and the new pattern directory contains its README, flow, input, and expected-output JSON files.

- [ ] **Step 5: Add the six role definitions and agent index row**

Each role file must use the existing frontmatter and prompt structure, state its boundary, name upstream/downstream roles, enforce the four policy gates, and hand off a structured result. Update `patterns/AGENTS.md` counts to 37 patterns, 167 references, and 147 unique labels, then add the new pattern row.

- [ ] **Step 6: Run the focused test to verify it passes**

Run: `python -m unittest tests.test_examples_catalog.ExamplesCatalogTest.test_catalog_includes_cognitive_metacognitive_loop -v`

Expected: PASS.

- [ ] **Step 7: Verify the runnable example**

Run: `python patterns/run_example.py cognitive-metacognitive-loop --check`

Expected: exit 0 and JSON output with `artifact_type` equal to `cognitive_cycle_record`.

- [ ] **Step 8: Run the complete test suite and generator drift check**

Run: `python -m unittest discover -s tests -v`

Expected: 7 tests pass with 0 failures.

Run: `$before = git diff --binary | Out-String; python tools/generate_examples.py; $after = git diff --binary | Out-String; if ($before -ne $after) { throw "generator drift detected" }`

Expected: rerunning the generator introduces no additional changes.

## Self-Review

- Spec coverage: the plan includes the book review result's missing cognitive architecture, all required runnable artifacts, policy gates, roles, index/catalog exposure, and tests.
- Placeholder scan: no TBD, TODO, deferred implementation, or unspecified error-handling steps remain.
- Type consistency: the id, artifact type, role labels, required fields, section, number, and reference values match across the test and generator specification.
