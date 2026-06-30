# Evidence dossier

Catalog entry: `catalog` pattern 3

Source heading: `research` — Evidence Dossier Pattern

Pattern: **Decompose -> search -> grade -> synthesize -> fact-check -> cite**

## Scenario

A product team asks whether passkeys reduce account takeover risk for consumer apps.

## Flow

1. Break the research question into independent sub-questions.
2. Collect primary and secondary sources for each sub-question.
3. Grade sources for authority, recency, bias, and relevance.
4. Synthesize only claims backed by accepted evidence.
5. Attack each claim and normalize citations.

## Agent Roles

- Scout
- Web Searcher
- Source Grader
- Synthesizer
- Fact Checker
- Citer

## Policy Gates

- Unsupported claims must be removed or marked as assumptions.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py research-evidence-dossier
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py research-evidence-dossier --check
```

## Expected Output

The flow should produce `evidence_dossier` with these required fields:

- answer
- evidence_table
- confidence
- disputed_claims
- missing_evidence
- citations

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
