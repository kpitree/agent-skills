# Contributing to KPI Tree Agent Skills

This guide is the source of truth for contributor-facing policy: repository layout, skill and agent authoring, validation, evals, versioning, changelog entries and pull request expectations. The README is for people installing and using the repo; `AGENTS.md` is for agent-specific operating instructions; `evals/ci/README.md` and `evals/README.md` own the eval mechanics.

## Repository Layout

```text
agent-skills/
├── skills/            # one directory per skill, SKILL.md at its root
├── agents/            # agent definitions (*.md with frontmatter)
├── commands/          # slash commands (*.md with frontmatter)
├── evals/             # tier 0 CI and the claude plugin eval suite
├── catalogue.json     # the connector's tools and comparisons, published from the connector
├── .claude-plugin/    # Claude plugin metadata (Claude, Cowork, Claude Code)
├── .agents/plugins/   # Codex marketplace
├── plugin.json        # Agent Plugins manifest (ChatGPT, Codex)
├── CHANGELOG.md
├── README.md
└── AGENTS.md
```

Skills, agents and commands are auto-discovered from their directories; the manifests carry plugin-level metadata and version information only. Do not add a registration step for a new skill.

This repository deliberately targets the assistants business people use, Claude and ChatGPT, not coding editors. KPI Tree's users ask questions about metrics; they do not keep metric definitions in code the way an analytics engineer keeps a semantic model, so editor plugins (Cursor, Copilot, Gemini CLI and the like) would be maintained for nobody. Do not add them without a request from people who would use them.

## Setup

You need a KPI Tree account in a workspace with AI assistant connections switched on, and an agent that can reach `https://mcp.kpitree.co/mcp` (any of the installs in the README). Use a safe workspace: prefer a demo or staging workspace when testing anything that writes (context, tasks, trees, RACI).

## Skill Authoring

Each skill lives in its own directory and must contain `SKILL.md` with YAML frontmatter:

```yaml
---
name: skill-name
description: One paragraph saying what this skill does and when to use it, with the phrases people actually say.
---
```

The `description` is the primary routing signal, and it is all an agent sees before loading the skill. Write it to match how people naturally ask for the work, and say what the skill is not for when a neighbour could claim the same prompt. The Agent Skills specification caps it at 1024 characters; Claude Code truncates past that.

Skill bodies name tools in backticks, `analyze_metric`, and so do agents and commands. Every such name must exist in `catalogue.json` (or be a period comparison id, or one of the argument and signal names `evals/ci/validate.py` lists as explained). The catalogue is published from the connector itself; if a tool you need is not in it, the connector does not offer it.

Put the guardrails an agent must know before it calls anything near the top. Keep `SKILL.md` under 500 lines; move detail into `references/` beside it, linked one level deep.

## Agent Authoring

Agent definitions live in `agents/` as Markdown files with YAML frontmatter:

```yaml
---
name: agent-name
description: When to delegate to this agent. Be specific.
---
```

Agent bodies define:

- **Workflow**: numbered steps the agent follows
- **Conventions**: behavioural defaults, output shape and confirmation points
- **Skills You Should Use**: explicit companion skills

Agents orchestrate skills. Do not duplicate tool sequences or interpretation rules inside an agent; if an agent investigates a metric it follows `kpitree-investigate`, if it writes something back it follows `kpitree-context`.

## Command Authoring

Commands in `commands/` are Markdown with a `description` (and optionally an `argument-hint`) in the frontmatter, and `$ARGUMENTS` in the body. They are the routines people run by hand; keep them short and point at the skill that owns the detail.

## House Style

British English (organisation, behaviour, colour). No em dashes: use a comma, a full stop or a colon. Name things by what they are to the person, never by UUID. Tier 0 fails on an em dash in distributed prose.

## Validation

Before opening a pull request:

