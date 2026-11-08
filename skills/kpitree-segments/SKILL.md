---
name: kpitree-segments
description: Answering questions scoped to one site, branch, region, product line, tier or other segment in KPI Tree, rather than to one metric. Use for "what's going on at", "how is the [segment] doing" and "which [segments] are struggling" questions.
---

# Questions about a segment

A segment question is about everything measured for one dimension value, not about one
metric. Two ways in:

- `get_metric_relationships` on any metric for that segment, and read
  `dimension_siblings`: every metric cut to the same dimension value, in one call.
- `search_metrics` with `dimension_value` set to the segment. Filters combine with AND
  (free text, `dimension_value`, `entity`, `owner`, `tree`). Text alone finds a segment
  only when the segment name is in the metric name, so use `dimension_value` for
  segment questions. An empty filtered result means the value did not match the
  semantic graph, NOT that the segment is unmeasured: check the spelling with
  `explore_entity` before saying there is no data.

Then run `analyze_metric` on the operational metrics (volume, quotes, consultations,
cancellations), not just the money one. The operational metrics are where the mechanism
shows first.

To rank segments against each other on one metric, `compare_dimension_metrics` with the
dimension named: it returns the segments side by side with contribution analysis.

Where a segment has its own KPI tree (`clone_tree_for_dimension` builds those), `get_tree`
on it shows the structure the organisation itself uses for that segment, and a linked
node in a company tree (`link_tree_node`) points at it.

Finish as for any metric question: the recorded why from `get_relevant_context`, prior
art from tasks, workflows and initiatives, one narrative, one recommended action with its
owner.
