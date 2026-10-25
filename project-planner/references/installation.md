# Install the planning skill

This skill ships in the [rajasekarm/skills](https://github.com/rajasekarm/skills) collection. Keep the whole `project-planner` folder together so its templates and references stay next to `SKILL.md`. It has no runtime dependency or machine-specific checkout path.

| Host | User-wide folder | Repository folder |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/project-planner/` | `.claude/skills/project-planner/` |
| Codex | `~/.codex/skills/project-planner/` (`$CODEX_HOME/skills`) | `.agents/skills/project-planner/` |

Ways to install:

- From a clone of the collection: `./install.sh project-planner` (both hosts, user-wide) or `./install.sh --scope project project-planner` from inside a project.
- Claude Code marketplace: `/plugin marketplace add rajasekarm/skills` then `/plugin install project-planner@rajasekarm-skills`.
- Codex: ask `$skill-installer` to install `project-planner` from `rajasekarm/skills`.

Inspect an existing installation before replacing it. Use the same source revision on every machine; copies do not update automatically, symlinks follow the checkout. Invoke `$project-planner` in Codex or `/project-planner` in Claude Code. Host discovery metadata stays in the skill package; generated planning documents are ordinary Markdown without YAML headers.

For example:

> Use project-planner to create a human-readable PRD.md and Milestone.md. Put all tasks for M1 in tasks/M1.md as a table with T1, T2, dependencies, completion conditions, and status. Keep each task's verification details in that same file. Prepare the next milestone for a worker without claiming it has run.

Project instructions can identify this workflow and the team's format examples. Installing a skill does not change execution permissions or migrate existing plans.

For several projects, use [multi-project planning](multi-project.md): shared standards, separate project plans, optional readable registry/portfolio, and `PROJECT/PLAN/M1/T1` references. Make the same documents available to reviewers and workers. A custom Python/LangGraph runtime must load them explicitly; this skill does not implement a runtime loader, queue, or dispatcher.
