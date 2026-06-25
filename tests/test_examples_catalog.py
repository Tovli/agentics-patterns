import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
CATALOG = EXAMPLES / "catalog.json"
STATUS = ROOT / "EXAMPLE_STATUS.md"
RUNNER = EXAMPLES / "run_example.py"


class ExamplesCatalogTest(unittest.TestCase):
    def load_catalog(self):
        with CATALOG.open(encoding="utf-8") as handle:
            return json.load(handle)

    def test_catalog_defines_every_example_once(self):
        catalog = self.load_catalog()
        entries = catalog["examples"]

        self.assertEqual(36, len(entries))
        self.assertEqual(len(entries), len({entry["id"] for entry in entries}))
        self.assertEqual(
            len(entries),
            len({(entry["section"], entry["number"]) for entry in entries}),
        )

    def test_every_example_has_required_artifacts(self):
        catalog = self.load_catalog()

        for entry in catalog["examples"]:
            with self.subTest(example=entry["id"]):
                example_dir = EXAMPLES / entry["id"]
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
                example_dir = EXAMPLES / entry["id"]
                result = subprocess.run(
                    [
                        sys.executable,
                        str(RUNNER),
                        entry["id"],
                        "--root",
                        str(EXAMPLES),
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
        scanned_roots = [EXAMPLES, ROOT / "tools", ROOT / "tests"]
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
            for path in EXAMPLES.iterdir()
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
