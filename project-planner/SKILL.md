---
name: project-planner
description: "Write human-readable PRDs, milestone overviews, and milestone task tables grounded in repository evidence. Use to plan one project or a portfolio and prepare dependency-aware work for people or coding agents. Produces planning documents and handoff guidance; execution and scheduling are separate."
metadata:
  short-description: Human-readable PRDs, milestones, and task tables
---

# Project Planner

Write for the person building and reviewing the project. They should understand the goal, next step, dependencies, and meaning of done without learning an agent framework. Coding agents use the same documents.

## Readability and layout

Use ordinary Markdown, plain language, descriptive titles, short paragraphs, and compact tables. Lead with the user outcome. Define necessary technical terms. Keep engineering details next to the work they explain. Do not generate YAML frontmatter, JSON specifications, repetitive agent instructions, or a separate LLM-oriented copy of the plan unless the user explicitly requests an integration format.

For each plan, use this layout:

```text
PRD.md
Milestone.md
tasks/
  M1.md
  M2.md
```

`PRD.md` explains what and why. `Milestone.md` summarizes the ordered delivery outcomes. Each lowercase `tasks/Mn.md` contains all tasks for that milestone in one table, followed by task-specific implementation notes and verification. Never put every milestone's detailed tasks into one giant task document or create a separate file/folder for every task under this format.

Name milestones `M1`, `M2`, and tasks `T1`, `T2`. Task numbering restarts within each milestone. A table uses short IDs; cross-milestone references use `M1/T1`. For dispatch across plans or projects, use `PROJECT/PLAN/M1/T1`. Put project/plan, revision, repository, and inspected-code details in a short readable document-details section, not a metadata header.

Use the user's supplied examples when available. These templates are the fallback:

- [PRD](assets/prd.md).
- [Milestone overview](assets/milestone.md).
- [Tasks for one milestone](assets/tasks.md).

Use the existing plan directory, or `docs/plans/<plan-id>-<plan-slug>/` for a new plan. Keep links relative. Adapt example rows to the actual scope; do not force exactly two milestones or tasks. Preserve the case of `PRD.md`, `Milestone.md`, and lowercase `tasks` for Linux compatibility. Updating this skill alone does not migrate existing documents. When migration is requested, update links together and preserve a mapping from old planning IDs; do not rename persisted runtime identities.

## Understand the project

Read the user's request, applicable repository instructions, existing plans, and relevant code. Inspect the working tree without cleaning or resetting it. Identify the outcome, constraints, current behavior, relevant local changes, available services/data, and intended execution environment.

Honor the current request's execution boundary. For planning-only work, write planning documents and inspect evidence; do not implement the proposed feature to validate the plan, including throwaway prototypes, scratch copies, or temporary feature code. Check document structure, links, and verification-command syntax without implementing or running the future feature. Leave behavioral checks not run unless execution is already authorized. A temporary location does not expand authority; preserve explicit restrictions on commands and network access.

Separate observed implementation, user requirements, proposed design, and assumptions. Cite relevant source files. Inspect actual commands and interfaces; do not invent paths, signatures, performance targets, or passed checks. For external APIs not established locally, consult authoritative documentation. Verify library defaults and error behavior before making precise claims; distinguish application errors from exceptions raised by wrappers or clients. When evidence is unavailable, state what needs confirmation rather than inventing an exact result.

Ask only when missing information materially changes scope, architecture, acceptance, or authority. Resolve ordinary choices from existing conventions. Record assumptions and unanswered questions with their effect on delivery. A blocking uncertainty keeps the affected task Draft or Blocked; use a bounded investigation task when appropriate.

For Mac/VM work, record runtime versions, working directory, services, data, network/model access, and credential names without values. Use repository-relative paths in shared documents. A target label is not proof that a worker has been configured or checked.

## Write the PRD

Explain the user's problem, desired outcome, scope, exclusions, and concrete user journeys. Describe the existing baseline separately from future work. Assign stable requirement IDs and give each an observable acceptance condition. Include only operational constraints relevant to the product: data ownership, compatibility, recovery, observability, or permissions as needed.

Keep the main document understandable without following every technical link. Place long shared contracts or setup references in supporting documents only when useful; introduce them with a sentence explaining why a reader needs them. Map requirements to milestones and task references, or record an explicit deferral. Retain decisions and their reasons when revising the plan.

## Write the milestone overview

Use one `Milestone.md` with a compact roadmap table: milestone, user-visible outcome, prerequisites, task-file link, and status. Add a short section per milestone explaining its demonstration and completion condition. Describe already-built capabilities as the baseline; do not create pretend rebuild tasks for them.

Each milestone should deliver something a person can demonstrate. Investigate uncertainties before dependent implementation. Detail the next executable milestone fully; label later outlines Draft until their decisions, interfaces, and runnable bases are known. Do not claim implementation or runtime acceptance from source inspection alone.

## Write one task table per milestone

In `tasks/M1.md`, place shared setup and context once, then a table with these columns:

