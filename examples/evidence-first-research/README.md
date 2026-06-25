# Evidence-first research

Catalog entry: `agentic` pattern 6

Source heading: Evidence-first research pattern

Pattern: **Retriever -> source ranker -> claim extractor -> contradiction finder -> synthesizer -> citation verifier**

## Scenario

A research assistant must answer a technical market question with primary-source support.

## Flow

1. Retrieve candidate sources for each sub-question.
2. Rank each source for authority, recency, balance, and relevance.
3. Extract claims and identify contradictions.
4. Synthesize only supported claims.
5. Verify every citation against the claim it supports.

## Agent Roles

- Retriever
- Source Ranker
- Claim Extractor
- Contradiction Finder
- Synthesizer
- Citation Verifier

## Policy Gates

- The synthesizer cannot use claims that failed citation verification.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py evidence-first-research
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py evidence-first-research --check
```

## Expected Output

The flow should produce `research_quality_packet` with these required fields:

- answer
- source_ranking
- claim_table
- contradictions
- citation_verdicts
- confidence

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
