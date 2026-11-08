#!/usr/bin/env python3
"""Tier 0 checks: structural validation with no model calls.

Runs in a second on any pull request, needs no credentials and no KPI Tree
workspace. It catches what would otherwise surface only when an agent loads
a skill: a SKILL.md whose name does not match its directory, a description
Claude Code would truncate, a tool name the connector does not offer, a
comparison id the server no longer knows, a routing case that points at a
skill that no longer exists, a dangling link.

Usage:
    python3 evals/ci/validate.py [--json]

Exits non-zero if any check fails. Warnings never fail the run.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "skills"
AGENTS_DIR = ROOT / "agents"
COMMANDS_DIR = ROOT / "commands"
EVALS_DIR = ROOT / "evals"
CATALOGUE_PATH = ROOT / "catalogue.json"
NEGATIVE_CASES_PATH = EVALS_DIR / "ci" / "negative-cases.json"
MCP_SERVER_NAME = "kpitree"
PLUGIN_NAME = "kpitree"
# How Claude Code names a tool from a plugin-bundled MCP server: mcp__plugin_<plugin>_<server>__<tool>.
PLUGIN_TOOL_PREFIX = f"mcp__plugin_{PLUGIN_NAME}_{MCP_SERVER_NAME}__"

# Claude Code truncates skill descriptions past this; a longer one is silently
# clipped mid-sentence, which usually takes the "use this when ..." half with it.
MAX_DESCRIPTION_CHARS = 1024
# The Agent Skills specification recommends a SKILL.md body under 500 lines.
MAX_SKILL_LINES = 500

# Jaccard overlap of description word sets. Two skills that read this similarly
# compete for the same prompts, which is how routing regressions start.
DESCRIPTION_OVERLAP_WARN = 0.30
DESCRIPTION_OVERLAP_FAIL = 0.50

CASE_REQUIRED_KEYS = ("id", "question", "expected_skill", "expected_behavior")
CASE_OPTIONAL_KEYS = ("ground_truth", "depends_on")

# Argument names, decision signals and output fields the prose explains in
# backticks. Everything else in backticks that looks like snake_case must be a
# tool the connector lists or a period comparison id.
EXPLAINED_NAMES = {
    "dimension_value", "entity", "owner", "tree", "skip_tools", "active_context", "status",
    "windows_moving_wrong_way", "progress", "execution_progress",
    "responsible", "accountable", "consulted", "informed", "dimension_siblings",
}

BACKTICKED = re.compile(r"`([a-z][a-z0-9_]*)`")
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FIXTURE_RE = re.compile(r"\{\{file:fixtures/([^}]+)\{")
EM_DASH = chr(0x2014)  # the em dash, spelt so this file never contains one
STOPWORDS = {
    "a", "an", "and", "the", "or", "for", "to", "of", "in", "on", "with", "when",
    "this", "that", "use", "using", "skill", "kpi", "tree", "via", "from",
    "it", "is", "are", "as", "by", "at", "into", "also", "you", "your", "user",
    "someone", "wants", "not", "but", "e", "g", "any", "asks", "about",
}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"{where}: {message}")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def parse_frontmatter(path: Path, report: Report) -> dict[str, str]:
    """Read the leading `---` block as flat `key: value` pairs.

    Every frontmatter block in this repo is single-line scalars, so this stays
    stdlib-only rather than pulling PyYAML in for CI. A block that needs more
    than that should fail loudly here instead of being half-parsed.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        report.error(rel(path), "missing YAML frontmatter (file must start with ---)")
        return {}

    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            report.error(rel(path), f"frontmatter line is not `key: value`: {line!r}")
            continue
        key, value = line.split(":", 1)
        if key != key.strip():
            report.error(rel(path), f"frontmatter key {key.strip()!r} is indented; nested keys are not supported")
            continue
        fields[key.strip()] = value.strip().strip('"').strip("'")

    report.error(rel(path), "frontmatter block is never closed with ---")
    return fields


def discover_skills() -> list[str]:
    if not SKILLS_DIR.is_dir():
        return []
    return sorted(p.name for p in SKILLS_DIR.iterdir() if (p / "SKILL.md").is_file())


def discover_agents() -> list[str]:
    if not AGENTS_DIR.is_dir():
        return []
    return sorted(p.stem for p in AGENTS_DIR.glob("*.md"))


