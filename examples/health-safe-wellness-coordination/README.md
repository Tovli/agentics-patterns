# Safe wellness coordination

Catalog entry: `catalog` pattern 14

Source heading: `health` — Safe Wellness Coordination Pattern

Pattern: **Intake -> red-flag triage -> resource coordination**

## Scenario

A user describes stress, poor sleep, and a concerning symptom while asking for next steps.

## Flow

1. Collect structured wellness information without diagnosing.
2. Detect red flags and route to appropriate resource type.
3. Coordinate logistics, reminders, and non-clinical follow-up.
4. Redirect clinical decisions to a clinician.

## Agent Roles

- Intake Agent
- Red-Flag Triage
- Care Coordinator
- Clinician Escalation Gate

## Policy Gates

- No diagnosis, treatment plan, or emergency minimization.
- Clinical content is routed to professional care.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py health-safe-wellness-coordination
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py health-safe-wellness-coordination --check
```

## Expected Output

The flow should produce `intake_summary` with these required fields:

- user_stated_concern
- non_clinical_context
- red_flags
- suggested_resource_type
- escalation_recommendation

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
