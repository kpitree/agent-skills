# Metric Drivers Analysis
**Target metric:** Consultations (Leeds)
**month_to_date_vs_previous change:** -31.0%

## Mapped Drivers (0)
No curated, outcome-verified or tree-mapped driver exists for this metric. This is a genuine absence, not a truncation: mapped drivers are never cut by the `limit` parameter.

## Statistical Correlations (1)
These metrics are statistically correlated but NOT mapped in any KPI tree.

### 1. Staff on shift (Leeds) [discovered] [same branch = Leeds]
- Direction: same direction (both down); driver change: -33.0%
- r = 0.77, n = 90, significant
- Owner: Priya Shah (Leeds branch manager); status: ACTIVE

## Presentation Rules
- **[same <dimension> = <value>]** means both metrics are cut to the same dimension value: an operational metric in the same segment is a CANDIDATE MECHANISM.
- **Statistical Correlations** are NOT confirmed drivers.

## Next Steps
- This output shows mechanism, not cause. The recorded why is in the CONTEXT_DATA block of analyze_metric.
- BEFORE offering any driver as a lever, check get_tasks_for_metric(metric_uuid="9e8d7c6b-5a4f-4e3d-8c2b-1a0f9e8d7c6b"), list_workflows() and list_initiatives().

## Number discipline (hard rule)
- EVERY figure you state must trace to a tool result.