```bash
python3 evals/ci/validate.py                                   # tier 0
python3 -m unittest discover -s evals/ci -p 'test_*.py'
python3 .github/scripts/stamp_versions.py --check
claude plugin validate . --profile directory                   # what the Claude directory checks
```

For a change to skill or agent behaviour, also exercise it against a real workspace through the connector: run the prompts the skill is for and read back anything it wrote. Do not mark a pull request ready when the behaviour has only been checked against mocked responses.

Run `git diff --check` before requesting review.

## Evals

Tier 0 runs on every pull request (`evals/ci/README.md`). If you change a skill's `description`, or add a skill, add or update routing cases in `skills/<skill>/evals/evals.json`, and consider an out-of-scope case in `evals/ci/negative-cases.json` when the new wording could claim a prompt that belongs elsewhere. The routing eval that scores those cases against a model runs outside this repository, as it needs an Anthropic key and the plugin directory holds plugins whose code reads one.

The full `claude plugin eval` suite (`evals/README.md`) runs an agent against mocked connector responses and scores the transcript. Run it when you change what a skill tells the agent to do, not only what it says the skill is for.

## Staying in Sync with the Connector

The skills document the KPI Tree connector, which gains tools and occasionally renames or removes one. `catalogue.json` is published here by the KPI Tree team from the connector itself whenever it changes, so a connector change arrives as a catalogue change. Tier 0 then fails on any skill that names a tool no longer listed, which is the signal to update the prose. Fix references to a removed tool rather than annotating them: naming a tool that does not exist, even to warn against it, leaves the agent a plausible option that will fail.

## Versioning and Changelog

Bump the version when a person who already has the plugin installed would get different behaviour after updating:

- a skill `description` changes, affecting when it loads
- a skill, agent or command workflow, tool sequence or default changes
- a new skill, agent or command is added
- plugin metadata that people see changes

Documentation-only changes to `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CHANGELOG.md` or `evals/` usually do not need a bump.

Semantic versioning, always three components:

| Change type | Version component |
|---|---|
| Bug fixes, clarifications, doc corrections | `PATCH` |
| New skills, new features, behaviour changes | `MINOR` |
| Breaking changes to existing skill behaviour | `MAJOR` |

CI does not infer the level; pick it with the table above.

### One version, one place

`versions.json` at the repo root is the single source of truth. For a release, edit it, then stamp and verify the manifests before committing:

```bash
python3 .github/scripts/stamp_versions.py          # rewrite the manifests
python3 .github/scripts/stamp_versions.py --check  # verify they match
```

Commit `versions.json`, the stamped manifests and the changelog entry in the same pull request. Every manifest (Claude and Agent Plugins) ships from the same commit, so one number identifies one commit of this repo.

Document user-visible changes in `CHANGELOG.md` under the version, with `Added`, `Changed` and `Fixed` sections and the release date:

```markdown
## [1.1.0] - YYYY-MM-DD

**Added**
- Description of new capability

**Changed**
- Description of behaviour change

**Fixed**
- Description of bug fix
```

## Pull Request Checklist

- [ ] Skill, agent or command frontmatter routes correctly
- [ ] Every tool named exists in `catalogue.json` and is used as its summary says
- [ ] Only the recommended period comparisons are recommended
- [ ] Behaviour was exercised end to end against a real workspace where relevant
- [ ] Routing cases were added or updated if a description changed
- [ ] `versions.json` was bumped and the manifests stamped if distributed behaviour changed
- [ ] `CHANGELOG.md` was updated if distributed behaviour changed
- [ ] `python3 evals/ci/validate.py` and `git diff --check` pass

## What to Avoid

- Do not invent tool names or arguments. The catalogue is the contract.
- Do not recommend a partial current period against a full previous one.
- Do not add a manifest registration step for skills, agents or commands; directories are auto-discovered.
- Do not add coding-editor integrations; see Repository Layout.
- Do not mark real-workspace validation complete when only mocked responses were used.

## Licence

By contributing to this repository, you agree that your contributions will be licensed under the MIT licence that covers the project.
