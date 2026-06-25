# Retrieval review

Catalog entry: `catalog` pattern 13

Source heading: `ruvector` — Retrieval Review Pattern

Pattern: **Index -> retrieve -> answer -> source review**

## Scenario

A documentation assistant answers a policy question from a newly indexed handbook corpus.

## Flow

1. Chunk, embed, and store source documents.
2. Retrieve candidate passages with citations.
3. Draft an answer only from retrieved evidence.
4. Grade answer fidelity against sources.
5. Reject or retry weak and unsupported answers.

## Agent Roles

- Indexer
- Retriever
- Answer Drafter
- Source Reviewer

## Policy Gates

- Retrieval confidence and answer faithfulness are assessed separately.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py retrieval-review
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py retrieval-review --check
```

## Expected Output

The flow should produce `reviewed_answer` with these required fields:

- cited_response
- source_list
- retrieval_confidence
- unsupported_claims
- reviewer_verdict

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
