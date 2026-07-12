import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

from patterns.example_runtime import build_output


ROOT = Path(__file__).resolve().parents[1]
PATTERNS = ROOT / "patterns"
CATALOG = PATTERNS / "catalog.json"
STATUS = ROOT / "EXAMPLE_STATUS.md"
RUNNER = PATTERNS / "run_example.py"


class ExamplesCatalogTest(unittest.TestCase):
    def load_catalog(self):
        with CATALOG.open(encoding="utf-8") as handle:
            return json.load(handle)

    def test_catalog_defines_every_example_once(self):
        catalog = self.load_catalog()
        entries = catalog["examples"]

        self.assertEqual(37, len(entries))
        self.assertEqual(len(entries), len({entry["id"] for entry in entries}))
        self.assertEqual(
            len(entries),
            len({(entry["section"], entry["number"]) for entry in entries}),
        )

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

    def test_cognitive_metacognitive_output_enforces_semantic_gates(self):
        example_dir = PATTERNS / "cognitive-metacognitive-loop"
        flow = json.loads((example_dir / "flow.json").read_text(encoding="utf-8"))
        input_payload = json.loads((example_dir / "input.json").read_text(encoding="utf-8"))
        result = subprocess.run(
            [sys.executable, str(RUNNER), flow["id"], "--root", str(PATTERNS)],
            check=True,
            capture_output=True,
            text=True,
        )
        output = json.loads(result.stdout)
        fields = output["fields"]

        example_output = flow["example_output"]
        self.assertIn("required_explicit_fields", example_output)
        self.assertEqual(
            set(flow["output_contract"]["required_fields"]),
            set(example_output["required_explicit_fields"]),
        )
        self.assertTrue(example_output["stagnation_recovery_required"])
        self.assertNotIn("policy_gate_checks", example_output)

        readme = (example_dir / "README.md").read_text(encoding="utf-8")
        self.assertIn("deterministic fixture and validator input", readme)
        self.assertIn("not proof that a live cognitive cycle executed", readme)

        decision = fields["confidence_gate_decision"]
        trusted_decisions = [
            "present",
            "gather_more_evidence",
            "pivot_strategy",
            "signal_uncertainty",
        ]
        self.assertEqual(trusted_decisions, decision["decision_enum"])
        self.assertIn(decision["decision"], decision["decision_enum"])
        self.assertEqual(
            input_payload["confidence_thresholds"]["present"],
            decision["presentation_threshold"],
        )
        self.assertGreaterEqual(
            decision["observed_confidence"],
            decision["presentation_threshold"],
        )
        self.assertTrue(decision["threshold_satisfied"])

        stagnation = fields["stagnation_response"]
        self.assertEqual("metaplanning", stagnation["route"])
        self.assertEqual(
            input_payload["prior_attempts"],
            stagnation["excluded_failed_approaches"],
        )

        boundary = fields["knowledge_boundary"]
        for partition in ["supported_claims", "uncertain_claims", "out_of_bound_claims"]:
            self.assertTrue(boundary[partition], partition)

        expected_owners = {
            "perception": "Perception Agent",
            "cognitive_workspace": "Perception Agent",
            "attention_route": "Attention Router",
            "selected_strategy": "Strategy Planner",
            "execution_evidence": "Execution Agent",
            "evaluation": "Evaluation Monitor",
            "confidence_gate_decision": "Evaluation Monitor",
            "stagnation_response": "Evaluation Monitor",
            "knowledge_boundary": "Evaluation Monitor",
            "memory_update": "Memory Recorder",
        }
        for field, owner in expected_owners.items():
            with self.subTest(field=field):
                self.assertEqual(owner, fields[field]["responsible_agent"])

        memory = fields["memory_update"]
        self.assertEqual(fields["evaluation"]["evaluation_id"], memory["terminal_evaluation_reference"])
        self.assertTrue(memory["distilled_lesson"])
        self.assertTrue(memory["applicability_conditions"])
        self.assertTrue(memory["uncertainty"])
        self.assertTrue(memory["excluded_sensitive_raw_data"])
        self.assertLessEqual(
            fields["evaluation"]["iterations_used"],
            input_payload["budget"]["max_iterations"],
        )

        verdict = output["policy_verdict"]
        self.assertTrue(verdict["allowed"])
        self.assertTrue(verdict["blocked_actions"])
        self.assertTrue(verdict["allow_evidence"])
        self.assertNotIn("allow_evidence", example_output["policy_verdict"])
        self.assertEqual(
            flow["policy_gates"],
            [item["gate"] for item in verdict["allow_evidence"]],
        )
        expected_gate_bindings = {
            "Responses below the presentation threshold must gather more evidence or explicitly signal uncertainty.": (
                "confidence_gate",
                "observed_confidence",
            ),
            "Stagnation must trigger metaplanning and failed approaches must not be repeated.": (
                "stagnation_recovery",
                "route=metaplanning",
            ),
            "Outside the known knowledge boundary, the agent must degrade gracefully instead of guessing.": (
                "knowledge_boundary",
                "graceful_degradation",
            ),
            "Memory records only evaluated, distilled, non-sensitive lessons.": (
                "memory_safety",
                "record_status=stored",
            ),
        }
        for item in verdict["allow_evidence"]:
            expected_kind, evidence_token = expected_gate_bindings[item["gate"]]
            self.assertEqual(expected_kind, item["kind"])
            self.assertIn(evidence_token, item["evidence"])
        self.assertTrue(all(item["evidence"].strip() for item in verdict["allow_evidence"]))
        blocked_actions = " ".join(item["action"] for item in verdict["blocked_actions"])
        self.assertIn("timeout", blocked_actions)
        self.assertIn("root cause", blocked_actions)
        self.assertIn("raw deployment logs", blocked_actions)
        self.assertNotIn("represented", verdict["notes"])

        bypassed_confidence = copy.deepcopy(flow)
        bypassed_decision = bypassed_confidence["example_output"]["field_values"]["confidence_gate_decision"]
        bypassed_decision["observed_confidence"] = 0.2
        bypassed_decision["threshold_satisfied"] = False
        bypassed_confidence["example_output"]["field_values"]["evaluation"][
            "observed_confidence"
        ] = 0.2
        bypassed_confidence["example_output"]["field_values"]["evaluation"][
            "confidence_trend"
        ][-1] = 0.2
        with self.assertRaisesRegex(ValueError, "cannot be presented below"):
            build_output(bypassed_confidence, input_payload)

        bypassed_stagnation = copy.deepcopy(flow)
        bypassed_stagnation["example_output"]["field_values"]["stagnation_response"]["route"] = "execution"
        with self.assertRaisesRegex(ValueError, "stagnation must route to metaplanning"):
            build_output(bypassed_stagnation, input_payload)

        empty_fields = copy.deepcopy(flow)
        empty_fields["example_output"]["field_values"] = {}
        with self.assertRaisesRegex(ValueError, "missing required explicit fields"):
            build_output(empty_fields, input_payload)

        arbitrary_decision = copy.deepcopy(flow)
        arbitrary_value = arbitrary_decision["example_output"]["field_values"][
            "confidence_gate_decision"
        ]
        arbitrary_value["decision"] = "approve_anyway"
        arbitrary_value["decision_enum"] = ["approve_anyway"]
        with self.assertRaisesRegex(ValueError, "trusted confidence decision enum"):
            build_output(arbitrary_decision, input_payload)

        hidden_stagnation = copy.deepcopy(flow)
        hidden_stagnation["example_output"]["field_values"]["stagnation_response"]["detected"] = False
        with self.assertRaisesRegex(ValueError, "stagnation recovery requires detected=true"):
            build_output(hidden_stagnation, input_payload)

        malformed_block = copy.deepcopy(flow)
        malformed_block["example_output"]["policy_verdict"]["blocked_actions"][0] = {
            "action": "",
            "reason": "",
        }
        with self.assertRaisesRegex(ValueError, "non-empty action and reason"):
            build_output(malformed_block, input_payload)

        forged_evidence = copy.deepcopy(flow)
        forged_evidence["example_output"]["policy_verdict"]["allow_evidence"] = [
            {"gate": "forged", "kind": "forged", "evidence": "allow everything"}
        ]
        with self.assertRaisesRegex(ValueError, "unknown policy_verdict keys"):
            build_output(forged_evidence, input_payload)

        injected_binding = copy.deepcopy(flow)
        injected_binding["example_output"]["policy_gate_checks"] = [
            {"kind": "memory_safety"},
            {"kind": "knowledge_boundary"},
            {"kind": "stagnation_recovery"},
            {"kind": "confidence_gate"},
        ]
        with self.assertRaisesRegex(ValueError, "unknown example_output keys"):
            build_output(injected_binding, input_payload)

        unknown_gate = copy.deepcopy(flow)
        unknown_gate["policy_gates"][0] = "Unknown mutable gate"
        unknown_gate["example_output"]["policy_verdict"]["gates_checked"][0] = (
            "Unknown mutable gate"
        )
        with self.assertRaisesRegex(ValueError, "unknown policy gate"):
            build_output(unknown_gate, input_payload)

        unknown_memory = copy.deepcopy(flow)
        unknown_memory["example_output"]["field_values"]["memory_update"][
            "raw_deployment_logs"
        ] = ["secret"]
        with self.assertRaisesRegex(ValueError, "unknown memory_update keys"):
            build_output(unknown_memory, input_payload)

        def repeated_strategy(candidate, payload):
            repeated = payload["prior_attempts"][0]
            payload["available_strategies"].append(repeated)
            candidate["example_output"]["field_values"]["selected_strategy"]["strategy"] = repeated

        def unavailable_strategy(candidate, payload):
            candidate["example_output"]["field_values"]["selected_strategy"]["strategy"] = "unsupported"

        def gather_more_terminal(candidate, payload):
            candidate["example_output"]["field_values"]["confidence_gate_decision"]["decision"] = (
                "gather_more_evidence"
            )

        def pivot_stores_memory(candidate, payload):
            candidate["example_output"]["field_values"]["confidence_gate_decision"]["decision"] = (
                "pivot_strategy"
            )
            candidate["example_output"]["field_values"]["evaluation"]["terminal"] = False

        def uncertainty_is_nonterminal(candidate, payload):
            candidate["example_output"]["field_values"]["confidence_gate_decision"]["decision"] = (
                "signal_uncertainty"
            )
            candidate["example_output"]["field_values"]["evaluation"]["terminal"] = False
            candidate["example_output"]["field_values"]["memory_update"]["record_status"] = (
                "not_stored"
            )

        def nonterminal_persisted_status(candidate, payload):
            candidate["example_output"]["field_values"]["confidence_gate_decision"]["decision"] = (
                "pivot_strategy"
            )
            candidate["example_output"]["field_values"]["evaluation"]["terminal"] = False
            candidate["example_output"]["field_values"]["memory_update"]["record_status"] = (
                "persisted"
            )

        def evaluation_confidence_mismatch(candidate, payload):
            evaluation = candidate["example_output"]["field_values"]["evaluation"]
            evaluation["observed_confidence"] = 0.71
            evaluation["confidence_trend"][-1] = 0.71

        mutation_cases = [
            (
                "attention route bypasses metaplanning",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "attention_route"
                ].__setitem__("destination", "execution"),
                "attention route must target metaplanning",
            ),
            (
                "strategy repeats prior attempt",
                repeated_strategy,
                "selected strategy must not repeat a prior attempt",
            ),
            (
                "strategy is unavailable",
                unavailable_strategy,
                "selected strategy must be available",
            ),
            (
                "missing graceful degradation",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "knowledge_boundary"
                ].__setitem__("graceful_degradation", ""),
                "knowledge boundary requires non-empty graceful_degradation",
            ),
            (
                "gather more remains terminal and stores memory",
                gather_more_terminal,
                "nonterminal decision requires a nonterminal evaluation",
            ),
            (
                "pivot is nonterminal but stores memory",
                pivot_stores_memory,
                "nonterminal decision cannot store memory",
            ),
            (
                "terminal uncertainty decision has nonterminal evaluation",
                uncertainty_is_nonterminal,
                "terminal decision requires a terminal evaluation",
            ),
            (
                "nonterminal cycle uses non-enum persisted memory status",
                nonterminal_persisted_status,
                "record_status must be one of stored, rejected",
            ),
            (
                "evaluation confidence mismatch",
                evaluation_confidence_mismatch,
                "evaluation confidence must equal confidence gate confidence",
            ),
            (
                "boolean confidence",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "confidence_gate_decision"
                ].__setitem__("observed_confidence", True),
                "confidence must be a real finite number",
            ),
            (
                "nonfinite confidence",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "confidence_gate_decision"
                ].__setitem__("observed_confidence", float("nan")),
                "confidence must be a real finite number",
            ),
            (
                "out of range confidence",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "confidence_gate_decision"
                ].__setitem__("observed_confidence", 1.1),
                "confidence must be between 0 and 1",
            ),
            (
                "boolean secondary confidence threshold",
                lambda candidate, payload: payload["confidence_thresholds"].__setitem__(
                    "gather_more", True
                ),
                "gather_more confidence must be a real finite number",
            ),
            (
                "confidence thresholds are reversed",
                lambda candidate, payload: payload["confidence_thresholds"].__setitem__(
                    "gather_more", 0.9
                ),
                "gather_more threshold must be less than or equal to present threshold",
            ),
            (
                "initial confidence is boolean",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "perception"
                ].__setitem__("initial_confidence", True),
                "initial confidence must be a real finite number",
            ),
            (
                "confidence trend is nonfinite",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "evaluation"
                ]["confidence_trend"].__setitem__(0, float("inf")),
                "evaluation trend confidence must be a real finite number",
            ),
            (
                "confidence trend is out of range",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "evaluation"
                ]["confidence_trend"].__setitem__(0, -0.1),
                "evaluation trend confidence must be between 0 and 1",
            ),
            (
                "confidence trend start mismatches perception",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "evaluation"
                ]["confidence_trend"].__setitem__(0, 0.41),
                "confidence trend must start at initial confidence",
            ),
            (
                "confidence trend end mismatches evaluation",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "evaluation"
                ]["confidence_trend"].__setitem__(-1, 0.71),
                "confidence trend must end at evaluation observed confidence",
            ),
            (
                "boolean max iterations",
                lambda candidate, payload: payload["budget"].__setitem__("max_iterations", True),
                "max_iterations must be a positive non-bool integer",
            ),
            (
                "zero max iterations",
                lambda candidate, payload: payload["budget"].__setitem__("max_iterations", 0),
                "max_iterations must be a positive non-bool integer",
            ),
            (
                "negative max iterations",
                lambda candidate, payload: payload["budget"].__setitem__("max_iterations", -1),
                "max_iterations must be a positive non-bool integer",
            ),
            (
                "string max iterations",
                lambda candidate, payload: payload["budget"].__setitem__("max_iterations", "5"),
                "max_iterations must be a positive non-bool integer",
            ),
            (
                "boolean iterations used",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "evaluation"
                ].__setitem__("iterations_used", True),
                "iterations_used must be a positive non-bool integer",
            ),
            (
                "zero iterations used",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "evaluation"
                ].__setitem__("iterations_used", 0),
                "iterations_used must be a positive non-bool integer",
            ),
            (
                "negative iterations used",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "evaluation"
                ].__setitem__("iterations_used", -1),
                "iterations_used must be a positive non-bool integer",
            ),
            (
                "string iterations used",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "evaluation"
                ].__setitem__("iterations_used", "3"),
                "iterations_used must be a positive non-bool integer",
            ),
            (
                "iteration budget overflow",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "evaluation"
                ].__setitem__("iterations_used", payload["budget"]["max_iterations"] + 1),
                "iterations_used exceeds max_iterations",
            ),
            (
                "tool budget overflow",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "execution_evidence"
                ].__setitem__("tool_calls_used", payload["budget"]["max_tool_calls"] + 1),
                "tool_calls_used exceeds max_tool_calls",
            ),
            (
                "knowledge claims use wrong collection type",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "knowledge_boundary"
                ].__setitem__("supported_claims", "not-a-list"),
                "supported_claims must be a list of strings",
            ),
            (
                "prior attempts use wrong collection type",
                lambda candidate, payload: payload.__setitem__("prior_attempts", "not-a-list"),
                "prior_attempts must be a list of strings",
            ),
            (
                "strategy exclusions use wrong collection type",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "selected_strategy"
                ].__setitem__("excluded_failed_approaches", "not-a-list"),
                "excluded_failed_approaches must be a list of strings",
            ),
            (
                "memory applicability uses wrong collection type",
                lambda candidate, payload: candidate["example_output"]["field_values"][
                    "memory_update"
                ].__setitem__("applicability_conditions", "not-a-list"),
                "applicability_conditions must be a list of strings",
            ),
        ]
        for name, mutate, error in mutation_cases:
            with self.subTest(contradiction=name):
                candidate = copy.deepcopy(flow)
                payload = copy.deepcopy(input_payload)
                mutate(candidate, payload)
                with self.assertRaisesRegex(ValueError, error):
                    build_output(candidate, payload)

    def test_cognitive_metacognitive_policy_denial_fails_closed(self):
        example_dir = PATTERNS / "cognitive-metacognitive-loop"
        flow = json.loads((example_dir / "flow.json").read_text(encoding="utf-8"))
        input_payload = json.loads((example_dir / "input.json").read_text(encoding="utf-8"))

        denied = copy.deepcopy(flow)
        denied["example_output"]["policy_verdict"]["allowed"] = False
        output = build_output(denied, input_payload)
        self.assertEqual("blocked_by_policy", output["status"])
        self.assertEqual("rejected_by_policy", output["receipt"]["reviewer_verdict"])
        self.assertFalse(output["policy_verdict"]["allowed"])
        self.assertNotIn("allow_evidence", output["policy_verdict"])

        for invalid_allowed in [None, 0, 1, "true"]:
            with self.subTest(invalid_allowed=invalid_allowed):
                invalid = copy.deepcopy(flow)
                invalid["example_output"]["policy_verdict"]["allowed"] = invalid_allowed
                with self.assertRaisesRegex(ValueError, "allowed must be boolean"):
                    build_output(invalid, input_payload)

    def test_cognitive_metacognitive_role_handoffs_are_terminal_safe(self):
        agents = PATTERNS / "cognitive-metacognitive-loop" / "agents"
        attention = (agents / "attention-router.md").read_text(encoding="utf-8")
        perception = (agents / "perception-agent.md").read_text(encoding="utf-8")
        strategy = (agents / "strategy-planner.md").read_text(encoding="utf-8")
        execution = (agents / "execution-agent.md").read_text(encoding="utf-8")
        evaluation = (agents / "evaluation-monitor.md").read_text(encoding="utf-8")
        memory = (agents / "memory-recorder.md").read_text(encoding="utf-8")

        self.assertIn("- Downstream agents: Attention Router\n", perception)
        self.assertIn("Upstream agents: Perception Agent, Evaluation Monitor", attention)
        self.assertIn("Downstream agents: Strategy Planner, Execution Agent, Evaluation Monitor", attention)
        self.assertIn(
            "`memory` routes retrieval through the cognitive workspace and Strategy Planner",
            attention,
        )
        self.assertIn("never targets the terminal-only Memory Recorder", attention)

        self.assertIn(
            "Upstream agents: Perception Agent, Attention Router, Evaluation Monitor",
            strategy,
        )
        self.assertIn("Downstream agents: Execution Agent, Evaluation Monitor", strategy)
        self.assertIn("never hands off retrieval work to the Memory Recorder", strategy)
        self.assertIn("- Downstream agents: Evaluation Monitor\n", execution)
        self.assertIn("Only a terminal decision hands off to the Memory Recorder", evaluation)
        self.assertIn("- Upstream agents: Evaluation Monitor\n", memory)
        self.assertIn("reached only by a terminal Evaluation Monitor handoff", memory)

    def test_every_example_has_required_artifacts(self):
        catalog = self.load_catalog()

        for entry in catalog["examples"]:
            with self.subTest(example=entry["id"]):
                example_dir = PATTERNS / entry["id"]
                self.assertTrue(example_dir.is_dir())
                self.assertTrue((example_dir / "README.md").is_file())
                self.assertTrue((example_dir / "flow.json").is_file())
                self.assertTrue((example_dir / "input.json").is_file())
                self.assertTrue((example_dir / "expected-output.json").is_file())

                flow = json.loads((example_dir / "flow.json").read_text(encoding="utf-8"))
                self.assertEqual(entry["id"], flow["id"])
                self.assertEqual(entry["pattern"], flow["pattern"])
                self.assertGreaterEqual(len(flow["workflow_steps"]), 3)
                self.assertGreaterEqual(len(flow["agents"]), 1)
                self.assertGreaterEqual(len(flow["policy_gates"]), 1)
                self.assertIn("artifact_type", flow["output_contract"])
                self.assertIn("receipt", flow)

    def test_every_example_is_runnable_and_matches_expected_output(self):
        catalog = self.load_catalog()

        for entry in catalog["examples"]:
            with self.subTest(example=entry["id"]):
                example_dir = PATTERNS / entry["id"]
                result = subprocess.run(
                    [
                        sys.executable,
                        str(RUNNER),
                        entry["id"],
                        "--root",
                        str(PATTERNS),
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )

                actual = json.loads(result.stdout)
                expected = json.loads((example_dir / "expected-output.json").read_text(encoding="utf-8"))
                self.assertEqual(expected, actual)
                self.assertEqual(entry["output_contract"]["artifact_type"], actual["artifact_type"])
                self.assertEqual(
                    set(entry["output_contract"]["required_fields"]),
                    set(actual["fields"]),
                )
                self.assertEqual(entry["policy_gates"], actual["policy_verdict"]["gates_checked"])
                self.assertTrue(actual["receipt"]["required"])

                serialized = json.dumps(expected)
                self.assertNotIn("Example value for", serialized)
                self.assertNotIn("example_expected_output", serialized)

                readme = (example_dir / "README.md").read_text(encoding="utf-8")
                self.assertIn(f"python ../run_example.py {entry['id']}", readme)

    def test_examples_do_not_reference_external_source_paths(self):
        forbidden = [
            "D:" + "\\Code\\ruvnet\\agent-harness-generator",
            "patterns" + ".md",
        ]
        scanned_roots = [PATTERNS, ROOT / "tools", ROOT / "tests"]
        scanned_files = [STATUS]
        for scanned_root in scanned_roots:
            scanned_files.extend(
                path
                for path in scanned_root.rglob("*")
                if path.is_file() and "__pycache__" not in path.parts
            )

        for path in scanned_files:
            with self.subTest(file=path.relative_to(ROOT)):
                text = path.read_text(encoding="utf-8")
                for value in forbidden:
                    self.assertNotIn(value, text)

    def test_example_ids_use_canonical_names_without_taxonomy_prefix(self):
        catalog = self.load_catalog()
        prefixed_catalog_ids = [
            entry["id"]
            for entry in catalog["examples"]
            if entry["id"].startswith(("agentic-", "vertical-"))
        ]
        prefixed_example_dirs = [
            path.name
            for path in PATTERNS.iterdir()
            if path.is_dir() and path.name.startswith(("agentic-", "vertical-"))
        ]
        prefixed_source_headings = [
            entry["source_heading"]
            for entry in catalog["examples"]
            if entry["source_heading"].startswith(("`agentic:", "`vertical:"))
        ]

        self.assertEqual([], prefixed_catalog_ids)
        self.assertEqual([], prefixed_example_dirs)
        self.assertEqual([], prefixed_source_headings)

    def test_status_file_tracks_all_examples_as_complete(self):
        catalog = self.load_catalog()
        status = STATUS.read_text(encoding="utf-8")

        self.assertNotIn("- [ ]", status)
        for entry in catalog["examples"]:
            with self.subTest(example=entry["id"]):
                self.assertIn(f"- [x] `{entry['id']}`", status)
                self.assertIn(entry["source_heading"], status)


if __name__ == "__main__":
    unittest.main()
