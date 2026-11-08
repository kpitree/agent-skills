# CI evals

Two cheap tiers run on every pull request. Neither needs a KPI Tree workspace.

| Tier | Script | Needs | Catches |
| --- | --- | --- | --- |
| 0 | `validate.py` | nothing (stdlib) | structure: names, descriptions, links, tool names against `catalogue.json`, routing cases, the plugin eval suite |
| 1 | `routing_eval.py` | an Anthropic key | a prompt routing to the wrong skill, or an out-of-scope prompt routing to any skill |

```bash
python3 evals/ci/validate.py
python3 -m unittest discover -s evals/ci -p 'test_*.py'
python3 -m pip install -r evals/ci/requirements.txt
python3 evals/ci/routing_eval.py --compare-to origin/main   # what a pull request runs
python3 evals/ci/routing_eval.py                            # what main runs
```

Tier 1 shows the model nothing but the skill catalogue (every `name` and
`description` from `skills/*/SKILL.md`) and asks which skill handles each
prompt. Cases come from `skills/<skill>/evals/evals.json` and the out-of-scope
prompts in `negative-cases.json`. On a pull request the catalogue is built twice,
from the branch and from the base, and the run gates only on regressions that
reproduce in a fresh confirmation pass. On `main` it scores against the floors in
`baselines.json`; record them with `--update-baselines` once the suite is stable.

The full `claude plugin eval` suite, with the connector mocked, lives one level up
and is described in `evals/README.md`.
