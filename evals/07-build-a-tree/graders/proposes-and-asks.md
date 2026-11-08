---
type: llm
focus: last_message
weight: 1
---
PASS if the reply proposes the tree by metric name (Churn rate, Net revenue retention and Repeat purchase rate are the retention metrics the workspace has), says how they would roll up, notes that drawing an edge becomes driver evidence so only believed relationships should be drawn, and asks the person to confirm before building.
FAIL if it builds the tree without confirmation, invents metrics the workspace does not have, shows any UUID, or describes canvas groups as directory groups or teams.
