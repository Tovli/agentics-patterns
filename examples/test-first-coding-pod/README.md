# Test-first coding pod

Catalog entry: `agentic` pattern 5

Source heading: Test-first coding pod

Pattern: **Understand issue -> failing test -> patch -> tests -> diff review**

## Scenario

A repo-maintenance agent fixes a parsing regression by proving the failure before editing production code.

## Flow

1. Understand the issue and target behavior.
2. Write the failing test that reproduces the issue.
3. Patch only the code needed to pass the test.
4. Run relevant and full validation gates.
5. Review the diff and summarize release notes.

## Agent Roles

- Issue Analyst
- Test Author
- Implementation Agent
- Reviewer
- Release-note Drafter

## Policy Gates

- No production code is edited before a failing test exists.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py test-first-coding-pod
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py test-first-coding-pod --check
```

## Expected Output

The flow should produce `coding_pod_packet` with these required fields:

- issue_summary
- failing_test
- patch
- validation
- diff_review
- release_note

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
