# Metric Drivers Analysis
**Target metric:** Revenue
**month_to_date_vs_previous change:** -17.8%

## Mapped Drivers (2)
These metrics have been intentionally linked by the user in a KPI tree, or curated/confirmed by a verified outcome. They are always returned in full and are never displaced by the `limit` parameter.

### 1. Consultations (Leeds) [tree-mapped] [same branch = Leeds]
- Direction: same direction (both down); driver change: -31.0%
- r = 0.84, n = 180, significant; deseasonalized r = 0.79; Granger-causes target at lag 3 days
- Owner: Priya Shah (Leeds branch manager); status: ACTIVE

### 2. Quotes issued [curated]
- Direction: same direction; driver change: -0.8%
- r = 0.61, n = 180, significant; deseasonalized r = 0.44
- Owner: Sam Patel (Commercial); status: ACTIVE

## Statistical Correlations (1)
These metrics are statistically correlated but NOT mapped in any KPI tree.

### 1. Website sessions [discovered]
- Direction: same direction; driver change: -2.1%
- r = 0.41, n = 180, not significant at this sample
- Owner: Lee Grant (Marketing); status: ACTIVE

## Interpretation Guide
- Drivers are ranked in bands: curated/outcome-verified first, then tree-mapped, then statistical.
- **The `limit` parameter only caps Statistical Correlations.** Mapped Drivers are always returned in full.
- **Ranking is not evidence.** Rank partly follows the magnitude of change.

## Presentation Rules
- **Mapped Drivers** are human-curated causal links. ALWAYS lead with these when summarising for stakeholders.
- **Statistical Correlations** are NOT confirmed drivers.
- **[same <dimension> = <value>]** means both metrics are cut to the same dimension value. This is the strongest mechanism signal.

## Next Steps
- Do not fan out across every driver above. DO go deep on the one or two you will lead with.
- BEFORE offering any driver as a lever, check what has already been tried: get_tasks_for_metric(metric_uuid="8f1c2d3e-4b5a-4c6d-8e7f-9a0b1c2d3e4f") for human actions, list_workflows() for an automation already firing on this metric, list_initiatives() for funded work already targeting it.
- This output shows mechanism, not cause. The recorded why is in the CONTEXT_DATA block of analyze_metric, or get_relevant_context(metric_uuid="8f1c2d3e-4b5a-4c6d-8e7f-9a0b1c2d3e4f").
- Then answer: lead with the mechanism, give the recorded why, name the owner responsible, and ask whether to create a task for them.

## Number discipline (hard rule)
- EVERY figure you state must trace to a tool result. The driver changes above are PERCENTAGES; do not convert them into currency.
