# Customer support resolution

Catalog entry: `catalog` pattern 5

Source heading: `support` — Customer Support Resolution Pattern

Pattern: **Triage -> KB retrieval -> grounded response -> escalation**

## Scenario

A frustrated enterprise customer reports that SSO stopped working after a certificate rotation.

## Flow

1. Classify intent, urgency, customer tier, and sentiment.
2. Retrieve cited policy and product answers from the KB.
3. Draft a grounded customer-facing response.
4. Escalate when confidence, policy coverage, tone, or authority requires it.
5. Store distilled account and ticket learning.

## Agent Roles

- Triager
- KB Searcher
- Responder
- Escalator
- Memory Updater

## Policy Gates

- The responder abstains instead of inventing product or policy details.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py support-resolution
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py support-resolution --check
```

## Expected Output

The flow should produce `support_reply_packet` with these required fields:

- classification
- cited_kb_articles
- customer_reply
- confidence
- escalation_reason
- next_action

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