`Task | What to do | Depends on | Done when | Status`

Use one row per task, with a brief, concrete description. Immediately after the table, add `## Execution order` with the actual dependency sequence, for example **T1 → T2 → T3**. State that a dependent task becomes Ready only after the prerequisite result is accepted. Identify required previous-milestone inputs and any independent branches that can run together; do not turn a branching graph into an invented serial chain.

Follow that with `## Detailed task information`. Link each table ID to its `### T1`, `### T2` section there. Keep table cells short; put technical design, code locations, ordered steps, contracts, exact verification commands, expected results, and evidence instructions in the task section. Use `####` headings within a task. Keep shared setup before the task table so the reading order is overview, execution order, then detail. All tasks and their checks remain in this single milestone file.

Every task owns a reviewable outcome. Its notes cover the relevant requirements, scope, source locations, necessary inputs/outputs, persistence/compatibility rules, starting code revision, and unresolved decisions. Name the chosen algorithm, data structure, or technical approach and explain its rationale when that decision affects correctness or integration; leave ordinary coding choices with the implementer. Material unresolved design choices keep a task Draft. Distinguish proposed files/contracts from existing ones. Carry the user's existing authority for implementation, commits, pushes, PRs, and deployment; planning adds no execution permission.

Follow the project's verification policy, including restrictions on new tests. Provide checkable scenarios for success and relevant failures. State what to do, what should happen, and what evidence to save. Distinguish checks actually observed, commands confirmed by source inspection, and checks awaiting the target environment. Check command setup and variable scope across steps, and distinguish a wrapper’s exit status from its underlying command. For compatibility or multiple output formats, compare actual values as well as shape and counts. Recording a failed check completes evidence collection, not product acceptance; required failures must be resolved or explicitly accepted as a scoped deferral. Record results as passed, failed, or not run. Save bulky real evidence only when it exists, using a scoped location such as `evidence/M1/T1/` or the project's established verification directory.

## Dependencies and multiple agents

The dependency column is required. `T2` depending on `T1` waits for T1's accepted result; starting or submitting T1 does not unblock T2. Use `None` for genuinely independent work. Dependencies in the same milestone can use `T1`, in another milestone `M1/T1`, and outside the plan `PROJECT/PLAN/M1/T1`. Link the referenced row's detail section and resolve short names in the source row's context.

Validate dependency existence and cycles. Record accepted input versions and the runnable base before Ready. Tasks that share contracts, migrations, files, or services need ordering or an explicit integration owner even if their functional outcomes differ. Never remove a real dependency just to make the plan appear parallel.

Trace each required input in the detailed steps to its producing task or existing accepted artifact, including shared code, fixtures, routing, and runtime setup. A contract document is not a runnable schema module. For independent branches, put common implementation and a usable base in an accepted prerequisite, or name a separate producer and include its dependency. An integration owner must have an explicit task for producing required inputs before consumers start; naming that owner alone does not satisfy the dependency. If one branch must wait for another's shared code, record that edge or move the shared work before the fork. Check prose and tables against the same graph.

Identify which tasks can run together and why. Multiple agents require isolated workspaces, compatible editing scope, and sufficient service/model capacity. A coordinator or tracker owns live assignments and status updates so agents do not overwrite one another's shared task table. The runner implements atomic claims; a planning table is not a scheduler.

Read [worker handoff](references/worker-handoff.md) for separate sessions/machines, and [multi-project planning](references/multi-project.md) when coordinating several plans or projects. Keep those operational details out of the main product narrative unless the reader needs them.

## Review and deliver

Check that a human can identify the next task, what it changes, why it matters, its prerequisites, and how to verify it. Check requirements coverage, unique scoped IDs, working links/anchors, dependency graphs, and consistency of statuses and contracts. Each milestone's complete task list must be present in its one task file; do not leave an index pointing at nonexistent task documents.

Ready tasks have sufficient decisions, accessible inputs, satisfied dependencies, environment instructions, and observable checks. Draft/Blocked tasks explain what is missing. Keep specification changes explicit during active runs and preserve saved evidence. Retry instructions must inspect existing changes and preserve unrelated or useful partial work; identify run-owned disposable artifacts before recommending cleanup or rollback. Completion requires observed results and acceptance; source changes, a merge, and deployment are separate facts.

Statuses describe readiness now, not the expected execution sequence. A future prerequisite listed in this plan is not already accepted: keep its dependents Draft or Blocked, even when their design is complete. Do not label a whole future chain Ready and rely on prose to defer it. A bounded discovery or document-drafting task may be Ready with open questions as its output; split off code implementation that needs those answers and keep it Draft. Before delivery, check every Ready row against actual accepted inputs and unresolved decisions, then reconcile the task table, detail sections, and roadmap.

Return the document links, next executable work, remaining blockers, and checks performed. Stop after the requested planning deliverables unless execution is also authorized. For installation, read [installation](references/installation.md) and keep the complete skill folder together.
