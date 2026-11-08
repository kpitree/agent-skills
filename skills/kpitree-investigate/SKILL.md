---
name: kpitree-investigate
description: The investigation sequence for "how is [metric] doing" and "why did [metric] change" questions in KPI Tree, including how to read period comparisons and drivers. Use whenever someone asks about a metric's performance, trend, drop, rise or cause.
---

# Investigating a metric

Do not stop before step 4 unless step 1 reports stable.

## 1. What moved: `analyze_metric`

Read the JSON decision signals first. `status` is the worst of six horizons (last 7 and
30 days, month, quarter and year to date, and the same month a year ago) plus the trend,
and `windows_moving_wrong_way` names the offenders. "drifting" means no single window
breached the threshold but the trajectory is wrong; that is what a slow compounding
decline looks like, so investigate it. Only "stable" is a reason to stop, and then name
the horizons you checked rather than implying you looked at everything.

## 2. Which driver or segment: `get_metric_drivers`

One call. The output carries its own interpretation guide, statistics and owners.
The invariants:

- Lead with Mapped Drivers (curated, tree-mapped, or verified via outcome: the strongest
  evidence a relationship is causal). Statistical, discovered correlations are NOT
  confirmed causes.
- A pair that shares a dimension value shares a real mechanism. Operational activity
  metrics (consultations, quotes, call volumes, cancellations) in the target's segment
  are candidate mechanisms, exactly what a "why did this change" question asks for. Two
  revenue-shaped metrics correlating is usually shared calendar structure, and
  near-duplicate definitions of one measure can appear as separate drivers at a
  correlation near 1.00: treat those as one item.
- A BROKEN relationship no longer holds; do not recommend it as a lever.
- Ranking is not evidence and ranking scores are internal. Never expose them.

For a segment breakdown, `compare_dimension_metrics`: call it without a dimension first
to discover the dimensions, then with one for contribution analysis.

## 3. The recorded why

If the `active_context` signal from step 1 is non-zero, the CONTEXT_DATA block in its
output already holds the recorded context. Otherwise call `get_relevant_context` with
the metric and a short query naming what moved. A mechanism without the recorded launch,
outage, absence or decision behind it is not yet an explanation. If nothing is
recorded, say so and ask; what the person tells you becomes an `add_context` write-back
in step 5 (see the `kpitree-context` skill).

## 4. Prior art

Before recommending anything: `get_tasks_for_metric` (tasks feature), `list_workflows`
and `list_workflow_runs` (workflows feature) to see whether an automation already fires
on this metric and what happened when it did, and `list_initiatives` (okrs feature) for
funded work already targeting it. Saying "nothing has been done" without having looked
is a wrong answer.

## 5. Answer, then write back

Lead with the headline, name the mechanism, give the recorded why, state what is
already in flight, recommend one action with its owner (the metric's Responsible or
Accountable person from the RACI in step 1), and apply the write-back triggers in the
`kpitree-context` skill. Ask before creating a task; never create one unprompted.

Deep dives when the signals or the person call for them: `explore_data_model` when the
pipeline is unhealthy (the move may be a data failure, not a real change);
`query_warehouse` (editor) only when the data needed is not already a metric, and only
after `explore_data_model` has named the table and column. `get_metric_calculations`
gives exact values: the latest row, or one date as YYYY-MM-DD; for a series narrow the
comparisons and pass a limit.

## Period comparisons

Always use the "to date versus previous" comparisons: `week_to_date_vs_previous`, `month_to_date_vs_previous`, `quarter_to_date_vs_previous`. They compare equivalent partial periods. Never use `day_over_day`, `week_on_week`, `month_on_month`, `quarter_on_quarter`, `year_on_year`: a partial current period against a full previous period misleads.

Both windows sit at the same calendar position in their period, so where the calendar
is uneven the two can differ by a day or two: read a quarter or year change of a few
percent as approximate, and check the window start and end dates before quoting a small
difference as real.

Two further families are fair like-for-like wherever a comparison is accepted:

- `trailing_7_days_vs_previous`, `trailing_30_days_vs_previous`: rolling windows that catch a change that started mid-period. When the
  trailing figure is materially worse than month to date, the change is recent and
  still running.
- `week_to_date_vs_previous_year`, `month_to_date_vs_previous_year`, `quarter_to_date_vs_previous_year`, `year_to_date_vs_previous`: the same period a year earlier. Read it before attributing a fall to
  seasonality, and before ruling seasonality out.
