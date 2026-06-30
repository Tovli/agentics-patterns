from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from example_runtime import build_output


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_example(root: Path, example_id: str) -> tuple[dict, dict]:
    example_dir = root / example_id
    if not example_dir.is_dir():
        raise FileNotFoundError(f"Unknown example: {example_id}")

    flow = read_json(example_dir / "flow.json")
    input_payload = read_json(example_dir / "input.json")
    if flow["id"] != example_id:
        raise ValueError(f"Flow id {flow['id']!r} does not match {example_id!r}")
    return flow, input_payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run one deterministic agentic pattern example.")
    parser.add_argument("example_id", help="Example directory name from catalog.json")
    parser.add_argument("--root", default=Path(__file__).resolve().parent, type=Path)
    parser.add_argument("--check", action="store_true", help="Compare the generated artifact with expected-output.json.")
    args = parser.parse_args(argv)

    try:
        flow, input_payload = load_example(args.root, args.example_id)
        output = build_output(flow, input_payload)
        if args.check:
            expected = read_json(args.root / args.example_id / "expected-output.json")
            if output != expected:
                print("Generated output differs from expected-output.json", file=sys.stderr)
                return 1
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 2

    json.dump(output, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
