---
expect:
  metric_uuid: string
---
{"metric": "Revenue (Leeds)", "parents": [{"name": "Revenue", "uuid": "8f1c2d3e-4b5a-4c6d-8e7f-9a0b1c2d3e4f", "tree": "Company"}], "children": [{"name": "Consultations (Leeds)", "uuid": "9e8d7c6b-5a4f-4e3d-8c2b-1a0f9e8d7c6b"}, {"name": "Quotes issued (Leeds)", "uuid": "2b3c4d5e-6f7a-4b8c-9d0e-1f2a3b4c5d6e"}],
 "trees": [{"name": "Leeds branch", "role": "root"}, {"name": "Company", "role": "node"}],
 "dimension_siblings": {"dimension": "branch", "value": "Leeds", "metrics": [
   {"name": "Revenue (Leeds)", "uuid": "4d5e6f7a-8b9c-4d1e-9f2a-3b4c5d6e7f8a", "kind": "money"},
   {"name": "Consultations (Leeds)", "uuid": "9e8d7c6b-5a4f-4e3d-8c2b-1a0f9e8d7c6b", "kind": "operational"},
   {"name": "Quotes issued (Leeds)", "uuid": "2b3c4d5e-6f7a-4b8c-9d0e-1f2a3b4c5d6e", "kind": "operational"},
   {"name": "Cancellations (Leeds)", "uuid": "3c4d5e6f-7a8b-4c9d-8e1f-2a3b4c5d6e7f", "kind": "operational"}]}}
