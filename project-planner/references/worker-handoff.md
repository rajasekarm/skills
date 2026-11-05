# Handoff to another person or agent

Read this when a task will be executed in a separate session, by another agent, or on another machine. The worker should need only the plan, not the planner's conversation.

## What to hand over

- The `plan.md` path and the full task reference: `M1/T2` inside a plan, `PROJECT/PLAN/M1/T2` across plans.
- The specification commit and the code repository plus starting revision. They may differ; pin both. A local draft is not automatically available on another machine.
- The environment the task needs: runtime versions, services, data, and credential names (never values). An environment label is not proof that it is configured; check it before pickup.

## Readiness

A task is Ready when every dependency is Done (accepted, not merely started or submitted), its prerequisite code is in the starting revision, and it has no open decision. External prerequisites need the actual accepted artifact or service version.

One owner updates status: the established tracker if there is one, otherwise a single coordinator editing `plan.md`. Parallel agents return results instead of editing the shared plan. Parallel work needs isolated workspaces and non-overlapping files, migrations, contracts, and services, or an explicit integration task.

## Claiming and resuming

The runner, not a Markdown edit, owns claims. Before resuming or redispatching, inspect existing branches, artifacts, and partial work and preserve them. A stale heartbeat alone is no reason to start a duplicate run. If the task specification changes materially mid-run, record the change and hand it over explicitly.

## Doing the work

Read repository rules, the plan's Goal, Context, Decisions, the task row, and its notes. Confirm the base and prerequisites, implement within scope, and run the task's Verify. Report missing inputs, missing authority, or invalidated assumptions as blockers instead of weakening the acceptance check. Planning grants no permission to commit, publish, or deploy.

## Returning the result

Return: what changed, the Verify result (passed, failed, or not run, with evidence), the revisions used, unresolved gaps, and the suggested next step. Implementation, checks, acceptance, merge, and deployment are separate facts. A reviewer accepts the result before the task becomes Done.
