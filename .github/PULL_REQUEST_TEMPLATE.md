## What changes for someone who has the plugin installed

## Checklist

- [ ] Every tool named exists in `catalogue.json` and is used as its summary says
- [ ] Only the recommended period comparisons are recommended
- [ ] Routing cases were added or updated if a description changed
- [ ] Version bumped in every manifest if distributed behaviour changed
- [ ] `CHANGELOG.md` updated if distributed behaviour changed
- [ ] `claude plugin validate . --profile directory` and `git diff --check` pass
- [ ] Exercised against a real workspace where the behaviour changed
