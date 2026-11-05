---
name: plan-writer
description: "Write one focused plan.md with milestones, a dependency graph, and verifiable tasks, grounded in repository evidence. Use to plan a feature, refactor, or project for people or coding agents. Produces planning documents only; execution is separate."
metadata:
  short-description: One-file plans with milestones, task graph, and checks
---

# Plan Writer

Write one `plan.md` that a person can review and a coding agent can execute task by task. The plan holds the outcome, the dependency graph, the decisions an agent cannot safely make alone, and how to verify each step. Ordinary coding choices stay with the implementer.

## Before writing

- Read the request, repository instructions, existing plans, and the relevant code. Inspect the working tree without cleaning or resetting it.
- Separate what exists (cite `file:line`), what the user asked for, what you propose, and what you assume. Never invent paths, signatures, commands, targets, or passed checks.
- Ask only when a missing answer changes scope, architecture, or acceptance. Otherwise record it under Open questions and keep affected tasks Draft or Blocked.
- Planning only: do not implement, prototype, or run the future feature to validate the plan. Planning adds no permission to commit, push, or deploy.

## The file

Use the existing plan directory, or `docs/plans/<plan-slug>/plan.md`. Follow [the template](assets/plan.md). Sections, in order:

1. **Goal** — one sentence: what a user can do when this is finished.
2. **Context** — 3–5 lines: why, what already works (cited), what is out of scope.
3. **Graph** — one line covering every task, e.g. `M1/T1 → (M1/T2 ∥ M1/T3) → M2/T1`. `→` means "waits for", `∥` means "can run in parallel".
4. **Milestones** — `## M1: <outcome>`, each with a `**Demo:**` line and one task table. Optional `### M1/T2 notes` below the table.
5. **Done when** — checkboxes for the overall acceptance. Use requirement IDs (`R1`) only when the plan already has them or the user asks.
6. **Decisions** — choices already made and why (`D1: … because …`). Omit if empty.
7. **Open questions** — each with the tasks it blocks. Write `None` if none.
8. **Progress** — write `- Not started`. `plan-runner` appends one verified line per finished task.

No PRD, separate milestone file, per-task files, YAML frontmatter, or agent-only copy.

## Milestones

A milestone is an outcome someone can demonstrate, not a phase. The `**Demo:**` line is its acceptance: a concrete command or action and what should be observed. Later milestones are gated: their tasks stay Draft until the milestone they depend on is accepted. At most 5 milestones; detail the next one fully and keep later ones short and Draft. Describe already-built behavior in Context; do not create tasks to rebuild it.

## Tasks

One table per milestone with exactly these columns:

`Task | Do | Files | Depends | Verify | Status`

- **Task** — `T1`, `T2`, restarting in each milestone. Elsewhere refer to it as `M1/T2`.
- **Do** — one line, one reviewable outcome (about one PR). At most 7 tasks per milestone; split larger work into another plan.
- **Files** — existing paths to change, or proposed ones marked `(new)`.
- **Depends** — `None`, or comma-separated `T1` / `M1/T1`. Every real input must trace to a producing task or to existing code. Never drop a real edge to make work look parallel; never add a fake one.
- **Verify** — a concrete check: a command plus expected output, or an action plus observation. Include the relevant failure case. Not "works correctly".
- **Status** — `Draft`, `Ready`, `In progress`, `In review`, `Done`, or `Blocked`. Status means readiness now: a task is Ready only when every dependency is Done and it has no open decision.

## Notes: implementation details that belong in the plan

Add `### M1/T2 notes` only when a task needs it, at most about 8 lines. Each line is one of:

- **Contract** — formats, fields, interfaces other tasks rely on.
- **Approach** — the chosen algorithm, data structure, or design, with the reason, when it affects correctness or integration.
- **Reuse** — existing code to build on, cited `file:line`.
- **Constraints** — compatibility, no new dependencies, data or permission rules.
- **Edge cases** — the specific cases that must work.
- **Open** — an unresolved decision; the task stays Draft.

Leave out step-by-step code changes, names, and internal structure. If notes outgrow 8 lines, split the task or add a design task first.

## Review before delivering

- Every task appears in the Graph line, and the Graph matches the Depends column.
- Dependencies exist, have no cycles, and include every input each task needs.
- No Ready task has an unfinished dependency or open decision.
- Every Verify is concrete; no check is reported as passed unless it was observed.
- Links and `file:line` citations resolve.

Return the plan path, the next Ready task, the blockers, and the checks you performed. Stop after planning. To execute the plan, the user runs `plan-runner` with the plan path.

When updating an existing plan, keep existing IDs and decisions meaning what they meant; add new IDs instead of reusing old ones. For handing work to another agent or machine, read [worker handoff](references/worker-handoff.md). For several projects or plans, read [multi-project planning](references/multi-project.md). For installation, read [installation](references/installation.md).
