# Routing cases

This folder holds `negative-cases.json`, prompts that belong to no skill. With the routing
cases in `skills/<skill>/evals/evals.json` they say what the descriptions should and should
not claim.

The structural checks that used to live here (names and descriptions, links, tool names
against `catalogue.json`, the routing cases, the plugin eval suite's files, house style) run
in the KPI Tree team's own test suite against a checkout of this repository, on every pull
request before it is merged. The Claude plugin directory accepts scripts only from
publishers it has verified, so this repository ships none. What you can run yourself:

```bash
claude plugin validate . --profile directory
```

The routing cases are scored against a model by a routing eval that also runs outside this
repository, as it needs an Anthropic key.

The full plugin eval suite, with the connector mocked, lives one level up and is
described in `evals/README.md`.
