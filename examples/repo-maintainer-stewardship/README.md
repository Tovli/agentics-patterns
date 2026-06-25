# Repo stewardship

Catalog entry: `catalog` pattern 18

Source heading: `repo-maintainer` — Repo Stewardship Pattern

Pattern: **Triage diff -> benchmark -> release check -> security scan**

## Scenario

A release candidate changes CLI wiring, dependencies, and generated template files.

## Flow

1. Identify changed areas, risks, and review order.
2. Run performance and regression gates.
3. Flag risky MCP grants, leaked secrets, and dangerous diffs.
4. Draft release body and validate readiness gates.
5. Produce release or no-release recommendation.

## Agent Roles

- Maintainer
- Benchmarker
- Security Reviewer
- Release Drafter

## Policy Gates

- The recommendation is conservative and does not overstate readiness.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py repo-maintainer-stewardship
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py repo-maintainer-stewardship --check
```

## Expected Output

The flow should produce `maintainer_packet` with these required fields:

- changed_areas
- risk_map
- benchmark_result
- security_findings
- release_notes
- readiness_verdict

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
