# DevOps incident response

Catalog entry: `catalog` pattern 1

Source heading: `devops` — Incident Response Pattern

Pattern: **Alert -> runbook -> gated action -> escalation -> postmortem**

## Scenario

Checkout latency crosses the paging threshold while database saturation is suspected.

## Flow

1. Classify alert severity and impacted service.
2. Find the closest runbook and propose bounded diagnostics.
3. Gate shell, network, and kubectl actions before execution.
4. Escalate when severity or uncertainty crosses policy.
5. Draft timeline, root cause, contributing factors, and follow-ups.

## Agent Roles

- Responder
- Runbook Runner
- Policy Gate
- Escalator
- Postmortem Writer

## Policy Gates

- Production mutations require explicit human approval.
- Escalation is mandatory for high severity or unclear blast radius.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py devops-incident-response
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py devops-incident-response --check
```

## Expected Output

The flow should produce `incident_packet` with these required fields:

- severity
- impacted_service
- evidence
- actions_taken
- actions_blocked
- escalation_target
- postmortem_draft

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
