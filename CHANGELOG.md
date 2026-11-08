# Changelog

All notable changes to this repository are documented in this file. The version in `versions.json` is stamped into every manifest, so one number identifies one commit of this repo.

## [1.0.0] - 2026-11-08

_Summary: first release. One repository for Claude and ChatGPT._

**Added**
- Seven skills: `kpitree-basics`, `kpitree-investigate`, `kpitree-segments`, `kpitree-context`, `kpitree-review`, `kpitree-briefing`, `kpitree-tree-builder`.
- Three agents: `kpitree-analyst`, `kpitree-reviewer`, `kpitree-architect`.
- Four commands: `/kpitree:briefing`, `/kpitree:investigate`, `/kpitree:weekly-review`, `/kpitree:record`.
- Manifests for Claude, Cowork and Claude Code, and for ChatGPT and Codex (Agent Plugins, with the ChatGPT listing details and OAuth declaration), each pointing at `https://mcp.kpitree.co/mcp`.
- `catalogue.json`, the connector's tools and period comparisons as the connector publishes them, with tier 0 CI checking every tool a skill names against it.
- Tier 1 routing eval, paired against the base branch on pull requests, and a `claude plugin eval` suite with the connector mocked.
