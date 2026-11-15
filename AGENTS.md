# Contributing with Agents

This file holds agent-specific operating instructions for this repository. Follow [CONTRIBUTING.md](CONTRIBUTING.md) for contributor policy: skill and agent authoring, validation, evals, versioning, changelog entries and pull request expectations.

## Before Editing

- Read the relevant existing skill, agent, command, README or eval file before changing it.
- Read `catalogue.json` before naming a tool. It is published from the connector itself and is the only source of truth for tool names, roles and features here.
- Keep edits scoped to the requested change and the repository's current patterns.
- Respect dirty worktrees. Do not revert changes you did not make.

## Repository Routing

- Skills go under `skills/<name>/SKILL.md`; the directory name and the frontmatter `name` match and start with `kpitree-`.
- Agent definitions live in `agents/`, slash commands in `commands/`.
- Routing cases for a skill live in `skills/<skill>/evals/evals.json`; the root `evals/` directory holds the CI scripts and the plugin eval suite.

Skills, agents and commands are auto-discovered. Do not add manifest registration for them. Do not add coding-editor integrations (Cursor, Copilot, Gemini CLI and the like): this repo targets Claude and ChatGPT, see CONTRIBUTING.md.

## Content Rules

- Every tool named in backticks must exist in `catalogue.json`. Do not name a tool to warn against it; drop the reference instead.
- Only the comparisons the catalogue marks recommended are recommended; the forbidden ones are named only in the sentence that forbids them.
- British English, no em dashes, no UUIDs in examples.

## Validation and Release

- Run `claude plugin validate . --profile directory` before marking work ready. The structural checks (names and descriptions, links, tool names against `catalogue.json`, routing cases, house style) run in the KPI Tree team's own test suite against this repository, on every pull request before it is merged: the directory accepts no scripts from a publisher it has not verified, so they are not in this repository.
- Exercise behaviour-changing skill or agent updates against a real KPI Tree workspace through the connector before marking the work ready.
- Add or update routing cases when a description changes.
- If distributed behaviour changes, bump the version in every manifest (`.claude-plugin/plugin.json`, both places in `.claude-plugin/marketplace.json`, and `plugin.json`) to the same number, and add a `CHANGELOG.md` entry in the same pull request. CI does not create a follow-up pull request.
- Documentation-only changes to `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CHANGELOG.md` or `evals/` usually need no version bump.
