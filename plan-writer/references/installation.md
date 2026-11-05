# Install the planning skill

This skill ships in the [rajasekarm/skills](https://github.com/rajasekarm/skills) collection. Keep the whole `plan-writer` folder together so its templates and references stay next to `SKILL.md`. It has no runtime dependency or machine-specific checkout path.

| Host | User-wide folder | Repository folder |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/plan-writer/` | `.claude/skills/plan-writer/` |
| Codex | `~/.codex/skills/plan-writer/` (`$CODEX_HOME/skills`) | `.agents/skills/plan-writer/` |

Ways to install:

- From a clone of the collection: `./install.sh plan-writer` (both hosts, user-wide) or `./install.sh --scope project plan-writer` from inside a project.
- Claude Code marketplace: `/plugin marketplace add rajasekarm/skills` then `/plugin install plan-writer@rajasekarm-skills`.
- Codex: ask `$skill-installer` to install `plan-writer` from `rajasekarm/skills`.

Inspect an existing installation before replacing it. Use the same source revision on every machine; copies do not update automatically, symlinks follow the checkout. Invoke `$plan-writer` in Codex or `/plan-writer` in Claude Code. Host discovery metadata stays in the skill package; generated planning documents are ordinary Markdown without YAML headers.

For example:

> Use plan-writer to write docs/plans/csv-export/plan.md: milestones with demos, a task table per milestone with dependencies and concrete verification, and the dependency graph. Planning only.

Project instructions can identify this workflow and the team's format examples. Installing a skill does not change execution permissions or migrate existing plans.

For several projects, use [multi-project planning](multi-project.md): one `plan.md` per plan, an optional registry/portfolio, and `PROJECT/PLAN/M1/T1` references. Make the same documents available to reviewers and workers. A custom Python/LangGraph runtime must load them explicitly; this skill does not implement a runtime loader, queue, or dispatcher.
