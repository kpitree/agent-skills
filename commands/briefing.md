---
description: What needs my attention in KPI Tree today, from the briefing compiled for me this morning
---

Follow the `kpitree-briefing` skill. Call `get_my_briefing` and present the action plan it
returns: the findings in priority order, each with what moved, why (from the recorded
context), who owns it and the proposed action. Open a finding with `get_briefing_finding`
only when the person asks about it. Do not re-analyse metrics the briefing already
covers; it was compiled from the same tools. When the person says to go ahead with a
proposed action, `accept_briefing_action`; when they turn one down,
`dismiss_briefing_action` with their reason in their own words. Never show UUIDs or ids.
End by asking which finding to pursue.
