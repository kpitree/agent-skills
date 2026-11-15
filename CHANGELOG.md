# Changelog

All notable changes to this repository are documented in this file. Every manifest carries the same version, so one number identifies one commit of this repo.

## [1.0.2] - 2026-11-15

_Summary: nothing about the skills changed; the repository ships no scripts._

**Changed**
- The structural checks moved out of the repository into the KPI Tree team's own test suite: the Claude plugin directory accepts scripts only from publishers it has verified. The out-of-scope routing cases stay in `evals/ci/`.
- One copy of the icon, in `assets/`.

## [1.0.1] - 2026-11-15

_Summary: a fix to one command and the listing's icon; the skills are unchanged._

**Fixed**
- The `/kpitree:investigate` command's description is quoted, so its frontmatter parses: the unquoted colon in it could leave the command without a description.

**Changed**
- The Claude manifest declares the plugin's icon for the directory listing.

## [1.0.0] - 2026-11-08

_Summary: first release. One repository for Claude and ChatGPT._

**Added**
- Seven skills: `kpitree-basics`, `kpitree-investigate`, `kpitree-segments`, `kpitree-context`, `kpitree-review`, `kpitree-briefing`, `kpitree-tree-builder`.
- Three agents: `kpitree-analyst`, `kpitree-reviewer`, `kpitree-architect`.
- Four commands: `/kpitree:briefing`, `/kpitree:investigate`, `/kpitree:weekly-review`, `/kpitree:record`.
- Manifests for Claude, Cowork and Claude Code, and for ChatGPT and Codex (Agent Plugins, with the ChatGPT listing details and OAuth declaration), each pointing at `https://mcp.kpitree.co/mcp`.
- `catalogue.json`, the connector's tools and period comparisons as the connector publishes them, with tier 0 CI checking every tool a skill names against it.
- A plugin eval suite for Claude Code with the connector mocked, and routing cases per skill.
