---
name: plan-runner
description: "Execute a plan.md written by plan-writer: the main agent coordinates, subagents (or a Workflow for parallel tasks) implement each task, and the coordinator re-verifies every task and updates the plan one task at a time. Pass `auto` to run every milestone unattended on a plan branch, stopping only on blockers. Use when the user gives a plan path and asks to run, execute, or continue it."
metadata:
  short-description: Coordinate subagents to execute a plan.md
---

# Plan Runner

You are the coordinator. Subagents implement tasks; you choose the work, brief them, re-run each check yourself, and keep `plan.md` truthful. You never implement a task yourself, and no subagent edits `plan.md`.

## Input

`/plan-runner <path-to-plan.md> [scope] [auto]` (Codex: `$plan-runner …`). Scope is optional: `M1` runs one milestone, `M1/T2` runs one task. `auto` runs the scope unattended; see [Auto mode](#auto-mode).

- No path: in auto mode, stop and ask for one. Otherwise find `docs/plans/*/plan.md` files with unfinished tasks. One match: name it and ask to confirm. Several: list and ask. None: say so and stop.
- Before starting, check the plan has a Graph, `## Mn:` milestones, and task tables with `Task | Do | Files | Depends | Verify | Status`; that the scope exists; and that at least one task in scope is Ready or In progress. Otherwise report exactly why (for example "M1/T2 is Draft: open question on timezone") and stop.
- Ask once at the start whether you may commit, one commit per verified task. Without that permission, run serially and leave changes uncommitted. In auto mode, `auto` is that permission: do not ask.

## Loop

Repeat until the scope is finished or you must stop:

1. **Pick.** Re-read `plan.md`. Ready tasks are those whose dependencies are all Done and whose notes have no **Open** item. Resume tasks left In progress first: inspect their existing changes and keep useful work; never start a duplicate.
2. **Choose the mode** for this batch of Ready tasks in the current milestone:
   - **Subagent** (default): one task at a time with the Agent tool, in the main working tree.
   - **Workflow**: only when two or more Ready tasks have disjoint Files and no shared migration, contract, or service, commits are allowed, and the Workflow tool is available. Follow [workflow mode](references/workflow.md). If the user asked for serial, never use it.
3. **Mark In progress.** Edit those rows' Status before dispatching.
4. **Dispatch** with the brief below.
5. **Verify each task, one at a time,** in Graph order:
   - Set Status to `In review`.
   - Read the diff. Reject changes outside the task's Files or scope.
   - Run the task's Verify yourself, scoped as in [Focused tests](#focused-tests). Do not accept the subagent's report as evidence.
   - **Pass:** commit if allowed, then immediately record it (see Updating the plan). Only then move to the next task.
   - **Fail:** send the failure output back to a subagent once. If it fails again, set `Blocked`, record why, and stop.
6. **Milestone gate.** When every task in the milestone is Done, run its **Demo** yourself, record the result, and stop. Ask the user to accept the milestone. Continue to the next milestone only after they accept and say to continue. In auto mode, follow [Auto mode](#auto-mode) instead.

Stop and ask instead of guessing when a task needs an open decision, a subagent reports a blocker, Verify cannot run in this environment, or a change would exceed the task's scope.

## Auto mode

`auto` means the user planned deeply and will review at the end, not during the run. Nobody is watching, so never wait on a question: where the loop says ask, stop and report instead.

1. **Branch.** Before the first task, work on `plan/<slug>`, where `<slug>` is the plan's folder name (`docs/plans/<slug>/plan.md`). If that branch exists, switch to it and resume. Otherwise create it from the current branch. If the working tree has uncommitted changes that are not In progress work from this plan, stop and report them; never stash or discard them.
2. **Commits.** One commit per verified task on that branch, as in the loop.
3. **Milestone gate.** Run the Demo yourself and record the result in Progress. Pass: add `- YYYY-MM-DD Mn Demo passed — <command> → <result>; auto-continued, awaiting user acceptance` and continue to the next milestone. Fail: set the milestone's failing work to Blocked with the output, and stop.
4. **Stops are unchanged.** An open decision, a second failure, a Verify that cannot run, or a change beyond a task's scope still stops the run. Record the reason in Progress first, so the next run resumes cleanly.
5. **Limits.** Never push, open a PR, merge, or deploy. Leave `## Done when` boxes that need user acceptance unticked.
6. **Report.** In the Finish report, also give the branch name, the milestones that passed their Demo and await acceptance, and the command to review them (`git log --oneline <base>..plan/<slug>`).

## Subagent brief

Each subagent knows only what you send. Include:

- The plan path, task reference (`M1/T2`), its table row, and its notes.
- The plan's Goal, Context, and Decisions, plus accepted outputs of its dependencies (commit or files).
- The files it may change. "Do not edit plan.md. Do not commit (unless told to in workflow mode). Do not change unrelated code."
- "Run only the tests for the files you changed, never the whole suite, in a single non-watch run. Run the Verify check the same way and return: files changed, the exact commands and output, and any blocker or assumption."

## Focused tests

Run tests for the change, not the whole suite. Full suites are slow, and stray runners keep running after an agent stops.

1. **Scope from the diff.** Take the changed files (`git diff --name-only` against the task's starting point) and run only their tests:
   - Spec files the task changed or added, plus specs that sit beside or import the changed source files.
   - Use the runner's own targeting when it has one: `jest <paths>` or `jest --findRelatedTests <changed files>`, `vitest run <paths>` or `vitest related <changed files>`, `pytest <test files or path::test>`, `go test ./<changed packages>`, `cargo test -p <crate> <filter>`.
   - Use the project's own script and config (for example `npm test -- <paths>`), so setup and environment match.
2. **Narrow a broad Verify.** If a task's Verify is the whole suite (`npm test`, `pytest`, `go test ./...`), run the focused equivalent instead and record the command you actually ran in the Progress line. Run a full suite only when the plan's Verify or Demo explicitly says "full suite", or the user asks.
3. **No focused tests found.** Do not fall back to the full suite. Say so, run the task's other checks (type check, lint, or the manual action in Verify) on the changed files, and report the missing coverage in the Progress line.
4. **One clean run.** No watch mode (`--watch`, `--watchAll`, `vitest` without `run`); pass the CI flag the runner needs (`CI=1`, `--runInBand` for Jest when parallel workers hang). Run tests in the foreground. If a run hangs or is interrupted, stop its processes before continuing, and never leave a test runner behind when you stop.

## Updating the plan

Update `plan.md` immediately after each task is verified, one edit per task, never batched at the end:

1. Set that row's Status to `Done`.
2. Append one line to `## Progress` (create it before the end of the file if missing; replace `- Not started`): `- YYYY-MM-DD M1/T2 Done — <Verify command> → <observed result> (<commit or "uncommitted">)`.
3. Tick a `## Done when` checkbox only when its condition has been observed, for example after the milestone Demo passes and the user accepts it. A Demo that passed in auto mode is not acceptance.
4. Recompute readiness: a dependent becomes Ready only now, after its dependency is Done. Update its Status if nothing else blocks it.

Blocked tasks get a Progress line with the reason and the missing input. Never mark Done from source inspection, a subagent's claim, or a check that did not run.

## Finish

Report: tasks Done (with their Progress lines), the Demo result, tasks Blocked or still Draft and why, commits made, and the next step. Implementation, verification, acceptance, merge, and deployment are separate facts; state which actually happened. Running a plan grants no permission to push, open PRs, or deploy.

For handing tasks to another machine, read the writer's worker handoff reference if installed (`plan-writer/references/worker-handoff.md`).
