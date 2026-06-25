# Campaign strategy

Catalog entry: `catalog` pattern 9

Source heading: `marketing` — Campaign Strategy Pattern

Pattern: **Audience -> message -> content -> SEO/analytics loop**

## Scenario

A B2B SaaS team wants a launch campaign for a new compliance dashboard.

## Flow

1. Define audience, positioning, channel, and target metric.
2. Draft channel-specific assets.
3. Ground content in search demand and analytics.
4. Revise campaign brief before human review and publishing.
5. Feed measured results back into memory.

## Agent Roles

- Strategist
- Content Creator
- SEO Analyst
- Analytics Reviewer
- Memory Updater

## Policy Gates

- Traffic, SEO, and competitor claims require analytics or cited evidence.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py marketing-campaign-strategy
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py marketing-campaign-strategy --check
```

## Expected Output

The flow should produce `campaign_brief` with these required fields:

- icp
- message
- content_plan
- channels
- seo_targets
- analytics_baseline
- kpi
- experiments

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
