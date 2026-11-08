---
name: kpitree-review
description: Running a weekly or monthly business review from KPI Tree, and answering "how is the business doing", "what needs my attention", "which objectives are at risk" and "where is the money working" questions.
---

# A business review

## Where to start

- "How is the business doing?": `get_business_health`, account-wide health organised by
  team; scope it by tree or team when asked.
- "What needs my attention?": `get_my_briefing`, the action plan already compiled for
  this person this morning. It never spends; open one finding with
  `get_briefing_finding`. Only for the person's OWN metrics and attention items.
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

1. Headline: the one or two metrics that moved most, on which horizons, using the
   comparison rules in the `kpitree-investigate` skill.
2. For each, the mechanism (`get_metric_drivers`) and the recorded why
   (`get_relevant_context`), in a sentence each.
3. Objectives and initiatives: the lane gaps and the portfolio verdicts that changed.
4. What is in flight: tasks, workflow runs, initiatives already targeting the problems.
5. Decisions for the room: one recommended action per problem, with its owner from the
   RACI. Offer to record decisions with `add_context` and to propose tasks; never create
   a task unprompted.

Name people and metrics; never show UUIDs. Where a feature is off for this workspace
(okrs, workflows, briefings, tasks, knowledge), say so once and leave that section out.
