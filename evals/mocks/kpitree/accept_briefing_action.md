---
expect:
  artifact_uuid: string
  action_id: string
---
{"accepted": true, "action_id": "{{input.action_id}}", "result": "A task was created from the finding and assigned to its owner; accepting the same action again changes nothing.", "task": {"uuid": "t2b3c4d5-0000-4000-8000-000000000002", "status": "open"}}
