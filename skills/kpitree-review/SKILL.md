---
name: kpitree-review
description: Running a weekly or monthly business review from KPI Tree, and answering "how is the business doing", "which objectives are at risk" and "where is the money working" questions.
---

# A business review

## Where to start

- "How is the business doing?": `get_briefing` with scope "company" where the briefings
  feature is on. It is compiled every weekday morning across every metric and carries,
  for each finding, the mechanism, the recorded context, the work in flight and the
  owners, so it answers in one call what would otherwise take a dozen `analyze_metric`
  calls. Scope "weekly" is the weekly action plan: which objectives moved last week,
  what completed against them, and what nothing confirmed. Where briefings are off, or
  the person wants live numbers rather than this morning's compile, `get_business_health`
  is the account-wide view organised by team; scope it by tree or team when asked.
- "What needs my attention?": `get_my_briefing`, the action plan already compiled for
  this person this morning, see the `kpitree-briefing` skill. Only for the person's OWN
  metrics and attention items.
- "Who is working on what?": `get_overview_timeline`, the week as lanes and dated items.
- Objectives: `list_objectives`, then `get_objective` for key results and funded
  initiatives. Each objective carries two progress lanes: `progress` (the outcome, read
  from the data) and `execution_progress` (work done). A gap between the lanes is the
  headline finding: delivered work that is not moving the number, or a number moving
  without the work. An objective with no reading yet is awaiting data, never 0%.
- Initiatives: `list_initiatives` and `get_initiative`, funded work with budget, spend,
  owner, milestones and targeted metrics. Impact evidence is read from the calculations
  pipeline, never self-reported.
- "Which initiatives should we back, fix or stop?": `get_portfolio`, every initiative
  ranked by outcome evidence with a verdict (double-down, working, wrong-lever,
  too-early, awaiting-data, not-started).
- Automation: `list_workflows` (what exists and whether it is live),
  `list_scheduled_workflow_runs` (what is due next), `get_workflow` and
  `list_workflow_runs` (did it fire, and what happened).

## Shape of the review

1. Headline: the one or two findings that matter most, from the briefing's headlines, or
   from `analyze_metric` on the metrics that moved most, using the comparison rules in
   the `kpitree-investigate` skill.
2. For each, the mechanism (`get_metric_drivers`) and the recorded why
   (`get_relevant_context`, or `recall` when a briefing may already have raised it), in
   a sentence each.
3. Objectives and initiatives: the lane gaps and the portfolio verdicts that changed.
4. What is in flight: tasks, workflow runs, initiatives already targeting the problems,
   and the actions the briefing proposed that nobody has accepted yet.
5. Decisions for the room: one recommended action per problem, with its owner from the
   RACI. Offer to record decisions with `add_context`, to accept a proposed action with
   `accept_briefing_action`, and to propose tasks; never create a task unprompted.

Name people and metrics; never show UUIDs. Where a feature is off for this workspace
(okrs, workflows, briefings, tasks, knowledge), say so once and leave that section out.
