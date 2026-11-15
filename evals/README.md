# Evals

Two things live here.

## The `claude plugin eval` suite

`evals/<case>/prompt.md` with `graders/*.md`, in the format `claude plugin eval` documents. The connector's tools are mocked under `mocks/kpitree/`, so a run never reaches a real workspace; it runs a full agent transcript per case and scores it with the graders. Every run spends tokens, so pilot it deliberately:

```bash
claude plugin eval . --runs 1 --ablation with-without --no-scaffold --no-publish
```

Then read `evals/results/*/aggregate-result.json`, check the plugin loaded, and ask whether you would have scored each answer the same way before trusting the graders. The headline number is the uplift (with the plugin minus without). Add a case when you change what a skill tells the agent to do.

A grader that names a connector tool uses the name Claude Code gives a plugin-bundled MCP tool, `mcp__plugin_kpitree_kpitree__<tool>`; the mocks, by contrast, are keyed by the bare server name, `mocks/kpitree/<tool>.md`. Tier 0 checks both.

The mocks describe one fictional workspace (a revenue decline led by the Leeds branch, an online conversion drop after a pricing change, a refund rate finding) in the shapes the connector really returns: `analyze_metric` as a JSON signals preamble, Markdown sections, a CONTEXT_DATA block and a NEXT STEPS block; `get_metric_drivers` as the Markdown drivers report; context as a fenced, untrusted-data block. Tools whose answer depends on the metric asked about read a fixture per metric from `mocks/kpitree/fixtures/`, chosen by the call's `metric_uuid`. Every case `expect`s only the argument types, so a call with the wrong shape aborts the run rather than passing by accident. `mocks/kpitree/_tools.json` is the connector's own tools/list response, so every mocked tool carries its real description and input schema and the agent reads exactly what it would read live. Record real responses from a demo workspace (`--mocks record --allow-real-servers`) before trusting the uplift numbers; a hand-written mock body cannot steer the model exactly as the connector does.

## CI tiers

`evals/ci/` holds tier 0, the structural validation that runs on every pull request. See [`evals/ci/README.md`](ci/README.md).
