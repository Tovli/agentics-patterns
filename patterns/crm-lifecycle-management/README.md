# CRM lifecycle management

Catalog entry: `catalog` pattern 8

Source heading: `crm` — Lifecycle Management Pattern

Pattern: **Qualify -> manage account -> watch churn**

## Scenario

A mid-market account expands usage but has three unresolved support tickets before renewal.

## Flow

1. Score fit, urgency, potential value, and routing.
2. Choose the next relationship play.
3. Monitor churn signals and explain early risk.
4. Update lifecycle memory with distilled state.

## Agent Roles

- Lead Qualifier
- Account Manager
- Churn Watcher
- Memory Updater

## Policy Gates

- CRM mutation is suggestion-only unless explicitly permitted.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py crm-lifecycle-management
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py crm-lifecycle-management --check
```

## Expected Output

The flow should produce `account_brief` with these required fields:

- stage
- score
- next_best_action
- relationship_context
- churn_risk
- missing_facts

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
