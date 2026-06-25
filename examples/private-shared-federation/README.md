# Private/shared federation

Catalog entry: `agentic` pattern 14

Source heading: Federation pattern for private/shared learning

Pattern: **Local confidential work -> distilled non-sensitive pattern -> signed sharing -> peer validation**

## Scenario

An enterprise team shares a generic failure pattern learned from internal incidents without exposing customer data.

## Flow

1. Distill non-sensitive pattern from confidential local work.
2. Filter user data, secrets, and task history.
3. Sign the reusable pattern and publish to an allowed namespace.
4. Validate peer patterns before import.

## Agent Roles

- Local Distiller
- Sensitivity Filter
- Signer
- Federation Publisher
- Peer Validator

## Policy Gates

- Federation shares patterns, not user data.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py private-shared-federation
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py private-shared-federation --check
```

## Expected Output

The flow should produce `federated_pattern_record` with these required fields:

- distilled_pattern
- excluded_sensitive_data
- signature
- namespace
- peer_validation
- import_decision

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
