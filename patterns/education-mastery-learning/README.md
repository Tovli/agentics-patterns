# Mastery learning

Catalog entry: `catalog` pattern 17

Source heading: `education` — Mastery Learning Pattern

Pattern: **Tutor -> explain -> quiz -> grade -> update mastery**

## Scenario

A learner knows linear equations but struggles to apply slope-intercept form in word problems.

## Flow

1. Choose next concept from the mastery map.
2. Explain at the right depth for the learner profile.
3. Generate calibrated questions.
4. Grade answers against a rubric.
5. Update mastery memory and recommend next focus.

## Agent Roles

- Tutor
- Explainer
- Quiz Master
- Grader
- Mastery Memory Updater

## Policy Gates

- The tutor abstains instead of faking certainty.

## Input

Use `input.json` as the concrete scenario payload for this example.

## Run

From this directory:

```bash
python ../run_example.py education-mastery-learning
```

To verify the checked-in expected artifact:

```bash
python ../run_example.py education-mastery-learning --check
```

## Expected Output

The flow should produce `learning_cycle_report` with these required fields:

- concept_taught
- explanation_level
- quiz_result
- misconceptions
- mastery_update
- next_recommendation

## Receipt

The run is complete only when `flow.json` receipt requirements are satisfied.
