# Media optimization

Catalog entry: `catalog` pattern 10

Source heading: `advertising` — Media Optimization Pattern

Pattern: **Media plan -> creative -> performance readout -> budget reallocation**

## Scenario

A paid acquisition team has a fixed budget and must rebalance underperforming channels weekly.

## Flow

1. Allocate spend across channels based on objective and audience.
2. Create format-specific creative variants.
3. Read performance metrics against KPIs and stop-loss thresholds.
4. Recommend budget reallocation and flag weak creative or channel fit.

## Agent Roles

- Media Planner
- Copywriter
- Performance Analyst
- Budget Reallocator

## Policy Gates

- Creative ideation cannot control spend reallocation without performance evidence.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py advertising-media-optimization
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py advertising-media-optimization --check
```

## Expected Output

The flow should produce `media_plan` with these required fields:

- audience
- channel_split
- budget
- creative_variants
- kpis
- test_plan
- stop_loss_thresholds
- optimization_recommendation

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
