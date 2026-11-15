---
description: "Investigate a KPI Tree metric: what moved, which driver, the recorded why, what is in flight, and what to do"
argument-hint: <metric name> [what prompted the question]
---

Investigate the metric named in `$ARGUMENTS` using the `kpitree-investigate` skill:

1. `search_metrics` if the name is ambiguous, then `analyze_metric`.
2. `get_metric_drivers` for the mechanism.
3. The recorded why: the CONTEXT_DATA block, or `get_relevant_context`.
4. Prior art: `get_tasks_for_metric`, `list_workflows` and `list_workflow_runs`,
   `list_initiatives`, where those features are on.
5. One narrative: headline, mechanism, recorded why, what is in flight, one recommended
   action with its owner. Offer the write-backs from the `kpitree-context` skill; ask
   before creating a task.

Use the to-date-versus-previous comparisons, never the partial-against-full ones.
