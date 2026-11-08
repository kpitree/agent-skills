---
name: kpitree-briefing
description: Reading and acting on KPI Tree's morning briefings. Use for "what should I look at today", "what changed", "anything I should know", "what needs my attention", "my action plan", "do that" or "not that one" about an action a briefing recommended, "how long has this been going on", and "what changed since last week".
---

# Briefings

Every weekday morning KPI Tree compiles a briefing across every metric: what moved, the
mechanism, the recorded context, the work in flight and the owners, with recommended
actions. It answers in one call what would otherwise take a dozen `analyze_metric`
calls, and reading it never spends: no model is asked to write anything.

## Which call

| The person asks | Call |
| --- | --- |
| "What should I look at today?", "What changed?", "Anything I should know?" | `get_briefing` with scope "company" |
| "What needs my attention?", "What's on my plate?" | `get_my_briefing`, the action plan written for this person; its header says whether it came from their plan, from their slice of the company briefing, or from a live read |
| "How is my team doing?" | `get_briefing` with scope "team" |
| "What did last week deliver against our objectives?" | `get_briefing` with scope "weekly" |
| "What changed since last week?" | `list_briefings` for the periods, then `get_briefing` with a period |
| "How long has this been going on?", "Was it investigated?", "Did it come back?" | `get_briefing_finding` with the finding's id |
| "Do that", "Go ahead with the nudge to Sam" | `accept_briefing_action` with the briefing's artifact uuid and the action's id |
| "Not that one", "Skip the check-in" | `dismiss_briefing_action`, with the reason in the person's own words |
| "Write me a plan", when `get_my_briefing` reports that none exists | `derive_briefing` |

Where the briefings feature is off, or the person wants live numbers rather than this
morning's compile, `get_business_health` is the account-wide fallback and
`analyze_metric` the per-metric one.

## Reading a briefing

- `get_briefing` returns the summary, the headlines and per-section counts. Ask for a
  named section (findings, people, decisions, blockers, absences, proposed_actions,
  tasks_scheduled, objectives, initiatives) to read its rows, paged with limit and
  offset.
- A finding keeps its id for as long as the same metric shows the same kind of trouble.
  That is what makes `get_briefing_finding` the answer to "how long": it returns every
  appearance the person can see, newest first, with the full record from the latest.
- Present findings in the briefing's priority order, each with what moved, why (from
  the recorded context), who owns it and the proposed action. Do not re-analyse metrics
  the briefing already covers; it was compiled from the same tools. Open a finding only
  when the person asks about it.
- `recall` searches the recorded context and the briefing findings together, for "what
  do we know about X" when you do not know which of the two holds the answer.

## Acting on a briefing

- Nothing a briefing proposes happens until somebody accepts it. Call
  `accept_briefing_action` only when the person has asked for that action by name. A do,
  record_why or assign_owner action becomes a task carrying its finding; a nudge sends
  the drafted message to the colleague it names; a check_in writes the check-in.
  Accepting twice is safe: the same task, and nothing is sent again.
- `dismiss_briefing_action` records the decision beside the briefing and stops offering
  that action for as long as the finding keeps its id. Record the reason in the person's
  own words; it is what makes the next morning's briefing better.
- `derive_briefing` writes the person's own plan from today's company briefing. Use it
  only when they ask for their plan and `get_my_briefing` has said none exists: it spends
  a model call against the workspace's daily budget. A refusal (a plan written within the
  last hour, or no company briefing yet) is an answer, not an error to retry.

## Preferences

`get_my_preferences` and `set_my_preference` hold small interface choices that follow
the person between devices: a collapsed band, a last-used filter. Read before offering
to change one; write only when the person asks to remember a layout choice. Never store
notes or findings there.

## Administrators

`get_artifact` (admin) returns a stored artifact whole, every section and no paging: a
briefing row, or an investigation kept against a metric. Prefer `get_briefing` for every
ordinary question.

Never show artifact uuids, finding ids or action ids; refer to findings and actions by
what they say. Where the client supports MCP resources, `kpitree://briefing/{scope}/{period}`
and `kpitree://finding/{id}` read the same rows the tools return.
