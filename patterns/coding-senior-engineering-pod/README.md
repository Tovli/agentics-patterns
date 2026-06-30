# Senior engineering pod

Catalog entry: `catalog` pattern 2

Source heading: `coding` — Senior Engineering Pod Pattern

Pattern: **Architect -> implementer -> reviewer -> test-writer**

## Scenario

A repository issue asks for deterministic retry behavior around a flaky API client.

## Flow

1. Convert the issue into a minimal file-level implementation plan.
2. Write or update the focused failing test.
3. Implement the smallest local-style patch.
4. Review the diff for correctness, security, reuse, and overengineering.
5. Run validation gates and summarize residual risk.

## Agent Roles

- Architect
- Implementer
- Reviewer
- Test Writer

## Policy Gates

- No implementation starts before a concrete plan exists.
- No merge recommendation is allowed before tests and review.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py coding-senior-engineering-pod
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py coding-senior-engineering-pod --check
```

## Expected Output

The flow should produce `patch_packet` with these required fields:

- plan
- changed_files
- tests
- review_findings
- validation_result
- residual_risk

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
