# STORM article synthesis

Catalog entry: `agentic` pattern 15

Source heading: STORM multi-perspective article synthesis pattern

Pattern: **Discover perspectives -> ask multi-perspective questions -> retrieve and ground -> outline -> write sections -> audit citations**

## Reference

This pattern is adapted from **STORM**: Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models.

Paper: https://arxiv.org/abs/2402.14207

## Scenario

A documentation team must produce a comprehensive, neutral overview article on an unfamiliar topic, grounded entirely in cited sources rather than model memory.

## Flow

1. Discover diverse perspectives by surveying related topics and articles.
2. Drive multi-perspective question asking through simulated expert conversations.
3. Convert questions into queries, retrieve trusted sources, and answer with citations.
4. Generate and refine a hierarchical outline from internal knowledge and collected answers.
5. Write each section grounded only in collected references with inline citations.
6. Assemble the lead section, remove duplication, and verify every citation.

## Agent Roles

- Perspective Discoverer
- Question Asker
- Grounded Expert
- Outline Architect
- Section Writer
- Citation Auditor

## Policy Gates

- Article claims must be grounded in retrieved, cited sources, not in model memory.
- Untrusted or unverifiable sources are excluded before they ground any section.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py storm-article-synthesis
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py storm-article-synthesis --check
```

## Expected Output

The flow should produce `grounded_article_packet` with these required fields:

- topic
- perspectives
- outline
- article
- citations
- excluded_references
- confidence

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
