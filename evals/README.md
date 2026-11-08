# Evals

Two things live here.

## The `claude plugin eval` suite

`evals/<case>/prompt.md` with `graders/*.md`, in the format `claude plugin eval` documents. The connector's tools are mocked under `mocks/kpitree/`, so a run never reaches a real workspace; it runs a full agent transcript per case and scores it with the graders. Every run spends tokens, so pilot it deliberately:

```bash
claude plugin eval . --runs 1 --ablation with-without --no-scaffold --no-publish
```

Then read `evals/results/*/aggregate-result.json`, check the plugin loaded, and ask whether you would have scored each answer the same way before trusting the graders. The headline number is the uplift (with the plugin minus without). Add a case when you change what a skill tells the agent to do.

## CI tiers

`evals/ci/` holds the two cheap tiers that run on every pull request: structural validation (tier 0) and skill routing (tier 1). See [`evals/ci/README.md`](ci/README.md).
