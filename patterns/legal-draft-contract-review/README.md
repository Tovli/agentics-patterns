# Draft-only contract review

Catalog entry: `catalog` pattern 6

Source heading: `legal` — Draft-Only Contract Review Pattern

Pattern: **Redline -> citation check -> risk rating -> human lawyer**

## Scenario

A vendor MSA includes broad indemnity and unilateral renewal language that conflicts with the playbook.

## Flow

1. Compare clauses against the contract playbook.
2. Propose clause-level draft redlines.
3. Verify every cited authority or policy reference.
4. Score residual legal and commercial risk per clause.
5. Route draft redline and memo for licensed human review.

## Agent Roles

- Redliner
- Citation Checker
- Risk Rater
- Human Lawyer Gate

## Policy Gates

- Output is draft-only and is never presented as legal advice.
- Licensed human review is required before external use.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py legal-draft-contract-review
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py legal-draft-contract-review --check
```

## Expected Output

The flow should produce `draft_redline_packet` with these required fields:

- redlines
- issue_list
- negotiation_notes
- citation_status
- risk_score_per_clause
- draft_only_disclaimer

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
