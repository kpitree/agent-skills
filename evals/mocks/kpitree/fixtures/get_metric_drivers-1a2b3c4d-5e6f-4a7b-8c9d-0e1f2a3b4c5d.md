# Metric Drivers Analysis
**Target metric:** Quote-to-sale conversion
**week_to_date_vs_previous change:** -38.0%

## Mapped Drivers (1)
These metrics have been intentionally linked by the user in a KPI tree, or curated/confirmed by a verified outcome. They are always returned in full and are never displaced by the `limit` parameter.

### 1. Online quote abandonment [tree-mapped] [same channel = Online]
- Direction: opposite (abandonment up, conversion down); driver change: +61.0%
- r = -0.88, n = 120, significant; deseasonalized r = -0.86; Granger-causes target at lag 1 day
- Owner: Dana Okafor (Sales Operations); status: ACTIVE

## Statistical Correlations (1)
These metrics are statistically correlated but NOT mapped in any KPI tree.

### 1. Website sessions [discovered]
- Direction: same direction; driver change: +1.2%
- r = 0.22, n = 120, not significant
- Owner: Lee Grant (Marketing); status: ACTIVE

## Interpretation Guide
- **The `limit` parameter only caps Statistical Correlations.** Mapped Drivers are always returned in full.
- **Ranking is not evidence.**

## Presentation Rules
- **Mapped Drivers** are human-curated causal links. ALWAYS lead with these.
- **Statistical Correlations** are NOT confirmed drivers.

## Next Steps
- BEFORE offering any driver as a lever, check what has already been tried: get_tasks_for_metric(metric_uuid="1a2b3c4d-5e6f-4a7b-8c9d-0e1f2a3b4c5d"), list_workflows() then list_workflow_runs(), list_initiatives().
- This output shows mechanism, not cause. The recorded why is in the CONTEXT_DATA block of analyze_metric.
- Then answer: lead with the mechanism, give the recorded why, name the owner responsible, and ask whether to create a task for them.

## Number discipline (hard rule)
- EVERY figure you state must trace to a tool result. The driver changes above are PERCENTAGES.
