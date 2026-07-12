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
            {
                "confidence_gate_decision",
                "stagnation_response",
                "knowledge_boundary",
                "evaluation",
                "memory_update",
            },
            set(example_output["required_explicit_fields"]),
        )
        self.assertTrue(example_output["stagnation_recovery_required"])

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

        verdict = output["policy_verdict"]
        self.assertTrue(verdict["allowed"])
        self.assertTrue(verdict["blocked_actions"])
        self.assertTrue(verdict["allow_evidence"])
        self.assertEqual(
            set(flow["policy_gates"]),
            {item["gate"] for item in verdict["allow_evidence"]},
        )
        blocked_actions = " ".join(item["action"] for item in verdict["blocked_actions"])
        self.assertIn("timeout", blocked_actions)
        self.assertIn("root cause", blocked_actions)
        self.assertIn("raw deployment logs", blocked_actions)
        self.assertNotIn("represented", verdict["notes"])

        bypassed_confidence = copy.deepcopy(flow)
        bypassed_decision = bypassed_confidence["example_output"]["field_values"]["confidence_gate_decision"]
        bypassed_decision["observed_confidence"] = 0.2
        bypassed_decision["threshold_satisfied"] = False
        with self.assertRaisesRegex(ValueError, "cannot be presented below"):
            build_output(bypassed_confidence, input_payload)

        bypassed_stagnation = copy.deepcopy(flow)
        bypassed_stagnation["example_output"]["field_values"]["stagnation_response"]["route"] = "execution"
        with self.assertRaisesRegex(ValueError, "stagnation must route to metaplanning"):
            build_output(bypassed_stagnation, input_payload)

        bypassed_policy = copy.deepcopy(flow)
        bypassed_policy["example_output"]["policy_verdict"]["allow_evidence"] = []
        with self.assertRaisesRegex(ValueError, "exactly one evidence record"):
            build_output(bypassed_policy, input_payload)

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

        empty_evidence = copy.deepcopy(flow)
        empty_evidence["example_output"]["policy_verdict"]["allow_evidence"][0]["evidence"] = ""
        with self.assertRaisesRegex(ValueError, "non-empty evidence"):
            build_output(empty_evidence, input_payload)

        malformed_block = copy.deepcopy(flow)
        malformed_block["example_output"]["policy_verdict"]["blocked_actions"][0] = {
            "action": "",
            "reason": "",
        }
        with self.assertRaisesRegex(ValueError, "non-empty action and reason"):
            build_output(malformed_block, input_payload)

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
