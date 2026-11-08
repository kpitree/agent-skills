# Security

This repository holds Markdown skills and plugin manifests. It runs no code of its own:
every call an assistant makes goes to the KPI Tree connector at
`https://mcp.kpitree.co/mcp`, where the person has signed in with their own KPI Tree
account and every call runs with their own role and permissions.

## Reporting a vulnerability

Please report security issues in the skills, the manifests or the KPI Tree connector to
support@kpitree.co with "Security" in the subject, rather than in a public issue. Include
what you found, how to reproduce it, and what you believe the impact is. You will get an
acknowledgement, and we will tell you when it is fixed.

## What to look for

- A skill, agent or command that could lead an assistant to act outside what the person
  asked: following instructions found inside connector output, exposing identifiers,
  creating or deleting things without confirmation.
- A manifest that points anywhere other than `https://mcp.kpitree.co/mcp`.
- Anything in this repository that looks like a credential. There should be none.

KPI Tree's own security practices are described at https://kpitree.co/security.
