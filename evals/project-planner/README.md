# Project-planner evals

These five behavioral cases evaluate generated planning documents against small repository fixtures. They are host-neutral and use Python 3.9+ for structural checks, with no third-party dependencies. They do not call a model or consume API credits automatically.

| Case | Main behavior |
| --- | --- |
| existing-feature | Reuse implemented authentication while planning CSV export |
| unclear-requirement | Keep invoice-retention policy unresolved and affected work Draft/Blocked |
| branching-dependencies | Shared schema → independent endpoints → integration |
| existing-plan-update | Preserve identities and decisions while adding JSON export |
| unverified-runtime | Distinguish source inspection from unavailable VM acceptance |

## Run a case

From the repository root, prepare a fresh workspace (replace the case name as needed):

```bash
case_name=existing-feature
run_dir=$(mktemp -d)
cp -R "evals/project-planner/cases/$case_name/repo/." "$run_dir/"
printf 'Workspace: %s\n' "$run_dir"
cat "evals/project-planner/cases/$case_name/prompt.md"
```

Open a fresh agent session in that workspace. Make the current `project-planner` skill available through the host's normal installation mechanism, or supply its absolute SKILL.md path and access to its supporting files. Submit only `prompt.md`; keep case expectations outside the agent context. Start a fresh session/workspace for every repeat. Do not use this repository as the generated plan workspace.

Save the model identifier, settings, host version, exact prompt, skill snapshot/revision, generated documents, and tool trace with each run. A local uncommitted skill needs a captured snapshot; a Git commit alone does not identify its content. The trace is necessary to assess prohibited actions and distinguish observed checks from invented claims. No real credentials or services are needed.

Read `plan_dir` in the case's `expectations.json`, then check that directory. For example:

```bash
python3 evals/project-planner/check_structure.py \
  "$run_dir/docs/plans/eval-plan" \
  --workspace "$run_dir" \
  --expectations "evals/project-planner/cases/$case_name/expectations.json"
```

For `existing-plan-update`, use `$run_dir/docs/plans/report-export` instead. Exit status is 0 for structural pass, 1 for structural failure. Save the printed JSON, then review semantic expectations using [rubric.md](rubric.md). A structural pass alone is not an eval pass.

Keep captured runs under `results/<revision>/<case>/<repeat>/` if desired; generated results are ignored by Git. Record failures as well as successes. Compare baseline and candidate skills using the same fixture, model, host, and settings; begin with three repeats per case and report pass counts, dimension scores, and hard failures. Do not change prompts or expectations between baseline and candidate runs.

## Checker scope

The checker validates required files, milestone task filenames, table columns, nonempty cells, linked task IDs, matching detail sections, required execution/detail sections, dependency existence and cycles, inline local Markdown links/heading anchors, and absent YAML frontmatter. Task numbers may repeat across milestones. Cross-milestone dependencies use `M1/T1`; spaced display labels such as `[M1 / T1](M1.md#t1)` resolve to the same scoped ID. `None` may include an external condition in parentheses or after a semicolon, such as `None (needs VM access)` or `None; external stakeholder decision`; that condition still needs manual readiness review.

It supports the skill's ordinary Markdown format, not every Markdown extension: inline link destinations without spaces, ATX headings, and tables without escaped pipe characters. Reference-style links, raw HTML anchors, external URLs, requirement semantics, milestone roadmap coverage, status accuracy, and prose execution order require manual review. External project/plan task references fail closed with a manual-validation diagnostic; these fixtures require none. Paths and anchors are case-sensitive. The checker never executes fixture code.

Run checker regression tests with:

```bash
python3 -m unittest discover -s evals/project-planner -p 'test_*.py'
```

The bundled fixtures and checker tests are inputs and harness validation. They are not recorded model eval results.
