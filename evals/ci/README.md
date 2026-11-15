# CI evals

Tier 0 runs on every pull request. It needs no KPI Tree workspace, no credential and
nothing beyond the Python standard library.

| Tier | Script | Needs | Catches |
| --- | --- | --- | --- |
| 0 | `validate.py` | nothing (stdlib) | structure: names, descriptions, links, tool names against `catalogue.json`, routing cases, the plugin eval suite |

```bash
python3 evals/ci/validate.py
python3 -m unittest discover -s evals/ci -p 'test_*.py'
```

The routing cases in `skills/<skill>/evals/evals.json` and the out-of-scope prompts in
`negative-cases.json` are validated here and scored against a model by a routing eval that
runs outside this repository: it needs an Anthropic key, and the plugin directory holds a
plugin for review whenever anything in its repository reads a credential.

The full plugin eval suite, with the connector mocked, lives one level up and is
described in `evals/README.md`.