def check_markdown_links(path: Path, report: Report) -> None:
    body = path.read_text(encoding="utf-8")
    for target in MD_LINK_RE.findall(body):
        target = target.split(" ", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = (path.parent / target.split("#", 1)[0]).resolve()
        if not resolved.exists():
            report.error(rel(path), f"link target does not exist: {target}")


def check_house_style(path: Path, report: Report) -> None:
    text = path.read_text(encoding="utf-8")
    if EM_DASH in text:
        line = next(i for i, l in enumerate(text.splitlines(), 1) if EM_DASH in l)
        report.error(rel(path), f"line {line} uses an em dash; use a comma, a full stop or a colon")


def load_catalogue(report: Report) -> dict:
    if not CATALOGUE_PATH.is_file():
        report.error("catalogue.json", "missing; tool names cannot be checked (see CONTRIBUTING.md)")
        return {"tools": [], "comparisons": [], "server": {}}
    try:
        data = json.loads(CATALOGUE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.error("catalogue.json", f"is not valid JSON: {exc}")
        return {"tools": [], "comparisons": [], "server": {}}

    seen: set[str] = set()
    for entry in data.get("tools", []):
        name = entry.get("name", "")
        where = f"catalogue.json tool {name or '?'}"
        if not name:
            report.error(where, "has no name")
        if name in seen:
            report.error(where, "is listed twice")
        seen.add(name)
        if not entry.get("title"):
            report.error(where, "has no title (the Claude directory requires one)")
        # Both directories read these; ChatGPT's requires all three as explicit booleans.
        for flag in ("read_only", "destructive", "open_world"):
            if not isinstance(entry.get(flag), bool):
                report.error(where, f"has no explicit {flag} flag")
    for comparison in data.get("comparisons", []):
        if not comparison.get("id"):
            report.error("catalogue.json comparisons", "an entry has no id")
    return data


def check_server_url(catalogue: dict, report: Report) -> None:
    """Every manifest that names the connector names the same address."""
    expected = catalogue.get("server", {}).get("url")
    if not expected:
        report.error("catalogue.json", "server.url is missing")
        return
    for manifest, pick in (
        (".mcp.json", lambda d: d["mcpServers"][MCP_SERVER_NAME]["url"]),
        ("mcp.json", lambda d: d["mcpServers"][MCP_SERVER_NAME]["url"]),
    ):
        path = ROOT / manifest
        if not path.is_file():
            report.error(manifest, "missing")
            continue
        try:
            found = pick(json.loads(path.read_text(encoding="utf-8")))
        except (KeyError, json.JSONDecodeError) as exc:
            report.error(manifest, f"does not name the {MCP_SERVER_NAME!r} server as expected: {exc!r}")
            continue
        if found != expected:
            report.error(manifest, f"points at {found}, catalogue.json says {expected}")


def check_tool_names(known: set[str], report: Report) -> None:
    """Every snake_case name in backticks is a tool, a comparison or an explained argument."""
    documents = [
        *SKILLS_DIR.glob("*/SKILL.md"),
        *SKILLS_DIR.glob("*/references/*.md"),
        *(AGENTS_DIR.glob("*.md") if AGENTS_DIR.is_dir() else []),
        *(COMMANDS_DIR.glob("*.md") if COMMANDS_DIR.is_dir() else []),
    ]
    for path in sorted(documents):
        names = set(BACKTICKED.findall(path.read_text(encoding="utf-8")))
        unknown = sorted(n for n in names - known if "_" in n)
        if unknown:
            report.error(rel(path), "names tools or comparisons the connector does not list: " + ", ".join(unknown))


def check_skill_docs(skills: list[str], report: Report) -> dict[str, str]:
    descriptions: dict[str, str] = {}
    for skill in skills:
        path = SKILLS_DIR / skill / "SKILL.md"
        fields = parse_frontmatter(path, report)

        name = fields.get("name", "")
        if not name:
            report.error(rel(path), "frontmatter is missing `name`")
        elif name != skill:
            report.error(rel(path), f"frontmatter name {name!r} does not match directory {skill!r}")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", skill) or len(skill) > 64:
            report.error(rel(path), f"directory name {skill!r} is not a valid skill name (lowercase, digits, single hyphens, 64 max)")

        description = fields.get("description", "")
        if not description:
            report.error(rel(path), "frontmatter is missing `description`")
        elif len(description) > MAX_DESCRIPTION_CHARS:
            report.error(
                rel(path),
                f"description is {len(description)} chars, over the {MAX_DESCRIPTION_CHARS} limit "
                "(it will be truncated before an agent reads the end of it)",
            )
        else:
            descriptions[skill] = description

        lines = path.read_text(encoding="utf-8").count("\n") + 1
        if lines > MAX_SKILL_LINES:
            report.warn(rel(path), f"is {lines} lines; the Agent Skills specification recommends under {MAX_SKILL_LINES}. Move detail into references/")

        check_markdown_links(path, report)
        check_house_style(path, report)
        for reference in sorted((SKILLS_DIR / skill / "references").glob("*.md")):
            check_markdown_links(reference, report)
            check_house_style(reference, report)
    return descriptions


def check_agents_and_commands(report: Report) -> None:
    for path in sorted(AGENTS_DIR.glob("*.md")) if AGENTS_DIR.is_dir() else []:
        fields = parse_frontmatter(path, report)
        if fields.get("name", "") != path.stem:
            report.error(rel(path), f"frontmatter name {fields.get('name', '')!r} does not match file stem {path.stem!r}")
        if not fields.get("description"):
            report.error(rel(path), "frontmatter is missing `description`")
        check_markdown_links(path, report)
        check_house_style(path, report)

    for path in sorted(COMMANDS_DIR.glob("*.md")) if COMMANDS_DIR.is_dir() else []:
        fields = parse_frontmatter(path, report)
        if not fields.get("description"):
            report.error(rel(path), "frontmatter is missing `description`")
        check_markdown_links(path, report)
        check_house_style(path, report)


def check_routing_cases(skills: list[str], report: Report) -> int:
    """`skills/<skill>/evals/evals.json`: the prompts tier 1 routes."""
    known = set(skills)
    total_cases = 0

    for skill in skills:
        path = SKILLS_DIR / skill / "evals" / "evals.json"
        if not path.is_file():
            report.warn(f"skills/{skill}", "has no evals/evals.json, so nothing checks that prompts route to it")
            continue

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report.error(rel(path), f"is not valid JSON: {exc}")
            continue

        if str(data.get("version", "")) != "1":
            report.error(rel(path), f"unexpected schema version {data.get('version')!r}, expected \"1\"")
        if data.get("skill_name") != skill:
            report.error(rel(path), f"skill_name {data.get('skill_name')!r} does not match directory {skill!r}")

        cases = data.get("cases")
        if not isinstance(cases, list) or not cases:
            report.error(rel(path), "cases must be a non-empty list")
            continue

        seen_ids: set[str] = set()
        for case in cases:
            total_cases += 1
            if not isinstance(case, dict):
                report.error(rel(path), "every case must be an object")
                continue
            case_id = str(case.get("id", "?"))
            where = f"{rel(path)} case {case_id}"

            for key in CASE_REQUIRED_KEYS:
                if key not in case:
                    report.error(where, f"missing required key `{key}`")
            for key in case:
                if key not in CASE_REQUIRED_KEYS + CASE_OPTIONAL_KEYS:
                    report.error(where, f"unknown key `{key}`")

            if case_id in seen_ids:
                report.error(where, "duplicate case id")
            seen_ids.add(case_id)

            if not isinstance(case.get("question"), str) or not case.get("question", "").strip():
                report.error(where, "`question` must be a non-empty string")
            if "ground_truth" in case and (not isinstance(case["ground_truth"], str) or not case["ground_truth"].strip()):
                report.error(where, "`ground_truth` must be a non-empty string when present")

            behaviours = case.get("expected_behavior")
            if not isinstance(behaviours, list) or not behaviours:
                report.error(where, "`expected_behavior` must be a non-empty list")
            elif not all(isinstance(item, str) and item.strip() for item in behaviours):
                report.error(where, "`expected_behavior` entries must be non-empty strings")

            if case.get("expected_skill") not in known:
                report.error(where, f"expected_skill {case.get('expected_skill')!r} is not a skill in skills/")

            depends_on = case.get("depends_on", [])
            if not isinstance(depends_on, list):
                report.error(where, "`depends_on` must be a list")
            else:
                for dep in depends_on:
                    if dep == skill:
                        report.error(where, f"depends_on lists its own skill {dep!r}")
                    elif dep not in known:
                        report.error(where, f"depends_on references unknown skill {dep!r}")

    return total_cases


def check_negative_cases(skills: list[str], report: Report) -> int:
    """Out-of-scope prompts that must route to `none`.

    These have no owning skill and no expected behaviour. They exist so tier 1
    can see a description that gets greedier, not just one that gets weaker.
    """
    if not NEGATIVE_CASES_PATH.is_file():
        report.warn("evals/ci/negative-cases.json", "missing; tier 1 cannot detect over-triggering")
        return 0

    try:
        data = json.loads(NEGATIVE_CASES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.error(rel(NEGATIVE_CASES_PATH), f"is not valid JSON: {exc}")
        return 0

    where_file = rel(NEGATIVE_CASES_PATH)
    if not isinstance(data, dict):
        report.error(where_file, "must be an object")
        return 0
    if str(data.get("version", "")) != "1":
        report.error(where_file, f"unexpected schema version {data.get('version')!r}, expected \"1\"")

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        report.error(where_file, "cases must be a non-empty list")
        return 0

    seen_ids: set[str] = set()
    seen_questions: set[str] = set()
    for position, case in enumerate(cases, 1):
        where = f"{where_file} entry {position}"
        if not isinstance(case, dict):
            report.error(where, "case must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            report.error(where, "`id` must be a non-empty string")
            continue
        where = f"{where_file} case {case_id}"
        for key in case:
            if key not in ("id", "question", "kind"):
                report.error(where, f"unknown key `{key}`")
        if case_id in seen_ids:
            report.error(where, "duplicate case id")
        seen_ids.add(case_id)

        question = case.get("question")
        if not isinstance(question, str) or not question.strip():
            report.error(where, "`question` must be a non-empty string")
            continue
        normalised = question.strip().lower()
        if normalised in seen_questions:
            report.error(where, "duplicate question")
        seen_questions.add(normalised)

        # A negative case naming a real skill is almost always a mistake: it
        # reads as in-scope work while being labelled out-of-scope.
        for skill in skills:
            if skill in question:
                report.error(where, f"names the skill {skill!r}, so it is not out-of-scope")

    return len(cases)


def check_plugin_eval_cases(tool_names: set[str], report: Report) -> int:
    """The `claude plugin eval` suite: evals/<case>/prompt.md with graders/."""
    cases = 0
    for prompt in sorted(EVALS_DIR.glob("*/prompt.md")):
        cases += 1
        case_dir = prompt.parent
        parse_frontmatter(prompt, report)
        graders = sorted((case_dir / "graders").glob("*.md"))
        if not graders:
            report.error(rel(case_dir), "has no graders/*.md, so nothing scores it")
        for grader in graders:
            fields = parse_frontmatter(grader, report)
            if not fields.get("type"):
                report.error(rel(grader), "frontmatter is missing `type`")
            for field in ("tool", "before", "after"):
                tool = fields.get(field, "")
                if not tool.startswith("mcp__"):
                    continue
                # Claude Code names a plugin-bundled MCP tool after the plugin and the
                # server key, so a grader written against the bare server key never
                # matches and the case passes or fails for the wrong reason.
                if not tool.startswith(PLUGIN_TOOL_PREFIX):
                    report.error(rel(grader), f"grades {tool}; plugin MCP tools are named {PLUGIN_TOOL_PREFIX}<tool>")
                elif tool.removeprefix(PLUGIN_TOOL_PREFIX) not in tool_names:
                    report.error(rel(grader), f"grades a tool the connector does not list: {tool}")
    mocks_dir = EVALS_DIR / "mocks" / MCP_SERVER_NAME
    for mock in sorted(mocks_dir.glob("*.md")):
        if mock.stem.startswith("_"):
            continue
        if mock.stem not in tool_names:
            report.error(rel(mock), "mocks a tool the connector does not list")
        # A fixture reference is resolved from the call's arguments at run time; the
        # fixture family it names must at least exist.
        for match in FIXTURE_RE.finditer(mock.read_text(encoding="utf-8")):
            prefix = match.group(1).split("{", 1)[0]
            if not list((mocks_dir / "fixtures").glob(f"{prefix}*")):
                report.error(rel(mock), f"names fixtures {prefix}* but none exist")
    tools_list = mocks_dir / "_tools.json"
    if tools_list.is_file():
        try:
            listed = {entry["name"] for entry in json.loads(tools_list.read_text(encoding="utf-8"))["tools"]}
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            report.error(rel(tools_list), f"is not a tools/list response: {exc!r}")
        else:
            if listed != tool_names:
                report.error(rel(tools_list), "lists different tools from catalogue.json; regenerate both together")
    return cases


def tokenize(description: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", description.lower())
    return {word for word in words if word not in STOPWORDS and len(word) > 2}


def check_description_overlap(descriptions: dict[str, str], report: Report) -> list[tuple[str, str, float]]:
    scored: list[tuple[str, str, float]] = []
    names = sorted(descriptions)
    for i, left in enumerate(names):
        for right in names[i + 1:]:
            a, b = tokenize(descriptions[left]), tokenize(descriptions[right])
            if not a or not b:
                continue
            overlap = len(a & b) / len(a | b)
            scored.append((left, right, overlap))
            if overlap >= DESCRIPTION_OVERLAP_FAIL:
                report.error(
                    "skill descriptions",
                    f"{left} and {right} overlap {overlap:.0%}; they will compete for the same prompts",
                )
            elif overlap >= DESCRIPTION_OVERLAP_WARN:
                report.warn(
                    "skill descriptions",
                    f"{left} and {right} overlap {overlap:.0%}; consider sharpening the boundary between them",
                )
    return sorted(scored, key=lambda item: item[2], reverse=True)


def write_step_summary(lines: list[str]) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    with open(summary_path, "a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable results instead of text")
    args = parser.parse_args()

    report = Report()
    skills = discover_skills()
    if not skills:
        report.error("skills/", "no skills found")

    catalogue = load_catalogue(report)
    tool_names = {entry.get("name", "") for entry in catalogue.get("tools", [])}
    comparison_ids = {entry.get("id", "") for entry in catalogue.get("comparisons", [])}
    check_server_url(catalogue, report)

    descriptions = check_skill_docs(skills, report)
    check_agents_and_commands(report)
    check_tool_names(tool_names | comparison_ids | EXPLAINED_NAMES | set(skills) | set(discover_agents()), report)
    total_cases = check_routing_cases(skills, report)
    negative_cases = check_negative_cases(skills, report)
    plugin_cases = check_plugin_eval_cases(tool_names, report)
    overlaps = check_description_overlap(descriptions, report)

    if args.json:
        print(json.dumps({
            "skills": skills,
            "tools": len(tool_names),
            "routing_cases": total_cases,
            "negative_cases": negative_cases,
            "plugin_eval_cases": plugin_cases,
            "errors": report.errors,
            "warnings": report.warnings,
            "top_description_overlaps": [
                {"a": a, "b": b, "overlap": round(score, 4)} for a, b, score in overlaps[:5]
            ],
        }, indent=2))
        return 1 if report.errors else 0

    print(f"Checked {len(skills)} skills against {len(tool_names)} connector tools, "
          f"{total_cases} routing cases, {negative_cases} out-of-scope cases, "
          f"{plugin_cases} plugin eval cases.")
    if overlaps:
        a, b, score = overlaps[0]
        print(f"Closest description pair: {a} / {b} ({score:.0%} overlap)")

    for warning in report.warnings:
        print(f"WARN  {warning}")
    for error in report.errors:
        print(f"ERROR {error}")

    summary = ["### Tier 0: structural validation", "",
               f"{len(skills)} skills, {len(tool_names)} connector tools, {total_cases} routing cases, "
               f"{negative_cases} out-of-scope cases, {plugin_cases} plugin eval cases."]
    if report.errors:
        summary += ["", "**Errors**", ""] + [f"- {item}" for item in report.errors]
    if report.warnings:
        summary += ["", "**Warnings**", ""] + [f"- {item}" for item in report.warnings]
    if not report.errors:
        summary += ["", "All structural checks passed."]
    write_step_summary(summary)

    if report.errors:
        print(f"\n{len(report.errors)} error(s).")
        return 1
    print("\nAll structural checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
