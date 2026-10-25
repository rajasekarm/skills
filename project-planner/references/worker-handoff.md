# Handoff to another person or agent

The worker should receive a useful plan, not instructions that require the planner's conversation. Share the PRD, milestone overview, relevant milestone task file, and necessary supporting references.

## Finding the assignment

Use `PROJECT/PLAN/M1/T1` as the full reference. The human-facing task table can display `T1`; its enclosing document supplies the milestone, project, and plan. Read the execution order below the table, then resolve the linked `### T1` section under Detailed task information in `tasks/M1.md`. For several projects, use [the registry and priority rules](multi-project.md).

For dispatch, record the specification repository/file/commit, task reference/revision, code repository/base, accepted dependency versions, and execution target. The code and specification repositories may differ. Pin both explicitly; do not embed a commit's own SHA into the file being committed. A local draft is not automatically published to the VM.

Keep secrets and absolute machine checkout paths in runtime configuration. Verify the target's services and capabilities before pickup rather than treating an environment label as proof.

## Readiness and dependencies

A task is Ready when its outcome, scope, decisions, inputs, accepted dependencies, runnable base, and checks are sufficient. `T2` depending on `T1` waits for accepted completion, not merely an agent starting or submitting T1. Same-repository prerequisite code must be in the starting base; external prerequisites need their actual accepted artifact or service version.

Use the team's existing status names, or Draft, Ready, In progress, In review, Done, Blocked, and Changes requested. Record the reason for a blocker and the missing input. Review and Done are distinct decisions.

The designated tracker owns live status when present; otherwise one coordinator/integration owner updates the task table. Other summaries are snapshots. Parallel agents return their results rather than independently rewriting the same milestone file.

## Claiming and resuming

The runner, not a Markdown edit by the language model, owns claims. Concurrent dispatchers require an atomic claim for the complete logical task across all specification revisions. Record the run owner, full task reference, revision, repository/workspace, and progress. A new revision does not justify a second simultaneous run.

Before resuming or redispatching, inspect prior process state, branches, artifacts, and progress. Preserve unfinished work. A stale heartbeat alone is insufficient reason to start a duplicate. Material specification changes require a documented revision and handoff; the worker should not silently switch requirements mid-run.

## Doing the work

Read repository rules, the PRD, milestone overview, task row/notes, and linked references. Confirm the actual base and prerequisites, perform proportionate baseline checks, implement within scope, and collect the specified evidence. Choose routine implementation details within the stated contracts.

Report missing inputs, insufficient authority, or discoveries invalidating material assumptions as blockers. Keep existing failures visible. Preserve acceptance criteria and seek a scope revision when needed rather than weakening the task to match an implementation. Planning does not expand authority for code changes, publication, or deployment.

## Returning the result

Give the reviewer a short account of what changed and whether the task's observable result was achieved. Include passed/failed/not-run checks, linked evidence, unresolved gaps, and useful next steps. Record the task/specification/run/code/dependency revisions needed to reproduce or resume the work in the task notes or established tracker.

Separate implementation, checks, acceptance, merge, and deployment. Save bulky sanitized evidence only when it exists. The designated reviewer accepts the saved task revision before the task becomes Done.
