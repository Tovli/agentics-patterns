# Paper trading decision

Catalog entry: `catalog` pattern 4

Source heading: `trading` — Paper Trading Decision Pattern

Pattern: **Watch -> signal -> risk gate -> paper execution -> attribution**

## Scenario

A momentum signal appears in a liquid ETF, but portfolio drawdown is near the weekly limit.

## Flow

1. Summarize market state and relevant conditions.
2. Propose signal, confidence, horizon, and invalidation criteria.
3. Check exposure, drawdown, liquidity, concentration, and circuit breakers.
4. Route only approved orders to paper execution.
5. Attribute outcome to thesis, timing, risk, or noise.

## Agent Roles

- Market Watcher
- Signal Generator
- Risk Checker
- Paper Executor
- Postmortem Analyst

## Policy Gates

- Risk Checker is non-bypassable.
- Executor runs paper-by-default unless live trading is explicitly approved.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py trading-paper-decision
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py trading-paper-decision --check
```

## Expected Output

The flow should produce `trade_ticket` with these required fields:

- hypothesis
- signal
- invalidation_criteria
- risk_checks
- order_intent
- paper_live_status
- post_trade_analysis

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
