<p align="left">
  <img src="assets/logo.svg" alt="KPI Tree" width="240">
</p>

# KPI Tree Agent Skills

Official [KPI Tree](https://kpitree.co) skills for Claude (web, desktop, mobile and Cowork), Claude Code, and ChatGPT with Codex.

KPI Tree is a decision intelligence platform: it connects a business's metrics to the people who own them, the strategy they serve, and the recorded business context that explains why they move. This repository gives your assistant the KPI Tree connector and the skills that teach it to use KPI Tree the way it is meant to be used: what moved, which driver or segment is responsible, what the organisation has recorded as the reason, what is already being done, and what to do now.

## How It Works

Everything here is plain Markdown and a pointer at one remote MCP server. Nothing runs on your computer and nothing is fetched at install time beyond this repository.

- Ask in natural language about a metric, a segment, a review, a tree or something you know about the business
- The assistant loads the matching skill or agent from this repo when the request fits; there is nothing to memorise
- Every tool call goes to `https://mcp.kpitree.co/mcp`, which fronts your own KPI Tree workspace; you sign in with your KPI Tree account (OAuth) and every call runs with your own role and permissions

## Why This Repo

- One shared source of truth for how an assistant should work with KPI Tree, in Claude and in ChatGPT
- 7 skills covering routing and guardrails, metric investigation, segment questions, recording context and tasks, business reviews, the morning briefings and tree building
- 3 specialised agents for deeper multi-step work
- 4 slash commands for the routines people run every day and every week
- A connector tool catalogue, `catalogue.json`, published from the connector itself, so CI knows when a skill names a tool the connector no longer offers

This repository targets the assistants business people use. KPI Tree's users ask questions about metrics; they do not keep metric definitions in code, so there are no coding-editor plugins here.

## Platform Support

| Platform | Install method | Notes |
|----------|----------------|-------|
| [Claude](https://claude.ai) (web, desktop, mobile, Cowork) | [Plugin directory](#install-claude) | Skills and commands, with the connector on the plugin's Connectors tab |
| [Claude Code](https://claude.com/product/claude-code) | [Plugin marketplace](#install-claude-code) | Full plugin: 7 skills, 3 agents, 4 commands and the connector |
| [ChatGPT](https://chatgpt.com) and [Codex](https://openai.com/codex/) | [Agent Plugin](#install-chatgpt) | Skills and the connector as a plugin, in the Agent Plugins format both load |

Any other assistant that reads [Agent Skills](https://agentskills.io) and remote MCP servers can use the `skills/` directories and the connector address directly; those installs are not documented here.

## Installation

<a id="install-claude"></a>
### Claude (web, desktop, mobile, Cowork)

Open **Customize**, then **Plugins**, find **KPI Tree** in Discover and add it. On the plugin's **Connectors** tab, connect KPI Tree and sign in with your KPI Tree account. A plugin added on claude.ai also reaches Claude Code as a synced plugin.

<a id="install-claude-code"></a>
### Claude Code

Marketplace install (run separately):

```bash
/plugin marketplace add kpitree/agent-skills
```
```bash
/plugin install kpitree@kpitree
```

Git URL install (run separately):

```bash
/plugin marketplace add https://github.com/kpitree/agent-skills.git
```
```bash
/plugin install kpitree@kpitree
```

The plugin brings the connector with it (`.mcp.json`). The first call opens your browser to sign in to KPI Tree; run `/mcp` to see the connection or sign in again.

<a id="install-chatgpt"></a>
### ChatGPT and Codex

The repository is an [Agent Plugin](https://agent-plugins.org) (`plugin.json` and `mcp.json` at the root), the format ChatGPT and Codex load, with the skills and the connector bundled. The connector signs you in with OAuth; ChatGPT registers itself with KPI Tree's sign-in service, so there is no client ID or key to paste.

Once KPI Tree is listed in ChatGPT's plugin directory, add it from there. A ChatGPT Enterprise or Workspace admin can also import this repository as a marketplace (Admin, Plugins, Add, Import marketplace, with the repository URL) and make the plugin available to chosen roles. Otherwise install it through Codex (the Codex app, or the CLI):

```bash
codex plugin marketplace add kpitree/agent-skills
```
```bash
codex plugin add kpitree@kpitree
```

Start a new session afterwards; the connector asks you to sign in when it is first used. To add the connector on its own:

```bash
codex mcp add kpitree --url https://mcp.kpitree.co/mcp
codex mcp login kpitree
```

## Setup

### Your KPI Tree workspace

- A KPI Tree account whose workspace has AI assistant connections switched on. A workspace admin controls this under **Settings**, **Security**, **Policies**, and can make assistants read-only or limit them to directory groups.
- You sign in with your KPI Tree account through OAuth. The assistant never sees your password, and every call runs with your own role (viewer, editor or admin) and your workspace's features. Nothing else is contacted and no data is sent anywhere but your KPI Tree workspace.
- If you belong to several KPI Tree organisations, the sign-in asks which one to connect.

### One address for every workspace

`https://mcp.kpitree.co/mcp` is a gateway: it validates your sign-in, works out which workspace your organisation belongs to, and forwards the call to it. You never need a workspace-specific address, and a trial workspace is reached the same way as any other.

## What You Get

### Skills (7)

These activate from natural-language requests:

| Skill | Description |
|-------|-------------|
| **kpitree-basics** | How to use the connector well: routing any KPI Tree question to the right tool, roles, features and the guardrails |
| **kpitree-investigate** | The investigation sequence for "how is X doing" and "why did X change": what moved, which driver, the recorded why, prior art, one action |
| **kpitree-segments** | Questions about one site, branch, region, product line or tier across every metric cut to it |
| **kpitree-context** | Writing what you learn back: facts, causes, driver hypotheses, retractions, tasks and approvals, RACI fixes |
| **kpitree-briefing** | Reading and acting on the morning briefings: what to look at today, what changed, the personal action plan, accepting or dismissing a proposed action |
| **kpitree-review** | Weekly and monthly business reviews: health, objectives, initiatives, the portfolio and what is in flight |
| **kpitree-tree-builder** | Creating, extending, reshaping, cloning and linking KPI trees |

### Agents (3)

Built for heavier workflows where explicit delegation is useful (Claude Code):

| Agent | Description |
|-------|-------------|
| **kpitree-analyst** | Investigates a metric or segment end to end and delivers one narrative with a recommended action |
| **kpitree-reviewer** | Runs a business review: health, headline moves, objectives, initiatives, portfolio, decisions |
| **kpitree-architect** | Designs, builds, reshapes and clones KPI trees |

### Commands (4)

Run them as `/kpitree:<name>` in Claude Code and Cowork; in Claude chat the same routines apply when they fit:

| Command | Description |
|---------|-------------|
| `/kpitree:briefing` | What needs my attention today, from the briefing compiled this morning |
| `/kpitree:investigate <metric>` | Investigate a metric: what moved, which driver, the recorded why, what is in flight, what to do |
| `/kpitree:weekly-review [tree or team]` | Run this week's business review |
| `/kpitree:record <fact>` | Record a fact about the business so later analysis starts from it |

## Example Prompts

Ask naturally:

```text
"How is revenue doing this month?"
"Why did conversion rate drop last week?"
"What's going on at the Leeds branch?"
"What drives our average order value?"
"What should I look at today?"
"Go ahead with the nudge to Sam that the briefing suggested."
"Has anything been done about the drop in trial sign-ups?"
"Which objectives are at risk this quarter?"
"Which initiatives should we double down on, fix or stop?"
"Bob is off this week, his branch's consultations will be down."
"Build a KPI tree for customer retention."
"Give every store the same KPI tree as the flagship store."
```

For direct agent routing in Claude Code:

```text
Use the kpitree-analyst agent: why is churn creeping up, and who should act on it?
Use the kpitree-reviewer agent to prepare the monthly review pack for the commercial team
Use the kpitree-architect agent to add Net Revenue Retention to the Growth tree under Expansion Revenue
```

## Team Deployment (Claude Code)

To make this plugin available to your whole team automatically, add it to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "kpitree": {
      "source": {
        "source": "github",
        "repo": "kpitree/agent-skills"
      }
    }
  },
  "enabledPlugins": ["kpitree@kpitree"]
}
```

When team members trust the repository folder, Claude Code installs the marketplace and plugin for them. Each person still signs in to KPI Tree with their own account.

## Updating

### Claude Code

Enable auto-updates:
1. Run `/plugin`
2. Go to **Marketplaces**
3. Select the marketplace, then **Enable auto-update**

Or update manually from the `/plugin` menu.

### Claude and ChatGPT

Plugins added from a directory update with the directory listing. A Codex install is refreshed by re-running the install commands.

### How these skills track the connector

The skills document a moving target: the KPI Tree connector gains tools, and occasionally renames or removes one. `catalogue.json` is the connector's tool list as it publishes it, released here by the KPI Tree team whenever the connector changes. CI (`evals/ci/validate.py`) checks every tool a skill names against it, so a skill cannot point at a tool the connector no longer offers.

Releases are recorded in `CHANGELOG.md`. If a tool refuses or is missing for you, your workspace may not have that feature switched on, or your role may not include it; the `kpitree-basics` skill tells the assistant how to say so.

## Repository Structure

```
agent-skills/
├── .claude-plugin/
│   ├── marketplace.json       # Claude Code marketplace (also read by Codex)
│   ├── plugin.json            # Claude plugin manifest
│   └── icon.png
├── .agents/plugins/
│   └── marketplace.json       # Codex marketplace
├── .mcp.json                  # the connector, for Claude Code
├── mcp.json                   # the connector, for ChatGPT and Codex (Agent Plugins format)
├── plugin.json                # Agent Plugins manifest (ChatGPT, Codex)
├── catalogue.json             # the connector's tools and comparisons, published from the connector
├── versions.json              # the one version every manifest carries
├── skills/
│   ├── kpitree-basics/
│   ├── kpitree-investigate/
│   ├── kpitree-segments/
│   ├── kpitree-context/
│   ├── kpitree-review/
│   ├── kpitree-briefing/
│   └── kpitree-tree-builder/
│       ├── SKILL.md
│       └── evals/evals.json   # routing cases for tier 1
├── agents/
│   ├── kpitree-analyst.md
│   ├── kpitree-reviewer.md
│   └── kpitree-architect.md
├── commands/
│   ├── briefing.md
│   ├── investigate.md
│   ├── record.md
│   └── weekly-review.md
├── evals/
│   ├── README.md              # the claude plugin eval suite
│   ├── ci/                    # tier 0 validation and tier 1 routing
│   ├── mocks/kpitree/         # mocked connector responses for the plugin eval suite
│   └── <case>/                # prompt.md and graders/ per case
├── assets/
├── .github/
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── README.md
└── LICENSE
```

### Layout Conventions

Skill packages stay compatible with the [Agent Skills specification](https://agentskills.io) by keeping each skill's `SKILL.md` at the skill root. Supporting material lives beside it in focused subdirectories such as `references/`, `evals/` or `assets/`; keep references from `SKILL.md` shallow and relative to the skill root.

The root `evals/` directory is contributor tooling, not a distributed skill package. Two suites live there:

| Path | Purpose |
|------|---------|
| `evals/ci/validate.py` | Tier 0: structure, tool names against `catalogue.json`, eval files. Stdlib only, runs on every pull request |
| `evals/ci/routing_eval.py` | Tier 1: does each prompt route to the skill that owns it? One classification call per sample, paired against the base branch on pull requests |
| `evals/<case>/` | The `claude plugin eval` suite: full agent runs with the connector mocked, scored by graders. On demand, see `evals/README.md` |

Per-skill routing cases live with the skill they evaluate:

```text
skills/<skill>/evals/evals.json
```

## Documentation

- [KPI Tree documentation](https://docs.kpitree.co)
- [CI evals](evals/ci/README.md) and the [plugin eval suite](evals/README.md)
- [Claude Code plugin docs](https://code.claude.com/docs/en/plugins)
- [Agent Skills specification](https://agentskills.io)
- [Agent Plugins specification](https://agent-plugins.org)

## Privacy and Support

KPI Tree's [privacy policy](https://cdn.kpitree.co/legal/privacy-policy.pdf) and [terms of service](https://cdn.kpitree.co/legal/terms-of-service.pdf). Support: support@kpitree.co.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contributor guidance: skill and agent authoring, validation, evals, versioning, changelog entries and pull request expectations.

## Licence

MIT. The contents of this repository are released under the MIT licence (see [LICENSE](LICENSE)). KPI Tree itself is a separate product and service.
