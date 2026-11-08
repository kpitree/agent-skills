{"source": "artifact", "artifact_uuid": "b1f5c2d3-4e5f-4a6b-8c7d-9e0f1a2b3c4d", "kind": "briefing", "scope": "company", "period": "2026-11-08", "state": "ready",
 "title": "Company briefing, Saturday 8 November 2026",
 "summary": "Revenue is down 17.8% month to date, led by the Leeds branch, where consultations fell 31% while the branch manager is on leave. Quote-to-sale conversion fell 38% week to date, almost all of it in the online channel after Tuesday's pricing change. Refund rate is above threshold for a third week. Everything else is within its normal range.",
 "severity_counts": {"high": 2, "medium": 1, "low": 0},
 "headlines": [
   {"finding_id": "f-rev-leeds", "severity": "high", "metric": "Revenue", "what_moved": "-17.8% month to date, -12.0% week to date", "mechanism": "Consultations (Leeds) -31%, a tree-mapped driver in the same branch", "why": "Leeds branch manager on leave 27 Oct to 14 Nov; two staff covering", "in_flight": "Task open for Sam Patel to cover Leeds consultations (due 14 Nov)", "owner": "Sam Patel", "proposed_action_ids": ["a1f3"]},
   {"finding_id": "f-conv-online", "severity": "high", "metric": "Quote-to-sale conversion", "what_moved": "-38.0% week to date", "mechanism": "Online quote abandonment +61% in the same channel", "why": "New pricing live since 3 Nov shows the higher tier first; signups abandon at the quote step", "in_flight": "Initiative 'Online pricing simplification' in progress (Lee Grant); the conversion alert workflow did not fire", "owner": "Dana Okafor", "proposed_action_ids": ["b2e4", "c3d5"]},
   {"finding_id": "f-refund", "severity": "medium", "metric": "Refund rate", "what_moved": "above threshold for the third week", "mechanism": "concentrated in the Pro range", "why": "nothing recorded", "in_flight": "investigated 2026-10-24, came back 2026-11-03", "owner": "Dana Okafor", "proposed_action_ids": ["d4e6"]}],
 "section_counts": {"findings": 3, "people": 4, "decisions": 0, "blockers": 1, "absences": 1, "proposed_actions": 4, "tasks_scheduled": 1, "objectives": 2, "initiatives": 1},
 "sections": {"proposed_actions": [
   {"action_id": "a1f3", "kind": "nudge", "finding_id": "f-rev-leeds", "title": "Nudge Sam Patel to confirm Leeds consultation cover holds through 14 Nov", "to": "Sam Patel"},
   {"action_id": "b2e4", "kind": "do", "finding_id": "f-conv-online", "title": "Show the standard tier first on the online quote form until the pricing initiative lands", "assignee": "Dana Okafor"},
   {"action_id": "c3d5", "kind": "check_in", "finding_id": "f-conv-online", "title": "Check in on the Online pricing simplification initiative", "to": "Lee Grant"},
   {"action_id": "d4e6", "kind": "record_why", "finding_id": "f-refund", "title": "Record why refunds are concentrated in the Pro range", "assignee": "Dana Okafor"}]},
 "note": "Ask for a named section (findings, people, decisions, blockers, absences, proposed_actions, tasks_scheduled, objectives, initiatives) to read its rows."}
